"""
SynapseLex: Unified Legal Data Schema & Annotations Specification
Enforces Zero Temporal Leakage, Strict Type Safety, and Provenance Tracking.

Standard: Python Dataclasses / Pydantic V2 Compatible
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import date

class ProceduralRole(str, Enum):
    PLAINTIFF = "PLAINTIFF"           # Nguyên đơn
    DEFENDANT = "DEFENDANT"           # Bị đơn
    INTERVENER = "INTERVENER"         # Người có quyền lợi nghĩa vụ liên quan
    JUDICIAL_ORGAN = "JUDICIAL_ORGAN" # Tòa án / Viện kiểm sát

class LegalStateEnum(str, Enum):
    VALID = "Valid"
    VOIDABLE = "Voidable"
    VOID_AB_INITIO = "Void_Ab_Initio"
    EXTINGUISHED = "Extinguished"

class VerdictCategory(str, Enum):
    ACCEPT_DEPOSIT_FORFEITURE = "ACCEPT_DEPOSIT_FORFEITURE"       # Chấp nhận phạt cọc (bên đặt cọc mất cọc)
    ACCEPT_DOUBLE_DEPOSIT_REFUND = "ACCEPT_DOUBLE_DEPOSIT_REFUND" # Phạt cọc gấp đôi (bên nhận cọc trả lại cọc + bồi thường)
    DISMISS_STATUTE_LAPSED = "DISMISS_STATUTE_LAPSED"             # Đình chỉ/Bác đơn do hết thời hiệu khởi kiện (Đ.429)
    DECLARE_CONTRACT_VOID = "DECLARE_CONTRACT_VOID"               # Tuyên hợp đồng vô hiệu, trả lại hiện trạng ban đầu
    DISMISS_UNFOUNDED_CLAIM = "DISMISS_UNFOUNDED_CLAIM"           # Bác yêu cầu khởi kiện do không có căn cứ thực tế

class TemporalSplit(str, Enum):
    TRAIN = "train"           # Case filing <= 2022-12-31
    VALIDATION = "val"        # Case filing between 2023-01-01 and 2023-12-31
    TEST = "test"             # Case filing >= 2024-01-01 (Strict Future Testing)

@dataclass
class TemporalEvent:
    event_id: str
    event_type: str                   # e.g., 'contract_signing', 'deposit_payment', 'breach_event', 'filing'
    subject_entity: str
    subject_role: ProceduralRole
    predicate: str                    # TBox relation (e.g. 'securesObligation', 'violatesObligation')
    object_entity: str
    timestamp_raw: str                # e.g., 'ngày 12 tháng 04 năm 2021'
    timestamp_iso: str                # '2021-04-12'
    duration_days: Optional[int] = None
    resulting_legal_state: LegalStateEnum = LegalStateEnum.VALID
    statutory_governance: List[str] = field(default_factory=list)

@dataclass
class JudgmentCase:
    case_id: str                      # e.g., '35/2022/DS-ST'
    court_name: str                   # e.g., 'TAND huyện Thới Lai, TP Cần Thơ'
    filing_date: str                  # ISO date: '2022-03-15'
    verdict_date: str                 # ISO date: '2022-09-20'
    case_type: str                    # 'deposit_contract_dispute' or 'land_transfer_dispute'
    dispute_summary: str              # Objective factual summary
    facts_timeline: List[TemporalEvent] = field(default_factory=list)
    ground_truth_verdict: VerdictCategory = VerdictCategory.ACCEPT_DEPOSIT_FORFEITURE
    cited_articles: List[str] = field(default_factory=list)
    temporal_split: TemporalSplit = TemporalSplit.TRAIN
    elapsed_days_to_filing: int = 0
    is_statute_of_limitations_lapsed: bool = False
    anonymized: bool = True
    provenance_url: str = ""

    def validate_temporal_split(self) -> bool:
        """Enforces strictly zero temporal leakage between splits."""
        year = int(self.filing_date.split("-")[0])
        if self.temporal_split == TemporalSplit.TRAIN:
            assert year <= 2022, f"Temporal leak: Train case {self.case_id} filed in {year} > 2022"
        elif self.temporal_split == TemporalSplit.VALIDATION:
            assert year == 2023, f"Validation case {self.case_id} filed in {year} != 2023"
        elif self.temporal_split == TemporalSplit.TEST:
            assert year >= 2024, f"Temporal leak: Test case {self.case_id} filed in {year} < 2024"
        return True
