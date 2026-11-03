"""
SynapseLex: Hierarchical Legal-Event Temporal Extractor (H-LETE)
Combines Chrono-Chunking with GPT-NER @@Entity [Role]## notation and VCLO TBox grounding.

Authors: Nguyễn Tiến Đạt (datbazuka2502) & Antigravity Research Agent
Standard: Non-Monotonic Legal Temporal Knowledge Graph Construction
"""

import sys
import os
import re
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from synapselex.src.extraction.chrono_chunker import ChronoChunker

ROLE_PATTERNS = {
    "PLAINTIFF": [
        r'(?:nguyên\s+đơn|người\s+khởi\s+kiện)[\s:]+(?:ông|bà|cụ|anh|chị)?\s*([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+(?:\s+[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+){1,4})',
        r'(?:ông|bà|anh|chị)\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+(?:\s+[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+){1,4})\s+khởi\s+kiện',
    ],
    "DEFENDANT": [
        r'(?:bị\s+đơn|người\s+bị\s+kiện)[\s:]+(?:ông|bà|cụ|anh|chị)?\s*([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+(?:\s+[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+){1,4})',
        r'kiện\s+(?:ông|bà|anh|chị)\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+(?:\s+[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zđáàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+){1,4})',
    ],
    "DEPOSIT_AMOUNT": [
        r'(?:đặt\s+cọc\s+(?:số\s+tiền\s+)?|tiền\s+cọc\s+là\s+)([0-9\.\,]+)\s*(?:đồng|triệu|tỷ)',
    ]
}

def parse_vietnamese_date(text: str) -> Optional[str]:
    """Converts Vietnamese date strings to ISO YYYY-MM-DD safely."""
    m = re.search(r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})', text, re.I)
    if m:
        try:
            d, month, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return date(y, month, d).isoformat()
        except (ValueError, OverflowError):
            pass
    
    m2 = re.search(r'ngày\s+(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})', text, re.I)
    if m2:
        try:
            d, month, y = int(m2.group(1)), int(m2.group(2)), int(m2.group(3))
            return date(y, month, d).isoformat()
        except (ValueError, OverflowError):
            pass
    return None

