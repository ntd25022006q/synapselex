"""
SynapseLex: Dynamic Legal Graph Subgraph Constructor
Transforms extracted case episodes into PyTorch-ready Temporal Knowledge Graphs.

Each case is modeled as a heterogeneous dynamic graph G = (V, E, T):
- Nodes V: Litigants (Plaintiff, Defendant, Intervener), Contracts, Real Estate Assets, Events.
- Edges E: Multi-relational typed edges (participated_in, affected_contract, precedes).
- Timestamps T: Continuous event timestamps and edge relative latencies.

Standard: Q1 AI & Law Empirical Formulation (Zero Target Leakage)
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
import torch

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Entity Types
NODE_TYPE_MAP = {
    "PLAINTIFF": 0,
    "DEFENDANT": 1,
    "THIRD_PARTY": 2,
    "DEPOSIT_CONTRACT": 3,
    "LAND_PARCEL": 4,
    "EVENT_SIGNING": 5,
    "EVENT_PAYMENT": 6,
    "EVENT_BREACH": 7,
    "EVENT_NOTICE": 8,
    "EVENT_FILING": 9
}

# Relation Types
RELATION_MAP = {
    "OBLIGEE_OF": 0,          # Plaintiff -> Contract
    "OBLIGOR_OF": 1,          # Defendant -> Contract
    "SUBJECT_MATTER": 2,      # LandParcel -> Contract
    "PARTICIPATED_IN": 3,     # Party -> Event
    "AFFECTS_CONTRACT": 4,    # Event -> Contract
    "TEMPORALLY_PRECEDES": 5, # Event_i -> Event_{i+1}
    "REVERSED_EDGE": 6        # Bidirectional flow
}

STATE_MAP = {
    "Valid": 0,
    "Voidable": 1,
    "Void_Ab_Initio": 2,
    "Extinguished": 3
}

VERDICT_MAP = {
    "ACCEPT_DEPOSIT_FORFEITURE": 0,
    "ACCEPT_DOUBLE_DEPOSIT_REFUND": 1,
    "DISMISS_STATUTE_LAPSED": 2,
    "DECLARE_CONTRACT_VOID": 3
}

def parse_iso_date(d_str: Optional[str]) -> Optional[datetime]:
    if not d_str:
        return None
    try:
        return datetime.strptime(d_str, "%Y-%m-%d")
    except Exception:
        return None

class LegalGraphBuilder:
    def __init__(self, feature_dim: int = 32):
        self.feature_dim = feature_dim

    def build_case_graph(self, case_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a single case dict into dynamic graph tensors.
        Strictly contains only observable facts available at dispute inception (NO TARGET LEAKAGE).
        """
        nodes = []
        node_types = []
        node_features = []
        
        # 1. Litigant & Object Nodes
        # Node 0: Plaintiff
        plaintiff_name = case_record.get("plaintiff", "Nguyên đơn")
        nodes.append({"id": "plaintiff", "label": plaintiff_name, "type": "PLAINTIFF"})
        node_types.append(NODE_TYPE_MAP["PLAINTIFF"])
        
        # Node 1: Defendant
        defendant_name = case_record.get("defendant", "Bị đơn")
        nodes.append({"id": "defendant", "label": defendant_name, "type": "DEFENDANT"})
        node_types.append(NODE_TYPE_MAP["DEFENDANT"])
        
        # Node 2: Deposit Contract
        nodes.append({"id": "contract", "label": "Hợp đồng đặt cọc", "type": "DEPOSIT_CONTRACT"})
        node_types.append(NODE_TYPE_MAP["DEPOSIT_CONTRACT"])
        contract_node_idx = 2

        # Node 3: Land Parcel
        nodes.append({"id": "parcel", "label": "Thửa đất chuyển nhượng", "type": "LAND_PARCEL"})
        node_types.append(NODE_TYPE_MAP["LAND_PARCEL"])

        edges = []
        edge_types = []
        edge_times = []

        # Structural edges
        # Plaintiff is obligee of Contract (t=0)
        edges.append((0, contract_node_idx))
        edge_types.append(RELATION_MAP["OBLIGEE_OF"])
        edge_times.append(0.0)

        # Defendant is obligor of Contract (t=0)
        edges.append((1, contract_node_idx))
        edge_types.append(RELATION_MAP["OBLIGOR_OF"])
        edge_times.append(0.0)

        # Land parcel is subject matter of Contract (t=0)
        edges.append((3, contract_node_idx))
        edge_types.append(RELATION_MAP["SUBJECT_MATTER"])
        edge_times.append(0.0)

        # Base reference date (earliest deposit date or 2018-01-01)
        t_ref = parse_iso_date(case_record.get("earliest_deposit_date")) or parse_iso_date("2018-01-01")

        # 2. Event Nodes & Temporal Sequences
        raw_events = case_record.get("temporal_events", [])
        event_node_indices = []

        for e_idx, ev in enumerate(raw_events):
            ev_type_str = ev.get("event_type", "")
            if "signing" in ev_type_str:
                n_type = NODE_TYPE_MAP["EVENT_SIGNING"]
            elif "breach" in ev_type_str:
                n_type = NODE_TYPE_MAP["EVENT_BREACH"]
            elif "filing" in ev_type_str:
                n_type = NODE_TYPE_MAP["EVENT_FILING"]
            elif "notice" in ev_type_str:
                n_type = NODE_TYPE_MAP["EVENT_NOTICE"]
            else:
                n_type = NODE_TYPE_MAP["EVENT_PAYMENT"]

            ev_date = parse_iso_date(ev.get("timestamp")) or t_ref
            elapsed_days = (ev_date - t_ref).days if ev_date and t_ref else 0.0

            curr_node_idx = len(nodes)
            nodes.append({
                "id": f"event_{e_idx}",
                "label": ev_type_str,
                "type": n_type,
                "time_days": elapsed_days
            })
            node_types.append(n_type)
            event_node_indices.append(curr_node_idx)

            # Event affects Contract
            edges.append((curr_node_idx, contract_node_idx))
            edge_types.append(RELATION_MAP["AFFECTS_CONTRACT"])
            edge_times.append(float(elapsed_days))

            # Litigants participate in event
            ev_subj = ev.get("subject", "")
            if (ev_subj == plaintiff_name) or ("Plaintiff" in ev_subj) or ("Nguyên" in ev_subj):
                edges.append((0, curr_node_idx))
                edge_types.append(RELATION_MAP["PARTICIPATED_IN"])
                edge_times.append(float(elapsed_days))
            if (ev_subj == defendant_name) or ("Defendant" in ev_subj) or ("Bị" in ev_subj):
                edges.append((1, curr_node_idx))
                edge_types.append(RELATION_MAP["PARTICIPATED_IN"])
                edge_times.append(float(elapsed_days))

        # Temporal sequence edges between consecutive events
        for i in range(len(event_node_indices) - 1):
            u_ev = event_node_indices[i]
            v_ev = event_node_indices[i + 1]
            dt = nodes[v_ev]["time_days"] - nodes[u_ev]["time_days"]
            edges.append((u_ev, v_ev))
            edge_types.append(RELATION_MAP["TEMPORALLY_PRECEDES"])
            edge_times.append(float(dt))

        # Build reverse edges for bidirectional information flow
        num_forward = len(edges)
        for i in range(num_forward):
            src, tgt = edges[i]
            edges.append((tgt, src))
            edge_types.append(RELATION_MAP["REVERSED_EDGE"])
            edge_times.append(edge_times[i])

        # Node initial feature vectors: one-hot of node type + observable facts
        num_nodes = len(nodes)
        node_feats = torch.zeros(num_nodes, self.feature_dim)
        for i, nt in enumerate(node_types):
            node_feats[i, nt % 10] = 1.0
            if "time_days" in nodes[i]:
                node_feats[i, 23] = float(nodes[i]["time_days"]) / 1000.0

        # Observable legal transaction variables (NO TARGET LEAKAGE / NO SHORTCUTS)
        perf_ratio = float(case_record.get("performed_ratio", 0.25))
        is_notarized = 1.0 if case_record.get("is_notarized", True) else 0.0
        has_fraud = 1.0 if case_record.get("has_fraud", False) else 0.0
        tolling_val = float(case_record.get("tolling_days", 0.0))
        raw_elapsed = float(case_record.get("elapsed_days_breach_to_filing", 0.0))
        eff_elapsed = float(case_record.get("effective_elapsed_days", raw_elapsed - tolling_val))

        # Contract node (idx 2): continuous transaction variables
        node_feats[contract_node_idx, 10] = perf_ratio
        node_feats[contract_node_idx, 11] = is_notarized
        node_feats[contract_node_idx, 12] = has_fraud

        # Breach & Filing events (observable temporal markers)
        for i, nt in enumerate(node_types):
            if nt == NODE_TYPE_MAP["EVENT_BREACH"]:
                node_feats[i, 14] = tolling_val / 365.0
            elif nt == NODE_TYPE_MAP["EVENT_FILING"]:
                node_feats[i, 15] = raw_elapsed / 1000.0
                node_feats[i, 16] = eff_elapsed / 1000.0

        # Litigants (0: Plaintiff, 1: Defendant)
        node_feats[0, 17] = 1.0
        node_feats[1, 18] = 1.0

        # Edge index tensor [2, M]
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        edge_type_tensor = torch.tensor(edge_types, dtype=torch.long)
        edge_time_tensor = torch.tensor(edge_times, dtype=torch.float32)

        # Ground truths
        gt_state_str = case_record.get("final_state", "Valid")
        gt_state = STATE_MAP.get(gt_state_str, 0)
        gt_verdict_str = case_record.get("ground_truth_verdict", "ACCEPT_DEPOSIT_FORFEITURE")
        gt_verdict = VERDICT_MAP.get(gt_verdict_str, 0)

        elapsed_breach_to_filing = eff_elapsed
        is_statute_lapsed = 1.0 if eff_elapsed > 1095.0 else 0.0

        return {
            "case_id": case_record.get("case_id", ""),
            "verdict_date": case_record.get("verdict_date", ""),
            "temporal_split": case_record.get("temporal_split", "train"),
            "num_nodes": num_nodes,
            "num_edges": len(edges),
            "node_types": torch.tensor(node_types, dtype=torch.long),
            "x": node_feats,
            "edge_index": edge_index,
            "edge_types": edge_type_tensor,
            "edge_times": edge_time_tensor,
            "contract_idx": contract_node_idx,
            "elapsed_days": elapsed_breach_to_filing,
            "is_statute_lapsed": is_statute_lapsed,
            "y_state": torch.tensor(gt_state, dtype=torch.long),
            "y_verdict": torch.tensor(gt_verdict, dtype=torch.long)
        }

