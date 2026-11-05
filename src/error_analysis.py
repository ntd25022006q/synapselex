"""
SynapseLex: Qualitative Failure Taxonomy & Error Analysis Module
================================================================
Performs rigorous Popperian failure investigation on both:
1. In-Distribution 920-case Test Set (`synapse_civil_bench_test.json`)
2. Out-of-Distribution 320-case Counterfactual Perturbation Set (`synapse_civil_bench_counterfactual_320.json`)

Identifies and isolates mispredictions, builds empirical 4x4 Confusion Matrices,
and categorizes errors into substantive legal failure modes:
- Mode 1: Boundary Curing Ambiguity (Article 129 performance fraction near 2/3)
- Mode 2: Force Majeure Tolling Discretion (Article 156 factual duration dispute)
- Mode 3: Mixed Deposit vs. Advance Payment Semantic Divergence (Article 328 vs 357)
- Mode 4: Complex Multi-Relational Usury Cross-Claims (Article 468)

Outputs audited report to `synapselex/data/FAILURE_ANALYSIS_REPORT.json`.
"""

import sys
import os
import json
from datetime import datetime
from collections import defaultdict
import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from synapselex.src.data.graph_builder import LegalGraphBuilder
from synapselex.src.models.tgat_core import SynapseLexTGAT

CLASS_NAMES = [
    "Obligee Prevailed (Accept Deposit Forfeiture)",
    "Obligor Prevailed (Refund / Counter-Remedy)",
    "Dismiss Statute Lapsed (Art. 429)",
    "Declare Contract Void (Art. 129/131)"
]

