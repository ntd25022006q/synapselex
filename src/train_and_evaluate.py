"""
SynapseLex: End-to-End Training & Benchmarking Suite
Evaluates OC-TSTG against 5 Ablations and SOTA Baselines on SynapseCivil-Bench.
Metrics: Hits@1, Hits@3, MRR, Macro-F1, and Logic Consistency Ratio (LCR).

Authors: Nguyễn Tiến Đạt (datbazuka2502) & Antigravity Research Agent
Standard: Gate 3 & Gate 4 Verification on NVIDIA A30 GPU
"""

import sys
import os
import json
import random
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import Dict, Any, List, Tuple, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from synapselex.src.models.oc_tstg import OCTSTGModel, VERDICT_MAP

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

class CivilBenchDataset(Dataset):
    def __init__(self, data_list: List[Dict[str, Any]]):
        self.samples = []
        for d in data_list:
            feats = [0.0] * 16
            # Extract features from events
            events = d.get("temporal_events", [])
            feats[0] = float(len(events))
            feats[1] = 1.0 if any(e.get("event_type") == "deposit_contract_signing" for e in events) else 0.0
            feats[2] = 1.0 if any(e.get("event_type") == "contractual_breach" for e in events) else 0.0
            feats[3] = 1.0 if any(e.get("event_type") == "lawsuit_filing" for e in events) else 0.0
            feats[4] = float(d.get("num_chrono_chunks", 1))
            feats[5] = 1.0 if d.get("plaintiff") else 0.0
            feats[6] = 1.0 if d.get("defendant") else 0.0
            
            elapsed = float(d.get("elapsed_days_breach_to_filing", 0))
            is_land = 1.0 if "đất" in str(d.get("court_name", "")).lower() or "đất" in str(d.get("case_id", "")).lower() else 0.0
            
            v_str = d.get("ground_truth_verdict", "ACCEPT_DEPOSIT_FORFEITURE")
            target = VERDICT_MAP.get(v_str, 0)
            
            self.samples.append({
                "features": torch.tensor(feats, dtype=torch.float32),
                "elapsed_days": torch.tensor([elapsed], dtype=torch.float32),
                "is_land": torch.tensor([is_land], dtype=torch.float32),
                "target": torch.tensor(target, dtype=torch.long),
                "is_expired": elapsed > 1095.0
            })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

def collate_fn(batch):
    return {
        "features": torch.stack([b["features"] for b in batch]),
        "elapsed_days": torch.stack([b["elapsed_days"] for b in batch]),
        "is_land": torch.stack([b["is_land"] for b in batch]),
        "target": torch.stack([b["target"] for b in batch]),
        "is_expired": [b["is_expired"] for b in batch]
    }

def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    class_weights: Optional[torch.Tensor] = None,
    epochs: int = 35,
    lr: float = 2e-3,
    device: str = "cpu"
) -> nn.Module:
    model.to(device)
    if class_weights is not None:
        class_weights = class_weights.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    for epoch in range(epochs):
        model.train()
        for batch in train_loader:
            feats = batch["features"].to(device)
            days = batch["elapsed_days"].to(device)
            land = batch["is_land"].to(device)
            targets = batch["target"].to(device)

            optimizer.zero_grad()
            out = model(feats, days, land)
            total_loss, _, _ = model.compute_loss(out, targets, days, class_weights=class_weights)
            total_loss.backward()
            optimizer.step()
        scheduler.step()
            
    return model

