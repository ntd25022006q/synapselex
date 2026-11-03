"""
SynapseLex: Chrono-Chunking Engine for Long Vietnamese Civil Judgments
Segments long legal narratives (15-30 pages) into coherent temporal episode chunks
anchored on Vietnamese statutory time expressions without fragmenting causal relationships.

Authors: Nguyễn Tiến Đạt (datbazuka2502) & Antigravity Research Agent
Paper Reference: H-LETE (Hierarchical Legal-Event Temporal Extraction)
"""

import sys
import os
import re
from typing import List, Dict, Any, Tuple

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Comprehensive regex patterns for Vietnamese legal temporal expressions
TEMPORAL_PATTERNS = [
    # Explicit full date: "ngày 15 tháng 03 năm 2021" or "ngày 15/03/2021"
    r'(?:vào\s+)?ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
    r'(?:vào\s+)?ngày\s+(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})',
    # Month/Year anchor: "tháng 05 năm 2022"
    r'(?:trong\s+)?tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
    # Year anchor: "năm 2021"
    r'(?:trong\s+|vào\s+)?năm\s+(20[0-2][0-9])',
    # Statutory relative period: "sau 30 ngày kể từ..."
    r'(?:sau|trong\s+thời\s+hạn)\s+(\d+)\s*(ngày|tháng|năm)\s*(?:kể\s+từ)?',
    # Procedural milestone anchors
    r'(?:Tại\s+phiên\s+tòa|Tại\s+đơn\s+khởi\s+kiện\s+ngày|Ngày\s+thụ\s+lý\s+vụ\s+án|Quá\s+trình\s+giải\s+quyết)',
]

COMBINED_TEMP_REGEX = re.compile('|'.join(f'(?:{p})' for p in TEMPORAL_PATTERNS), re.IGNORECASE)

class ChronoChunker:
    def __init__(self, max_chunk_chars: int = 1500, min_chunk_chars: int = 200):
        self.max_chunk_chars = max_chunk_chars
        self.min_chunk_chars = min_chunk_chars

    def extract_temporal_anchors(self, text: str) -> List[Tuple[int, int, str]]:
        """Finds all temporal anchors with character spans."""
        anchors = []
        for match in COMBINED_TEMP_REGEX.finditer(text):
            anchors.append((match.start(), match.end(), match.group(0)))
        return anchors

    def segment_into_chrono_chunks(self, full_text: str, case_id: str = "") -> List[Dict[str, Any]]:
        """
        Segments a multi-page judgment into temporal narrative chunks.
        Each chunk is anchored to a specific legal milestone date.
        """
        if not full_text or len(full_text.strip()) == 0:
            return []

        anchors = self.extract_temporal_anchors(full_text)
        if not anchors:
            # Fallback: slice into default size chunks if no dates found
            return [{
                "chunk_id": f"{case_id}_c0",
                "anchor_text": "Không xác định ngày",
                "text": full_text[:self.max_chunk_chars],
                "char_span": [0, min(len(full_text), self.max_chunk_chars)]
            }]

        chunks = []
        n_anchors = len(anchors)
        
        for idx in range(n_anchors):
            start_pos, end_pos, anchor_str = anchors[idx]
            
            # Find chunk start: either start of text or halfway between prev anchor
            if idx == 0:
                chunk_start = 0
            else:
                prev_end = anchors[idx - 1][1]
                # Look for sentence boundary between prev_end and start_pos
                sub = full_text[prev_end:start_pos]
                dot_idx = sub.rfind('.')
                if dot_idx != -1:
                    chunk_start = prev_end + dot_idx + 1
                else:
                    chunk_start = prev_end

            # Find chunk end: before next anchor or end of text
            if idx == n_anchors - 1:
                chunk_end = len(full_text)
            else:
                next_start = anchors[idx + 1][0]
                sub = full_text[end_pos:next_start]
                dot_idx = sub.rfind('.')
                if dot_idx != -1 and (end_pos + dot_idx) - chunk_start >= self.min_chunk_chars:
                    chunk_end = end_pos + dot_idx + 1
                else:
                    chunk_end = next_start

            chunk_text = full_text[chunk_start:chunk_end].strip()
            
            # Limit chunk length if too huge
            if len(chunk_text) > self.max_chunk_chars:
                chunk_text = chunk_text[:self.max_chunk_chars]
                chunk_end = chunk_start + len(chunk_text)

            if len(chunk_text) >= 50:
                chunks.append({
                    "chunk_id": f"{case_id}_c{idx:02d}",
                    "anchor_text": anchor_str,
                    "anchor_span": [start_pos, end_pos],
                    "chunk_span": [chunk_start, chunk_end],
                    "text": chunk_text
                })

        return chunks

if __name__ == "__main__":
    sample_text = (
        "Ngày 15/03/2021, ông Nguyễn Văn A và bà Trần Thị B ký hợp đồng đặt cọc số tiền 500.000.000 đồng "
        "để bảo đảm nhận chuyển nhượng thửa đất số 12, tờ bản đồ số 4 tại xã X, huyện Y. "
        "Hai bên thỏa thuận đến ngày 15/04/2021 sẽ ra văn phòng công chứng ký hợp đồng chuyển nhượng chính thức. "
        "Tuy nhiên đến ngày 15/04/2021, bà B không đến văn phòng công chứng và sau đó đem thửa đất chuyển nhượng cho người khác. "
        "Ngày 10/05/2024, ông A nộp đơn khởi kiện yêu cầu bà B phạt cọc gấp đôi số tiền 1.000.000.000 đồng."
    )
    chunker = ChronoChunker()
    res = chunker.segment_into_chrono_chunks(sample_text, case_id="CASE_TEST_01")
    print(f"Generated {len(res)} Chrono-Chunks:")
    for c in res:
        print(f"  [{c['chunk_id']}] Anchor: '{c['anchor_text']}' -> {c['text'][:80]}...")
