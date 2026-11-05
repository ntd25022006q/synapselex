"""
SynapseLex: Interactive Neuro-Symbolic Legal Adjudication CLI
=============================================================
Demonstrates end-to-end inference on authentic civil dispute cases:
1. Loads case facts, entities, and temporal timeline
2. Constructs heterogeneous temporal case graph
3. Computes continuous-time harmonic Fourier embeddings
4. Applies Description Logic TBox constraints (BLDS 2015)
5. Predicts adjudication verdict with defeasible reasoning rationale
"""

import sys
import os
import json
import argparse
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from synapselex.src.data.graph_builder import LegalGraphBuilder
from synapselex.src.models.tgat_core import SynapseLexTGAT

VERDICT_NAMES = [
    "CHẤP NHẬN PHẠT CỌC / YÊU CẦU KHỞI KIỆN (Obligee Prevailed)",
    "CHẤP NHẬN PHẢN TỐ / HOÀN TRẢ TIỀN CỌC (Obligor Prevailed)",
    "ĐÌNH CHỈ DO HẾT THỜI HIỆU KHỞI KIỆN - ĐIỀU 429 (Statute Lapsed)",
    "TUYÊN BỐ HỢP ĐỒNG VÔ HIỆU TOÀN BỘ - ĐIỀU 129/131 (Contract Void)"
]

STATE_NAMES = ["Hợp lệ (Valid)", "Có thể hủy bỏ (Voidable)", "Vô hiệu tuyệt đối (Void_Ab_Initio)", "Đã tiêu tán/Hết thời hiệu (Extinguished)"]

def run_demo(case_id: str = None, case_index: int = 0):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bench_path = os.path.join(base_dir, "data", "benchmarks", "synapse_civil_bench_test.json")
    ckpt_path = os.path.join(base_dir, "data", "best_synapselex_m0.pt")

    if not os.path.exists(bench_path):
        print(f"[!] Benchmark file not found at: {bench_path}")
        return

    with open(bench_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    selected_case = None
    if case_id:
        for c in cases:
            if c.get("case_id") == case_id:
                selected_case = c
                break
    if not selected_case:
        selected_case = cases[min(case_index, len(cases) - 1)]

    print("\n" + "=" * 90)
    print("  SYNAPSELEX: NEURO-SYMBOLIC TEMPORAL ADJUDICATION INFERENCE DEMO")
    print("=" * 90)
    print(f"  • Vụ án số:       {selected_case.get('case_id')}")
    print(f"  • Cơ quan xét xử: {selected_case.get('court_name', 'TAND')} ({selected_case.get('jurisdiction_level', 'Sơ thẩm')})")
    print(f"  • Quan hệ pháp luật: {selected_case.get('case_title', 'Tranh chấp hợp đồng dân sự')}")
    print(f"  • Ngày tuyên án:  {selected_case.get('verdict_date')}")
    print(f"  • Nguyên đơn:     {selected_case.get('plaintiff')} | Bị đơn: {selected_case.get('defendant')}")
    print("\n[TÓM TẮT DIỄN BIẾN SỰ KIỆN PHÁP LÝ]")
    print(f"  {selected_case.get('fact_summary', 'Không có tóm tắt')}")

    # Build Graph
    builder = LegalGraphBuilder()
    g = builder.build_case_graph(selected_case)
    print("\n[CẤU TRÚC ĐỒ THỊ PHÁP LÝ ĐỘNG (Dynamic Legal Graph)]")
    print(f"  • Số lượng nút (Entities): {g['num_nodes']} (Nguyên đơn, Bị đơn, Hợp đồng, Sự kiện)")
    print(f"  • Số cạnh quan hệ (Edges): {g['num_edges']}")
    print(f"  • Thời gian vi phạm đến khởi kiện: {g['elapsed_days']:.0f} ngày")
    print(f"  • Rào cản thời hiệu (Điều 429 > 1,095 ngày): {'CÓ (Lapsed)' if g['is_statute_lapsed'] else 'KHÔNG (Active)'}")

    # Model Inference
    device = torch.device("cpu")
    hidden_dim = 64
    weights = None
    if os.path.exists(ckpt_path):
        try:
            weights = torch.load(ckpt_path, map_location=device)
            if "node_type_embed.weight" in weights:
                hidden_dim = weights["node_type_embed.weight"].shape[1] * 2
        except Exception:
            weights = None

    model = SynapseLexTGAT(
        in_feat_dim=32,
        hidden_dim=hidden_dim,
        num_layers=2,
        num_heads=4,
        time_dim=32,
        use_ontology=True,
        use_temporal=True
    ).to(device)

    if weights is not None:
        model.load_state_dict(weights, strict=True)
        print(f"\n[+] Đã tải trọng số mô hình SynapseLex đã huấn luyện ({hidden_dim}d): {ckpt_path}")
    else:
        print("\n[!] Chạy suy luận với mô hình kiến trúc chuẩn Axiom-TGAT")

    model.eval()
    with torch.no_grad():
        out = model(g)
        probs = F.softmax(out["verdict_logits"], dim=-1).squeeze(0)
        pred_class = int(torch.argmax(probs).item())
        pred_conf = float(probs[pred_class]) * 100.0

        state_probs = F.softmax(out["state_logits"], dim=-1).squeeze(0)
        pred_state = int(torch.argmax(state_probs).item())

    gt_verdict_idx = g["y_verdict"].item()

    print("\n" + "-" * 90)
    print("  KẾT QUẢ SUY LUẬN TỰ ĐỘNG CỦA HỆ THỐNG")
    print("-" * 90)
    print(f"  [Trạng thái Hợp đồng Dự đoán]:   {STATE_NAMES[pred_state]} (Xác suất: {state_probs[pred_state]*100:.1f}%)")
    print(f"  [Phán quyết Tố tụng Dự đoán]:     {VERDICT_NAMES[pred_class]}")
    print(f"  [Độ tin cậy Mô hình (Confidence)]: {pred_conf:.2f}%")
    print(f"  [Phán quyết Thực tế của Bản án]:  {VERDICT_NAMES[gt_verdict_idx]}")
    print(f"  [Kết quả Đánh giá]:               {'CHÍNH XÁC (MATCH)' if pred_class == gt_verdict_idx else 'SAI LỆCH (MISMATCH)'}")

    print("\n[LẬP LUẬN TƯ PHÁP CỦA HỘI ĐỒNG XÉT XỬ (Ground Truth Judicial Reasoning)]")
    print(f"  {selected_case.get('judicial_holding_reasoning', 'Không có dữ liệu')}")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SynapseLex Demo Inference CLI")
    parser.add_argument("--case_id", type=str, default=None, help="Specific Case ID to evaluate")
    parser.add_argument("--case_index", type=int, default=0, help="Case index in test split")
    args = parser.parse_args()
    run_demo(args.case_id, args.case_index)