if __name__ == "__main__":
    builder = LegalGraphBuilder()
    mock_case = {
        "case_id": "TEST_001",
        "plaintiff": "Nguyễn Văn A",
        "defendant": "Trần Thị B",
        "earliest_deposit_date": "2021-01-10",
        "breach_date": "2021-03-15",
        "filing_date": "2024-05-20",
        "elapsed_days_breach_to_filing": 1162,
        "is_statute_lapsed": True,
        "final_state": "Extinguished",
        "ground_truth_verdict": "DISMISS_STATUTE_LAPSED",
        "temporal_events": [
            {"event_type": "contract_signing", "subject": "Nguyễn Văn A", "timestamp": "2021-01-10"},
            {"event_type": "contractual_breach", "subject": "Trần Thị B", "timestamp": "2021-03-15"},
            {"event_type": "lawsuit_filing", "subject": "Nguyễn Văn A", "timestamp": "2024-05-20"}
        ]
    }
    g = builder.build_case_graph(mock_case)
    print(f"[GROUND TRUTH / FACT] Legal Graph Constructed (Target-Leak Free):")
    print(f"  • Nodes: {g['num_nodes']} (Types: {g['node_types'].tolist()})")
    print(f"  • Edges: {g['num_edges']} (Shape: {g['edge_index'].shape})")
    print(f"  • Contract Node Idx: {g['contract_idx']}")
    print(f"  • Verdict Target: {g['y_verdict'].item()} (State Target: {g['y_state'].item()})")
