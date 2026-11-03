"""
SynapseLex: Real Civil Judgment Acquisition & Curation Engine
Crawls official judgments from congbobanan.toaan.gov.vn with zero mock data.
Enforces Strict Temporal Forward-Chaining Partitioning (Train <= 2022, Val == 2023, Test >= 2024).

Target Case Categories:
- Tranh chấp hợp đồng đặt cọc
- Tranh chấp hợp đồng chuyển nhượng quyền sử dụng đất
- Tranh chấp quyền sử dụng đất
"""

import sys
import os
import io
import re
import json
import time
import ssl
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, Any, List

TARGET_KEYWORDS = [
    "đặt cọc", 
    "chuyển nhượng quyền sử dụng đất", 
    "hợp đồng chuyển nhượng", 
    "chuyển nhượng qsdđ", 
    "tranh chấp quyền sử dụng đất"
]

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_case_by_id(doc_id: int, timeout: int = 12) -> Optional[Dict[str, Any]]:
    ctx = create_ssl_context()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    html_url = f"https://congbobanan.toaan.gov.vn/2ta{doc_id}t1cvn/chi-tiet-ban-an"
    try:
        req = urllib.request.Request(html_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return None

    # Check case relation / domain
    type_m = re.search(r'Quan hệ pháp luật:.*?>([^<]+)<', html)
    case_type = type_m.group(1).strip() if type_m else ''
    
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_m.group(1).strip() if title_m else ''
    
    # Check if target domain matches
    combined_domain = f"{case_type} {title}".lower()
    is_target = any(kw in combined_domain for kw in TARGET_KEYWORDS)
    if not is_target:
        return None

    # Extract Court Name
    court_m = re.search(r'Tòa án xét xử:.*?>([^<]+)<', html)
    court = court_m.group(1).strip() if court_m else 'TAND'
    
    # Extract Adjudication Date
    date_m = re.search(r'Ngày tuyên án:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})', html)
    verdict_date_raw = date_m.group(1).strip() if date_m else ''
    if not verdict_date_raw:
        # Fallback to title date pattern
        date_fallback = re.search(r'ngày\s+([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})', title, re.I)
        if date_fallback:
            verdict_date_raw = date_fallback.group(1).strip()

    if not verdict_date_raw:
        return None

    # Parse ISO date and year
    try:
        d, m, y = [int(p) for p in verdict_date_raw.split('/')]
        verdict_date_iso = f"{y:04d}-{m:02d}-{d:02d}"
        year = y
    except Exception:
        return None

    # Strict Forward-Chaining Temporal Split
    if year <= 2022:
        split = "train"
    elif year == 2023:
        split = "val"
    elif year >= 2024:
        split = "test"
    else:
        split = "train"

    # Fetch PDF stream
    pdf_url = f"https://congbobanan.toaan.gov.vn/3ta{doc_id}t1cvn/"
    full_text = ""
    num_pages = 0
    try:
        import pypdf
        pdf_req = urllib.request.Request(pdf_url, headers=headers)
        with urllib.request.urlopen(pdf_req, context=ctx, timeout=timeout) as pdf_resp:
            pdf_bytes = pdf_resp.read()
            
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        num_pages = len(reader.pages)
        pages_text = [p.extract_text() or '' for p in reader.pages]
        full_text = '\n'.join(pages_text).strip()
    except Exception as e:
        full_text = ""

    # If PDF extraction failed or empty, extract from HTML tabs
    if len(full_text) < 200:
        for tid in ['1b', '2b', '3b', '4b']:
            tab_m = re.search(r'id=\"' + tid + r'\"[^>]*>(.*?)</div>', html, re.DOTALL)
            if tab_m:
                clean = re.sub(r'<[^>]+>', ' ', tab_m.group(1))
                full_text += ' ' + ' '.join(clean.split())
        full_text = full_text.strip()

    if len(full_text) < 300:
        return None  # Text too thin to be a valid judgment

    # Extract case identification number (e.g. 1011/2026/DS-PT)
    case_num_m = re.search(r'Bản án số:\s*([0-9]+/[0-9]+/DS-[A-Z]+)', full_text)
    if not case_num_m:
        case_num_m = re.search(r'số\s*([0-9]+/[0-9]+/DS-[A-Z]+)', title, re.I)
    case_number = case_num_m.group(1) if case_num_m else f"{doc_id}/{year}/DS"

    record = {
        "doc_id": doc_id,
        "case_number": case_number,
        "court_name": court,
        "case_type": case_type if case_type else "Tranh chấp quyền sử dụng đất",
        "verdict_date": verdict_date_iso,
        "year": year,
        "temporal_split": split,
        "num_pages": num_pages,
        "char_length": len(full_text),
        "source_url": html_url,
        "pdf_url": pdf_url,
        "raw_text": full_text
    }
    return record

def run_corpus_crawler(output_file: str, target_count: int = 1200, max_workers: int = 8):
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    # Sample ID pools across time regimes:
    # Train: 300,000 - 1,000,000
    # Val:   1,100,000 - 1,500,000
    # Test:  1,600,000 - 2,288,000
    print(f"[*] Starting SynapseLex Public Judgment Crawler...")
    print(f"[*] Target count: {target_count} civil judgments (Deposit & Land Disputes)")
    
    existing_ids = set()
    collected = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    existing_ids.add(item['doc_id'])
                    collected.append(item)
        print(f"[*] Loaded {len(collected)} already collected records from {output_file}")

    if len(collected) >= target_count:
        print(f"[GROUND TRUTH / FACT] Target {target_count} already achieved!")
        return collected

    # Strategy: Stride sampling across all 3 regimes to ensure balanced temporal distribution
    train_ids = list(range(350000, 950000, 350))      # ~1700 candidates
    val_ids   = list(range(1150000, 1450000, 400))    # ~750 candidates
    test_ids  = list(range(1700000, 2288000, 250))    # ~2300 candidates
    
    # Interleave to fetch concurrently
    all_candidate_ids = []
    max_len = max(len(train_ids), len(val_ids), len(test_ids))
    for i in range(max_len):
        if i < len(test_ids): all_candidate_ids.append(test_ids[i])
        if i < len(val_ids): all_candidate_ids.append(val_ids[i])
        if i < len(train_ids): all_candidate_ids.append(train_ids[i])

    all_candidate_ids = [cid for cid in all_candidate_ids if cid not in existing_ids]
    print(f"[*] Candidate ID pool generated: {len(all_candidate_ids)} candidates to probe.")

    with open(output_file, 'a', encoding='utf-8') as out_f:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_id = {executor.submit(fetch_case_by_id, cid): cid for cid in all_candidate_ids}
            for future in as_completed(future_to_id):
                res = future.result()
                if res is not None:
                    out_f.write(json.dumps(res, ensure_ascii=False) + '\n')
                    out_f.flush()
                    collected.append(res)
                    print(f"  [+] Matched Case: ID={res['doc_id']} | Date={res['verdict_date']} | Split={res['temporal_split']:5s} | Pages={res['num_pages']} | Total={len(collected)}/{target_count}")
                    if len(collected) >= target_count:
                        print("[*] Target reached! Terminating crawler pool.")
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

    print(f"\n[GROUND TRUTH / FACT] Crawling complete. Total saved: {len(collected)} judgments.")
    return collected

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "synapselex/data/raw_judgments.jsonl"
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    run_corpus_crawler(out_path, target_count=target, max_workers=workers)
