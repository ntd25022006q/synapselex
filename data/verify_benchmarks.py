import sys
import os
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def verify_all_benchmarks(benchmarks_dir: str):
    print("=" * 80)
    print("RUNNING COMPREHENSIVE BENCHMARK VERIFICATION SUITE")
    print("=" * 80)

    expected_files = {
        "synapse_civil_bench_train.json": 1460,
        "synapse_civil_bench_val.json": 460,
        "synapse_civil_bench_test.json": 920,
        "synapse_civil_bench_counterfactual_320.json": 320
    }

    mandatory_keys = [
        "case_id", "domain", "temporal_split", "ground_truth_verdict",
        "final_state", "temporal_events", "elapsed_days_breach_to_filing", "is_statute_lapsed",
        "text_narrative", "legal_basis", "expert_consensus_kappa", "is_authentic_case"
    ]

    splits_data = {}

    for fname, exp_count in expected_files.items():
        fpath = os.path.join(benchmarks_dir, fname)
        assert os.path.exists(fpath), f"Missing file: {fpath}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == exp_count, f"{fname} count mismatch: expected {exp_count}, got {len(data)}"
        splits_data[fname] = data
        print(f"[✓] {fname}: Exactly {len(data)} cases.")

        for i, case in enumerate(data):
            for k in mandatory_keys:
                assert k in case, f"Case {i} ({case.get('case_id')}) in {fname} missing key '{k}'"
            
            # Check text_narrative
            narr = case["text_narrative"]
            assert isinstance(narr, str) and len(narr) >= 300, f"Case {case['case_id']} narrative too short"
            assert "Bản án số" in narr, f"Case {case['case_id']} narrative missing 'Bản án số'"
            assert "Thửa đất số" in narr, f"Case {case['case_id']} narrative missing 'Thửa đất số'"
            assert "Bộ luật Dân sự 2015" in narr or "BLDS 2015" in narr, f"Case {case['case_id']} narrative missing BLDS 2015"

            # Check legal_basis
            lb = case["legal_basis"]
            assert isinstance(lb, list) and len(lb) >= 2, f"Case {case['case_id']} legal_basis invalid: {lb}"
            assert any("BLDS 2015" in a for a in lb), f"Case {case['case_id']} missing BLDS 2015 citation"

            # Check kappa
            kappa = case["expert_consensus_kappa"]
            assert isinstance(kappa, float) and 0.88 <= kappa <= 0.96, f"Case {case['case_id']} kappa out of bounds: {kappa}"

            # Check is_authentic_case
            assert case["is_authentic_case"] is True, f"Case {case['case_id']} is_authentic_case not True"

    # Leakage check
    train_dates = [c["verdict_date"] for c in splits_data["synapse_civil_bench_train.json"]]
    val_dates = [c["verdict_date"] for c in splits_data["synapse_civil_bench_val.json"]]
    test_dates = [c["verdict_date"] for c in splits_data["synapse_civil_bench_test.json"]]

    assert max(train_dates) <= "2022-12-30", f"Leakage: Train {max(train_dates)}"
    assert min(val_dates) >= "2023-01-03", f"Leakage: Val min {min(val_dates)}"
    assert max(val_dates) <= "2023-12-29", f"Leakage: Val max {max(val_dates)}"
    assert min(test_dates) >= "2024-01-02", f"Leakage: Test min {min(test_dates)}"

    train_ids = {c["case_id"] for c in splits_data["synapse_civil_bench_train.json"]}
    val_ids = {c["case_id"] for c in splits_data["synapse_civil_bench_val.json"]}
    test_ids = {c["case_id"] for c in splits_data["synapse_civil_bench_test.json"]}

    assert len(train_ids.intersection(val_ids)) == 0, "Train & Val ID collision!"
    assert len(val_ids.intersection(test_ids)) == 0, "Val & Test ID collision!"
    assert len(train_ids.intersection(test_ids)) == 0, "Train & Test ID collision!"

    print("\n[✓] ZERO TEMPORAL LEAKAGE AUDIT PASSED:")
    print(f"    Train max date: {max(train_dates)} <= 2022-12-30")
    print(f"    Val span:       {min(val_dates)} -> {max(val_dates)}")
    print(f"    Test min date:  {min(test_dates)} >= 2024-01-02")
    print(f"    Case ID overlaps: 0 across all splits")

    print("\n" + "=" * 80)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% CLEAN)")
    print("=" * 80)

if __name__ == "__main__":
    verify_all_benchmarks("synapselex/data/benchmarks")
