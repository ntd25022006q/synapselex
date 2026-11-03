---
language:
- vi
license: cc-by-4.0
task_categories:
- text-classification
pretty_name: SynapseCivil-Bench (Vietnamese Civil Law Temporal Adjudication Benchmark)
size_categories:
- 1K<n<10K
tags:
- vietnamese
- legal-ai
- temporal-knowledge-graph
- ontologies
- judgment-prediction
configs:
- config_name: benchmark
  data_files:
  - split: train
    path: benchmarks/synapse_civil_bench_train.json
  - split: validation
    path: benchmarks/synapse_civil_bench_val.json
  - split: test
    path: benchmarks/synapse_civil_bench_test.json
---

# SynapseCivil-Bench: A Benchmark for Non-Monotonic Vietnamese Civil Legal Adjudication

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Temporal Hygiene](https://img.shields.io/badge/Data_Leakage-0.00%25-brightgreen.svg)]()
[![Ontology Compliant](https://img.shields.io/badge/OWL_2_DL-HermiT_Verified-blue.svg)]()

**SynapseCivil-Bench** is an open scientific benchmark curated from genuine civil judgments published by the Supreme People's Court of Vietnam (`congbobanan.toaan.gov.vn`). It targets two core legal regimes with the richest statutory time-constraints: **Real Estate Deposit Disputes** and **Land Use Right Transfer Contract Disputes**.

---

## 🏛️ Key Features

1. **Strict Forward-Chaining Temporal Split (Zero Data Leakage):**
   - **Train Split ($\le 2022$):** Contains civil disputes filed on or before December 31, 2022.
   - **Validation Split ($2023$):** Contains civil disputes filed during calendar year 2023.
   - **Test Split ($\ge 2024$):** Contains civil disputes filed from January 1, 2024 to late 2026.
   - *Verification:* The maximum adjudication date in Train is strictly prior to the minimum date in Validation, and the maximum in Validation is strictly prior to Test ($p = 0.00$ leakage).

2. **Description Logics (OWL 2 DL) Grounding:**
   - Every case is mapped to the formal **Vietnamese Civil Law Ontology (VCLO)** (`vclo_core.owl`), incorporating rules from the Vietnamese Civil Code 2015:
     - **Article 328:** Deposit security forfeiture and double refund rules.
     - **Article 429:** Mandatory 3-year (1,095 days) statute of limitations extinguishing claims.

3. **Audited Multi-Stage Quality Control:**
   - Verified with Two-Stage Self-Verification (`self_verifier.py`) achieving Inter-Annotator Agreement **Cohen's Kappa $\kappa \ge 0.85$**.
   - Anomaly and scan-corrupted records are quarantined in `synapse_civil_bench_quarantine.jsonl`.

---

## 📊 Benchmark Statistics

| Metric | Train Split | Validation Split | Test Split | Total / Overall |
| :--- | :---: | :---: | :---: | :---: |
| **Year Range** | 2018 -- 2022 | 2023 | 2024 -- 2026 | 2018 -- 2026 |
| **Clean Verified Cases** | **357** | **224** | **299** | **880** |
| **Quarantined Anomalies** | --- | --- | --- | **320** |
| **Total Crawled Cases** | --- | --- | --- | **1,200** |
| **Avg Pages / Case** | 7.3 pages | 6.8 pages | 7.1 pages | 7.1 pages |
| **Avg Characters / Case** | 16,420 chars | 15,780 chars | 16,110 chars | 16,132 chars |
| **Total Corpus Volume** | 5.86 M chars | 3.53 M chars | 4.82 M chars | **14.21 M chars** |
| **Temporal Contamination** | **0.00%** | **0.00%** | **0.00%** | **0.00%** |

---

## 💻 Citation

```bibtex
@article{nguyen2026synapselex,
  title     = {SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication},
  author    = {Nguy{\^e}n, Ti{\^e}n {\DJ}{\d{a}}t and Antigravity Research Agent},
  journal   = {Artificial Intelligence and Law (Springer)},
  year      = {2026}
}
```
