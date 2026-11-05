"""
SynapseLex: Clean, Target-Leak-Free Training Script
Trains SynapseLexTGAT (M0) on genuine observable legal graph features.
"""

import sys
import os
import json
import random
import time
from collections import Counter
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from synapselex.src.data.graph_builder import LegalGraphBuilder
from synapselex.src.models.tgat_core import SynapseLexTGAT

def train_clean_model():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    train_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_train.json")
    val_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_val.json")
    test_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_test.json")
    ckpt_path = os.path.join(base_dir, "data", "best_synapselex_m0.pt")

    device = torch.device("cpu")
    builder = LegalGraphBuilder()

    print("[*] Loading training and validation splits...")
    with open(train_path, "r", encoding="utf-8") as f:
        train_raw = json.load(f)
    with open(val_path, "r", encoding="utf-8") as f:
        val_raw = json.load(f)
    with open(test_path, "r", encoding="utf-8") as f:
        test_raw = json.load(f)

    # Convert to graphs
    train_graphs = [builder.build_case_graph(c) for c in train_raw[:500]]
    val_graphs = [builder.build_case_graph(c) for c in val_raw[:150]]
    test_graphs = [builder.build_case_graph(c) for c in test_raw]

    print(f"  • Loaded {len(train_graphs)} train, {len(val_graphs)} val, {len(test_graphs)} test graphs.")

    # Class balance weights
    train_verdicts = [g["y_verdict"].item() for g in train_graphs]
    counts = Counter(train_verdicts)
    total_t = len(train_verdicts)
    weights = [total_t / max(1, counts.get(c, 1)) for c in range(4)]
    weight_tensor = torch.tensor(weights, dtype=torch.float32).to(device)

    # Initialize model
    model = SynapseLexTGAT(
        in_feat_dim=32,
        hidden_dim=64,
        num_layers=2,
        num_heads=4,
        time_dim=32,
        dropout=0.1,
        use_ontology=True,
        use_temporal=True
    ).to(device)

    optimizer = optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    epochs = 4
    best_val_f1 = -1.0
    best_weights = None

    print(f"\n[*] Training SynapseLexTGAT for {epochs} epochs on leak-free graphs...")
    for ep in range(epochs):
        model.train()
        train_shuffled = list(train_graphs)
        random.shuffle(train_shuffled)
        total_loss = 0.0

        for g in train_shuffled:
            optimizer.zero_grad()
            out = model(g)
            l_v = F.cross_entropy(out["verdict_logits"], g["y_verdict"].view(-1), weight=weight_tensor)
            l_s = F.cross_entropy(out["state_logits"], g["y_state"].view(-1))
            loss = l_v + 0.5 * l_s
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        # Validation
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for g in val_graphs:
                out = model(g)
                pred = int(torch.argmax(out["verdict_logits"], dim=-1).item())
                val_preds.append(pred)
                val_targets.append(g["y_verdict"].item())

        val_acc = sum(1 for p, t in zip(val_preds, val_targets) if p == t) / len(val_targets) * 100.0
        print(f"  Epoch {ep+1}/{epochs} | Train Loss: {total_loss/len(train_graphs):.4f} | Val Accuracy: {val_acc:.2f}%")

        if val_acc > best_val_f1:
            best_val_f1 = val_acc
            best_weights = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    if best_weights:
        torch.save(best_weights, ckpt_path)
        print(f"[+] Successfully saved clean checkpoint to: {ckpt_path}")
        model.load_state_dict(best_weights)

    # Evaluate on test set
    model.eval()
    test_preds, test_targets = [], []
    with torch.no_grad():
        for g in test_graphs:
            out = model(g)
            pred = int(torch.argmax(out["verdict_logits"], dim=-1).item())
            test_preds.append(pred)
            test_targets.append(g["y_verdict"].item())

    test_acc = sum(1 for p, t in zip(test_preds, test_targets) if p == t) / len(test_targets) * 100.0
    print(f"\n[+] Evaluated on {len(test_graphs)} test cases:")
    print(f"    Clean Test Accuracy: {test_acc:.2f}% (Realistic, No Target Leakage)")

if __name__ == "__main__":
    train_clean_model()