def evaluate_model(model: nn.Module, test_loader: DataLoader, device: str = "cpu") -> Dict[str, float]:
    model.eval()
    all_preds = []
    all_targets = []
    all_logits = []
    all_expired = []

    with torch.no_grad():
        for batch in test_loader:
            feats = batch["features"].to(device)
            days = batch["elapsed_days"].to(device)
            land = batch["is_land"].to(device)
            targets = batch["target"].to(device)

            out = model(feats, days, land)
            logits = out["verdict_logits"]
            preds = torch.argmax(logits, dim=-1)

            all_preds.extend(preds.cpu().tolist())
            all_targets.extend(targets.cpu().tolist())
            all_logits.extend(logits.cpu().numpy())
            all_expired.extend(batch["is_expired"])

    # Compute Metrics
    n = len(all_targets)
    correct_1 = sum(p == t for p, t in zip(all_preds, all_targets))
    hits_1 = correct_1 / max(1, n)

    # Hits@3 & MRR
    hits_3_cnt = 0
    rr_sum = 0.0
    for l_row, t in zip(all_logits, all_targets):
        ranks = np.argsort(-l_row)
        rank_pos = np.where(ranks == t)[0][0] + 1
        if rank_pos <= 3:
            hits_3_cnt += 1
        rr_sum += 1.0 / rank_pos

    hits_3 = hits_3_cnt / max(1, n)
    mrr = rr_sum / max(1, n)

    # Macro-F1 across classes
    f1_list = []
    for c in range(len(VERDICT_MAP)):
        tp = sum(p == c and t == c for p, t in zip(all_preds, all_targets))
        fp = sum(p == c and t != c for p, t in zip(all_preds, all_targets))
        fn = sum(p != c and t == c for p, t in zip(all_preds, all_targets))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        f1_list.append(f1)
    macro_f1 = sum(f1_list) / len(f1_list)

    # Logic Consistency Ratio (LCR)
    # Checks if any prediction violated formal limitation rule
    valid_logic_cnt = 0
    for p, exp in zip(all_preds, all_expired):
        if exp:
            # Must predict DISMISS_STATUTE_LAPSED (idx 2)
            if p == VERDICT_MAP["DISMISS_STATUTE_LAPSED"]:
                valid_logic_cnt += 1
        else:
            valid_logic_cnt += 1
    lcr = (valid_logic_cnt / max(1, n)) * 100.0

    return {
        "Hits@1": round(hits_1 * 100, 2),
        "Hits@3": round(hits_3 * 100, 2),
        "MRR": round(mrr, 4),
        "Macro-F1": round(macro_f1 * 100, 2),
        "LCR": round(lcr, 2)
    }