class HLEExtractor:
    def __init__(self):
        self.chunker = ChronoChunker()

    def extract_case_entities(self, full_text: str) -> Dict[str, str]:
        """Extracts primary parties and their roles."""
        entities = {}
        for role, patterns in ROLE_PATTERNS.items():
            for pat in patterns:
                m = re.search(pat, full_text, re.I)
                if m:
                    val = m.group(1).strip()
                    # Clean punctuation
                    val = re.sub(r'[\,\;\:\.]+$', '', val).strip()
                    if len(val) >= 2 and val not in entities.values():
                        entities[role] = val
                        break
        return entities

    def extract_temporal_state_graph(self, case_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Builds the 5-tuple temporal state graph from raw judgment text:
        (s, r, o, [t_start, t_end], S) where S in {Valid, Voidable, Void_Ab_Initio, Extinguished}
        """
        full_text = case_record.get("raw_text", "")
        case_id = case_record.get("case_number", f"DOC_{case_record.get('doc_id')}")
        chunks = self.chunker.segment_into_chrono_chunks(full_text, case_id=case_id)
        
        entities = self.extract_case_entities(full_text)
        plaintiff = entities.get("PLAINTIFF", "Nguyên đơn")
        defendant = entities.get("DEFENDANT", "Bị đơn")
        
        events = []
        earliest_deposit_date = None
        breach_date = None
        filing_date = None
        
        for c in chunks:
            c_text = c["text"]
            iso_d = parse_vietnamese_date(c["anchor_text"]) or parse_vietnamese_date(c_text)
            
            # Detect contract signing or deposit payment
            if any(k in c_text.lower() for k in ["đặt cọc", "ký hợp đồng", "giao nhận tiền cọc"]):
                if iso_d and not earliest_deposit_date:
                    earliest_deposit_date = iso_d
                events.append({
                    "event_type": "deposit_contract_signing",
                    "subject": f"@@{plaintiff} [Plaintiff]##",
                    "predicate": "securesObligation",
                    "object": f"@@{defendant} [Defendant]##",
                    "timestamp": iso_d,
                    "state": "Valid",
                    "text_evidence": c_text[:120]
                })
            
            # Detect contractual breach
            elif any(k in c_text.lower() for k in ["không đến", "không thực hiện", "vi phạm", "chuyển nhượng cho người khác", "bán cho người khác"]):
                if iso_d and not breach_date:
                    breach_date = iso_d
                events.append({
                    "event_type": "contractual_breach",
                    "subject": f"@@{defendant} [Defendant]##",
                    "predicate": "violatesObligation",
                    "object": "Hợp đồng đặt cọc",
                    "timestamp": iso_d,
                    "state": "Voidable",
                    "text_evidence": c_text[:120]
                })

            # Detect lawsuit filing
            elif any(k in c_text.lower() for k in ["khởi kiện", "nộp đơn", "thụ lý vụ án", "yêu cầu tòa án"]):
                if iso_d and not filing_date:
                    filing_date = iso_d
                events.append({
                    "event_type": "lawsuit_filing",
                    "subject": f"@@{plaintiff} [Plaintiff]##",
                    "predicate": "initiatesDispute",
                    "object": "Tòa án nhân dân",
                    "timestamp": iso_d,
                    "state": "Valid",
                    "text_evidence": c_text[:120]
                })

        # Calculate statute of limitations lapse (Article 429 BLDS 2015: 1095 days)
        elapsed_days = 0
        statute_lapsed = False
        final_state = "Valid"
        
        if breach_date and filing_date:
            try:
                d_breach = datetime.strptime(breach_date, "%Y-%m-%d")
                d_filing = datetime.strptime(filing_date, "%Y-%m-%d")
                elapsed_days = (d_filing - d_breach).days
                if elapsed_days > 1095:
                    statute_lapsed = True
                    final_state = "Extinguished"
            except Exception:
                pass

        # Ground Truth Verdict attribution
        verdict_text = full_text[-3000:] if len(full_text) > 3000 else full_text
        if statute_lapsed and any(k in verdict_text.lower() for k in ["hết thời hiệu", "đình chỉ", "bác yêu cầu"]):
            verdict = "DISMISS_STATUTE_LAPSED"
            final_state = "Extinguished"
        elif any(k in verdict_text.lower() for k in ["phạt cọc gấp đôi", "trả lại tiền cọc và bồi thường", "chấp nhận yêu cầu khởi kiện"]):
            verdict = "ACCEPT_DOUBLE_DEPOSIT_REFUND"
        elif any(k in verdict_text.lower() for k in ["mất tiền cọc", "bác yêu cầu của nguyên đơn", "không chấp nhận yêu cầu đòi lại tiền cọc"]):
            verdict = "ACCEPT_DEPOSIT_FORFEITURE"
        elif any(k in verdict_text.lower() for k in ["vô hiệu", "tuyên bố hợp đồng vô hiệu"]):
            verdict = "DECLARE_CONTRACT_VOID"
            final_state = "Void_Ab_Initio"
        else:
            verdict = "ACCEPT_DEPOSIT_FORFEITURE"

        return {
            "case_id": case_id,
            "doc_id": case_record.get("doc_id"),
            "court_name": case_record.get("court_name", ""),
            "verdict_date": case_record.get("verdict_date", ""),
            "temporal_split": case_record.get("temporal_split", "train"),
            "plaintiff": plaintiff,
            "defendant": defendant,
            "earliest_deposit_date": earliest_deposit_date,
            "breach_date": breach_date,
            "filing_date": filing_date,
            "elapsed_days_breach_to_filing": elapsed_days,
            "is_statute_lapsed": statute_lapsed,
            "final_state": final_state,
            "ground_truth_verdict": verdict,
            "temporal_events": events,
            "num_chrono_chunks": len(chunks)
        }

if __name__ == "__main__":
    sample_case = {
        "doc_id": 999999,
        "case_number": "12/2024/DS-ST",
        "court_name": "TAND thành phố Thủ Đức",
        "verdict_date": "2024-06-15",
        "temporal_split": "test",
        "raw_text": (
            "Nguyên đơn: ông Nguyễn Văn A. Bị đơn: bà Trần Thị B. "
            "Ngày 15/03/2021, ông A và bà B ký hợp đồng đặt cọc số tiền 500.000.000 đồng để chuyển nhượng đất. "
            "Ngày 15/04/2021, bà B vi phạm nghĩa vụ, không đến công chứng và bán đất cho người khác. "
            "Ngày 20/05/2024, ông A nộp đơn khởi kiện yêu cầu bà B phạt cọc gấp đôi. "
            "Hội đồng xét xử nhận định: Kể từ ngày vi phạm 15/04/2021 đến ngày khởi kiện 20/05/2024 đã quá 03 năm. "
            "Căn cứ Điều 429 Bộ luật Dân sự 2015, thời hiệu khởi kiện đã hết. Quyết định: Đình chỉ giải quyết vụ án do hết thời hiệu khởi kiện."
        )
    }
    extractor = HLEExtractor()
    graph = extractor.extract_temporal_state_graph(sample_case)
    print("[GROUND TRUTH / FACT] Extracted SynapseLex Case Graph:")
    for k, v in graph.items():
        if k != "temporal_events":
            print(f"  • {k:30s}: {v}")
    print(f"  • Total Events Extracted: {len(graph['temporal_events'])}")
