"""
SynapseLex: Two-Stage Self-Verification & IAA Audit Engine
Performs multi-tier logical and temporal consistency checks on extracted legal graphs.
Computes Cohen's Kappa Inter-Annotator Agreement (IAA) score for scientific publication.

Authors: Nguyễn Tiến Đạt (datbazuka2502) & Antigravity Research Agent
Standard: Gate 2 Verification (Cohen's Kappa >= 0.85, Zero Forward Temporal Leakage)
"""

import sys
import os
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class SelfVerifier:
    def __init__(self):
        pass

    def verify_case_graph(self, case_graph: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Runs 3-stage self-verification on an extracted case graph:
        1. Role & Identity Integrity
        2. Temporal Ordering Validity
        3. TBox Description Logic Consistency (BLDS 2015 Art. 429)
        """
        issues = []
        
        # 1. Role Integrity
        plaintiff = case_graph.get("plaintiff", "").strip().lower()
        defendant = case_graph.get("defendant", "").strip().lower()
        if not plaintiff or plaintiff == "nguyên đơn":
            issues.append("Missing or ungrounded Plaintiff entity")
        if not defendant or defendant == "bị đơn":
            issues.append("Missing or ungrounded Defendant entity")
        if plaintiff and defendant and plaintiff == defendant:
            issues.append(f"Identity collision: Plaintiff and Defendant have identical name '{plaintiff}'")

        # 2. Temporal Ordering Validity
        t_deposit = case_graph.get("earliest_deposit_date")
        t_breach = case_graph.get("breach_date")
        t_filing = case_graph.get("filing_date")
        t_verdict = case_graph.get("verdict_date")

        def _safe_dt(s):
            if not s:
                return None
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except Exception:
                return None

        dt_deposit = _safe_dt(t_deposit)
        dt_breach = _safe_dt(t_breach)
        dt_filing = _safe_dt(t_filing)
        dt_verdict = _safe_dt(t_verdict)

        if t_deposit and not dt_deposit:
            issues.append(f"Malformed date string for deposit: {t_deposit}")
        if t_breach and not dt_breach:
            issues.append(f"Malformed date string for breach: {t_breach}")
        if t_filing and not dt_filing:
            issues.append(f"Malformed date string for filing: {t_filing}")

        if dt_deposit and dt_breach and dt_deposit > dt_breach:
            issues.append(f"Temporal anomaly: Deposit date ({t_deposit}) occurs AFTER breach date ({t_breach})")
            
        if dt_breach and dt_filing and dt_breach > dt_filing:
            issues.append(f"Temporal anomaly: Breach date ({t_breach}) occurs AFTER filing date ({t_filing})")

        if dt_filing and dt_verdict and dt_filing > dt_verdict:
            issues.append(f"Temporal anomaly: Filing date ({t_filing}) occurs AFTER verdict date ({t_verdict})")

        # 3. Axiomatic Consistency Check (Article 429 BLDS 2015)
        if dt_breach and dt_filing:
            diff_days = (dt_filing - dt_breach).days
            if diff_days > 1095:
                # Must be marked extinguished or statute lapsed
                if not case_graph.get("is_statute_lapsed"):
                    issues.append(f"Axiom violation: Elapsed time {diff_days} days > 1095 days, but is_statute_lapsed is False")

        # 4. Strict Forward Temporal Split Guard
        split = case_graph.get("temporal_split", "")
        if not dt_verdict:
            issues.append("Missing or invalid verdict date")
        else:
            y = dt_verdict.year
            if y < 2017:
                issues.append(f"Pre-Civil Code 2015 era judgment (year {y} < 2017)")
            elif split == "train" and y > 2022:
                issues.append(f"TEMPORAL LEAKAGE: Train split contains verdict year {y} > 2022")
            elif split == "val" and y != 2023:
                issues.append(f"TEMPORAL LEAKAGE: Val split contains verdict year {y} != 2023")
            elif split == "test" and y < 2024:
                issues.append(f"TEMPORAL LEAKAGE: Test split contains verdict year {y} < 2024")

        is_valid = len(issues) == 0
        return is_valid, issues

    @staticmethod
    def calculate_cohens_kappa(rater1: List[Any], rater2: List[Any]) -> float:
        """Computes Cohen's Kappa coefficient between two label sequences."""
        assert len(rater1) == len(rater2), "Label sequences must have identical length"
        n = len(rater1)
        if n == 0:
            return 1.0

        categories = sorted(list(set(rater1).union(set(rater2))))
        cat_to_idx = {c: i for i, c in enumerate(categories)}
        k = len(categories)
        
        matrix = [[0] * k for _ in range(k)]
        for r1, r2 in zip(rater1, rater2):
            matrix[cat_to_idx[r1]][cat_to_idx[r2]] += 1
            
        po = sum(matrix[i][i] for i in range(k)) / n
        
        pe = 0.0
        for i in range(k):
            row_sum = sum(matrix[i][j] for j in range(k))
            col_sum = sum(matrix[j][i] for j in range(k))
            pe += (row_sum * col_sum) / (n * n)

        if pe == 1.0:
            return 1.0
        kappa = (po - pe) / (1.0 - pe)
        return round(kappa, 4)

if __name__ == "__main__":
    verifier = SelfVerifier()
    
    # Test 1: Perfectly valid case
    valid_case = {
        "case_id": "01/2024/DS-ST",
        "plaintiff": "Nguyễn Văn A",
        "defendant": "Trần Thị B",
        "earliest_deposit_date": "2023-01-10",
        "breach_date": "2023-02-15",
        "filing_date": "2024-01-20",
        "verdict_date": "2024-05-15",
        "temporal_split": "test",
        "is_statute_lapsed": False
    }
    ok, issues = verifier.verify_case_graph(valid_case)
    print(f"Test 1 Valid Case -> Status: {'PASSED' if ok else 'FAILED'}, Issues: {issues}")

    # Test 2: Anomaly case (Temporal Leakage + Role collision)
    invalid_case = {
        "case_id": "02/2021/DS-ST",
        "plaintiff": "Lê Văn C",
        "defendant": "Lê Văn C",
        "earliest_deposit_date": "2023-01-10",
        "breach_date": "2021-02-15",
        "filing_date": "2024-01-20",
        "verdict_date": "2025-05-15",
        "temporal_split": "train",
        "is_statute_lapsed": False
    }
    ok2, issues2 = verifier.verify_case_graph(invalid_case)
    print(f"Test 2 Anomaly Case -> Status: {'PASSED' if ok2 else 'DETECTED ANOMALIES'}, Issues count: {len(issues2)}")
    for iss in issues2:
        print(f"   ! {iss}")

    # Test 3: Cohen's Kappa verification
    labels_gold = ["ACCEPT_DOUBLE_DEPOSIT_REFUND", "DISMISS_STATUTE_LAPSED", "ACCEPT_DEPOSIT_FORFEITURE", "ACCEPT_DOUBLE_DEPOSIT_REFUND"] * 25
    labels_pred = ["ACCEPT_DOUBLE_DEPOSIT_REFUND", "DISMISS_STATUTE_LAPSED", "ACCEPT_DEPOSIT_FORFEITURE", "ACCEPT_DOUBLE_DEPOSIT_REFUND"] * 24 + ["ACCEPT_DOUBLE_DEPOSIT_REFUND", "DISMISS_STATUTE_LAPSED", "ACCEPT_DEPOSIT_FORFEITURE", "DISMISS_STATUTE_LAPSED"]
    kappa = verifier.calculate_cohens_kappa(labels_gold, labels_pred)
    print(f"[GROUND TRUTH / FACT] Cohen's Kappa score test: kappa = {kappa} (>= 0.85: {kappa >= 0.85})")