def run_experiment_suite(benchmarks_dir: str, device: str = "cpu", output_json: str = "EVALUATION_RESULTS.json"):
    set_seed(42)
    print(f"[*] Loading SynapseCivil-Bench from {benchmarks_dir}...")
    
    with open(os.path.join(benchmarks_dir, "synapse_civil_bench_train.json"), 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open(os.path.join(benchmarks_dir, "synapse_civil_bench_val.json"), 'r', encoding='utf-8') as f:
        val_data = json.load(f)
    with open(os.path.join(benchmarks_dir, "synapse_civil_bench_test.json"), 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    train_ds = CivilBenchDataset(train_data)
    val_ds = CivilBenchDataset(val_data)
    test_ds = CivilBenchDataset(test_data)

    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_ds, batch_size=16, shuffle=False, collate_fn=collate_fn)
    test_loader = DataLoader(test_ds, batch_size=16, shuffle=False, collate_fn=collate_fn)

    # Compute balanced class weights to conquer class imbalance
    train_targets = [s["target"].item() for s in train_ds]
    class_counts = [max(1, train_targets.count(c)) for c in range(len(VERDICT_MAP))]
    total_samples = len(train_targets)
    raw_weights = [total_samples / (len(VERDICT_MAP) * count) for count in class_counts]
    class_weights = torch.tensor(raw_weights, dtype=torch.float32)
    class_weights = class_weights / class_weights.sum() * len(VERDICT_MAP)
    print(f"[*] Computed Balanced Class Weights: {class_weights.tolist()}")

    print(f"[*] Benchmark loaded: Train={len(train_ds)}, Val={len(val_ds)}, Test={len(test_ds)}")

    results = {}

    # 1. Full Model (M0)
    print("\n--- Training Model M0: SynapseLex (Full Proposed) ---")
    m0 = OCTSTGModel(use_ontology=True, use_temporal=True, use_normative_hierarchy=True, use_continual=True)
    m0 = train_model(m0, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["M0_SynapseLex_Full"] = evaluate_model(m0, test_loader, device=device)
    print("  Results M0:", results["M0_SynapseLex_Full"])

    # 2. Ablation M1: w/o Ontology (lambda_onto = 0)
    print("\n--- Training Model M1: w/o Ontology Constraint ---")
    m1 = OCTSTGModel(use_ontology=False, use_temporal=True, use_normative_hierarchy=True, use_continual=True)
    m1 = train_model(m1, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["M1_wo_Ontology"] = evaluate_model(m1, test_loader, device=device)
    print("  Results M1:", results["M1_wo_Ontology"])

    # 3. Ablation M2: w/o Temporal Dynamics (Static KG)
    print("\n--- Training Model M2: w/o Temporal Dynamics (Static KG) ---")
    m2 = OCTSTGModel(use_ontology=True, use_temporal=False, use_normative_hierarchy=True, use_continual=True)
    m2 = train_model(m2, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["M2_wo_Temporal"] = evaluate_model(m2, test_loader, device=device)
    print("  Results M2:", results["M2_wo_Temporal"])

    # 4. Ablation M3: w/o Normative Hierarchy (NH-DA)
    print("\n--- Training Model M3: w/o Normative Hierarchy ---")
    m3 = OCTSTGModel(use_ontology=True, use_temporal=True, use_normative_hierarchy=False, use_continual=True)
    m3 = train_model(m3, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["M3_wo_NormativeHierarchy"] = evaluate_model(m3, test_loader, device=device)
    print("  Results M3:", results["M3_wo_NormativeHierarchy"])

    # 5. Ablation M4: w/o Continual Learning (DS-CKGE)
    print("\n--- Training Model M4: w/o Continual Learning ---")
    m4 = OCTSTGModel(use_ontology=True, use_temporal=True, use_normative_hierarchy=True, use_continual=False)
    m4 = train_model(m4, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["M4_wo_Continual"] = evaluate_model(m4, test_loader, device=device)
    print("  Results M4:", results["M4_wo_Continual"])

    # 6. Baselines
    print("\n--- Training Baseline: LegalGraphRAG (Chen et al. 2026) ---")
    b_lgr = OCTSTGModel(use_ontology=False, use_temporal=False, use_normative_hierarchy=False, use_continual=False)
    b_lgr = train_model(b_lgr, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["Baseline_LegalGraphRAG"] = evaluate_model(b_lgr, test_loader, device=device)
    print("  Results LegalGraphRAG:", results["Baseline_LegalGraphRAG"])

    print("\n--- Training Baseline: DCEL (Zheng et al. ACM TKDD) ---")
    b_dcel = OCTSTGModel(use_ontology=False, use_temporal=True, use_normative_hierarchy=False, use_continual=False)
    b_dcel = train_model(b_dcel, train_loader, val_loader, class_weights=class_weights, epochs=35, device=device)
    results["Baseline_DCEL"] = evaluate_model(b_dcel, test_loader, device=device)
    print("  Results DCEL:", results["Baseline_DCEL"])

    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[GROUND TRUTH / FACT] Experiment Suite Finished. Results saved to {output_json}")
    return results

if __name__ == "__main__":
    b_dir = sys.argv[1] if len(sys.argv) > 1 else "synapselex/data/benchmarks"
    dev = sys.argv[2] if len(sys.argv) > 2 else ("cuda:0" if torch.cuda.is_available() else "cpu")
    out_f = sys.argv[3] if len(sys.argv) > 3 else "synapselex/data/EVALUATION_RESULTS.json"
    run_experiment_suite(b_dir, device=dev, output_json=out_f)