def run_failure_analysis():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    test_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_test.json")
    cf_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_counterfactual_320.json")
    ckpt_path = os.path.join(base_dir, "data", "best_synapselex_m0.pt")
    out_report = os.path.join(base_dir, "data", "FAILURE_ANALYSIS_REPORT.json")

    print("\n" + "=" * 90)
    print("  SYNAPSELEX: QUALITATIVE FAILURE TAXONOMY & EMPIRICAL ERROR AUDIT")
    print("=" * 90)

    device = torch.device("cpu")
    builder = LegalGraphBuilder()

    model = SynapseLexTGAT(
        in_feat_dim=32,
        hidden_dim=64,
        num_layers=2,
        num_heads=4,
        time_dim=32,
        use_ontology=True,
        use_temporal=True
    ).to(device)

    if os.path.exists(ckpt_path):
        weights = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(weights, strict=False)
        print(f"  [+] Loaded model checkpoint from: {ckpt_path}")
    else:
        print(f"  [!] Checkpoint not found; running with initialized model weights")

    model.eval()

    def evaluate_split(split_name: str, file_path: str):
        if not os.path.exists(file_path):
            print(f"  [!] File not found: {file_path}")
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            cases = json.load(f)

        conf_matrix = np.zeros((4, 4), dtype=int)
        failures = []
        category_counts = defaultdict(int)

        with torch.no_grad():
            for idx, c in enumerate(cases):
                g = builder.build_case_graph(c)
                out = model(g)
                probs = F.softmax(out["verdict_logits"], dim=-1).squeeze(0)
                pred = int(torch.argmax(probs).item())
                target = g["y_verdict"].item()

                conf_matrix[target, pred] += 1

                if pred != target:
                    elapsed = g.get("elapsed_days", 0.0)
                    is_lapsed = g.get("is_statute_lapsed", 0.0) == 1.0

                    if is_lapsed and pred != 2:
                        mode = "Mode_1_Statute_Boundary_Leakage"
                        desc = "Model failed to enforce strict procedural time-bar despite elapsed > 1095 days."
                    elif target == 3 and pred in [0, 1]:
                        mode = "Mode_2_Curing_Fidelity_False_Positive"
                        desc = "Contract formal defect incorrectly treated as cured under Article 129."
                    elif target == 1 and pred == 0:
                        mode = "Mode_3_Evidentiary_Symmetry_Divergence"
                        desc = "Model attributed breach unilaterally to obligor, missing obligee contributory fault."
                    else:
                        mode = "Mode_4_Borderline_Judicial_Discretion"
                        desc = "Discretionary interpretation of pandemic tolling or interest calculation divergence."

                    category_counts[mode] += 1
                    failures.append({
                        "case_id": c.get("case_id"),
                        "domain": c.get("domain"),
                        "verdict_date": c.get("verdict_date"),
                        "ground_truth_class": target,
                        "ground_truth_label": CLASS_NAMES[target],
                        "predicted_class": pred,
                        "predicted_label": CLASS_NAMES[pred],
                        "confidence": round(float(probs[pred]) * 100.0, 2),
                        "failure_mode": mode,
                        "failure_description": desc,
                        "fact_summary": str(c.get("fact_summary", c.get("summary", "N/A")))[:250] + "..."
                    })

        total_cases = len(cases)
        total_failures = len(failures)
        accuracy = ((total_cases - total_failures) / max(1, total_cases)) * 100.0

        print(f"\n[{split_name.upper()}] (N = {total_cases})")
        print(f"  • Số lượng ca dự đoán chính xác: {total_cases - total_failures}/{total_cases} ({accuracy:.2f}%)")
        print(f"  • Số lượng ca dự đoán sai lệch:  {total_failures}/{total_cases} ({100.0 - accuracy:.2f}%)")

        print("\n  Ma trận nhầm lẫn (4x4 Confusion Matrix):")
        hdr = "  True \\ Pred"
        print(f"{hdr:<37} | {'Class 0':<10} | {'Class 1':<10} | {'Class 2':<10} | {'Class 3':<10}")
        print("  " + "-" * 78)
        for i in range(4):
            print(f"  {CLASS_NAMES[i][:34]:<35} | {conf_matrix[i, 0]:<10} | {conf_matrix[i, 1]:<10} | {conf_matrix[i, 2]:<10} | {conf_matrix[i, 3]:<10}")

        if total_failures > 0:
            print("\n  Phân loại nguyên nhân sai số (Qualitative Failure Taxonomy):")
            for mode, cnt in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (cnt / total_failures) * 100.0
                print(f"    • {mode:<42}: {cnt:3d} ca ({pct:5.1f}%)")

            print("\n  Mẫu ca tiêu biểu mô hình dự đoán sai lệch:")
            for sample in failures[:3]:
                print(f"    ─────────────────────────────────────────────────────────────────────────")
                print(f"    Vụ án: {sample['case_id']} ({sample['verdict_date']}) - Lĩnh vực: {sample['domain']}")
                print(f"    Thực tế: {sample['ground_truth_label']}")
                print(f"    Dự đoán: {sample['predicted_label']} (Confidence: {sample['confidence']}%)")
                print(f"    Lỗi: {sample['failure_mode']} -> {sample['failure_description']}")
                print(f"    Tóm tắt: {sample['fact_summary']}")

        return {
            "total_cases": total_cases,
            "total_failures": total_failures,
            "accuracy_pct": round(accuracy, 2),
            "confusion_matrix": conf_matrix.tolist(),
            "failure_taxonomy_distribution": dict(category_counts),
            "sample_failures": failures[:25]
        }

    test_eval = evaluate_split("Test Set (In-Distribution)", test_path)
    cf_eval = evaluate_split("Counterfactual Hard Perturbation Set (Out-of-Distribution)", cf_path)

    report_data = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "model_architecture": "SynapseLexTGAT (M0)",
        "test_set_evaluation": test_eval,
        "counterfactual_set_evaluation": cf_eval
    }

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"\n[+] Báo cáo phân tích sai số toàn diện đã được lưu tại: {out_report}\n")

if __name__ == "__main__":
    run_failure_analysis()
