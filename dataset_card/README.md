---
language:
- vi
license: cc-by-4.0
task_categories:
- text-classification
- tabular-classification
pretty_name: SynapseCivil-Bench (Vietnamese Civil Law Temporal Adjudication Benchmark v2)
size_categories:
- 1K<n<10K
tags:
- vietnamese
- legal-ai
- temporal-knowledge-graph
- ontologies
- judgment-prediction
- non-monotonic-reasoning
- civil-law
configs:
- config_name: default
  data_files:
  - split: train
    path: benchmarks/synapse_civil_bench_train.json
  - split: validation
    path: benchmarks/synapse_civil_bench_val.json
  - split: test
    path: benchmarks/synapse_civil_bench_test.json
  - split: counterfactual
    path: benchmarks/synapse_civil_bench_counterfactual_320.json
---

# SynapseCivil-Bench v2: Multi-Domain Non-Monotonic Civil Adjudication Benchmark

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Temporal Hygiene](https://img.shields.io/badge/Data_Leakage-0.00%25-brightgreen.svg)]()
[![Ontology Compliant](https://img.shields.io/badge/OWL_2_DL-HermiT_Verified-blue.svg)]()
[![Total Cases](https://img.shields.io/badge/Total%20Judgments-2%2C840-indigo.svg)]()
[![Future Test Split](https://img.shields.io/badge/Future%20Test%20Split-920%20cases-orange.svg)]()

**SynapseCivil-Bench v2** is an open, rigorously curated scientific benchmark developed for studying **temporal reasoning, non-monotonic contract state transitions, and normative legal adjudication** under the civil law tradition (specifically the Vietnamese Civil Code 2015 - BLDS 2015, Land Law 2024, and judicial precedents of the Supreme People's Court of Vietnam).

Unlike common-law case databases focused solely on precedents, civil adjudication demands modeling **statutory time bars (statutes of limitations)**, **usury interest rate ceilings**, **formal defect performance curing**, and **force majeure tolling intervals**. SynapseCivil-Bench v2 captures these exact mechanisms across **2,840 genuine multi-domain civil disputes**.

---

## 🏛️ Corpus Structure & Domain Breakdown

The benchmark covers four primary litigation domains in civil court proceedings:

| Domain Identifier | Substantive Civil Dispute Domain | Statutory Articles (BLDS 2015 / Land Law) | Total | Train ($\le 2022$) | Val ($2023$) | Test ($\ge 2024$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `deposit_contract_dispute` | Real Estate Deposit Agreements & Forfeiture | Art. 328, Art. 429 (3-yr statute) | 920 | 473 | 149 | 298 |
| `loan_contract_dispute` | Property Loans, Civil Debt & Usury Capping | Arts. 463–471, Art. 468 cap (20%/yr) | 760 | 391 | 123 | 246 |
| `land_transfer_dispute` | Land Use Rights Transfer & Form Defect Curing | Land Law 2024, Art. 129 (2/3 curing) | 680 | 350 | 110 | 220 |
| `lease_service_dispute` | Commercial Leases & COVID-19 Force Majeure | Arts. 472–482, Art. 156 (Tolling) | 480 | 246 | 78 | 156 |
| **Total Benchmark** | **All 4 Multi-Domain Litigation Regimes** | **BLDS 2015, Land Law 2024** | **2,840** | **1,460** | **460** | **920** |

In addition to the primary splits, the corpus provides a **Counterfactual Stress Suite (320 paired cases)** to empirically test algorithmic sensitivity when perturbing breach elapsed time past 1,095 days, adjusting loan interest across the 20% threshold, or modifying consideration payments across the 2/3 performance boundary.

---

## 🛡️ Forward-Chaining Partition & Anti-Leakage Hygiene

To prevent temporal lookahead contamination, splits are isolated chronologically:
- **Train Split ($\le 2022-12-26$):** 1,460 cases.
- *Temporal Buffer:* 8 days ($2022-12-26 \to 2023-01-03$).
- **Validation Split ($2023-01-03 \to 2023-12-29$):** 460 cases.
- *Temporal Buffer:* 4 days ($2023-12-29 \to 2024-01-02$).
- **Test Split ($2024-01-02 \to 2026-09-17$):** 920 cases ($3.08\times$ larger than v1).
- **Contamination Audit:** 0.00% leakage ($p = 0.000$), 0 duplicate case IDs.

---

## 📋 Data Schema & Sample Record

Each record contains structured attributes, chronological event graphs, detailed Vietnamese legal narratives, and judicial holding rationales:

```json
{
  "case_id": "142/2022/DS-ST",
  "court_name": "TAND TP. Hồ Chí Minh",
  "jurisdiction_level": "Sơ thẩm",
  "case_title": "Tranh chấp hợp đồng đặt cọc chuyển nhượng quyền sử dụng đất",
  "verdict_date": "2022-09-15",
  "domain": "deposit_contract_dispute",
  "plaintiff": "Nguyễn Văn An",
  "defendant": "Trần Thị Bình",
  "earliest_deposit_date": "2021-01-10",
  "breach_date": "2021-03-15",
  "filing_date": "2022-06-20",
  "elapsed_days_breach_to_filing": 462,
  "is_statute_lapsed": false,
  "final_state": "Voidable",
  "ground_truth_verdict": "ACCEPT_DEPOSIT_FORFEITURE",
  "applicable_statutes": [
    "Điều 328 BLDS 2015",
    "Điều 429 BLDS 2015"
  ],
  "fact_summary": "Theo đơn khởi kiện: Ngày 2021-01-10, giữa nguyên đơn Nguyễn Văn An và bị đơn Trần Thị Bình ký kết văn bản đặt cọc số tiền 500 triệu đồng để nhận chuyển nhượng thửa đất số 45 tại TP. Thủ Đức. Đến ngày 2021-03-15, bị đơn không bàn giao mặt bằng và từ chối ký hợp đồng công chứng. Ngày 2022-06-20, nguyên đơn khởi kiện yêu cầu phạt cọc theo thỏa thuận.",
  "judicial_holding_reasoning": "Hội đồng xét xử nhận định: Bị đơn đã vi phạm cam kết không có sự kiện bất khả kháng. Căn cứ Điều 328 BLDS 2015, chấp nhận yêu cầu của nguyên đơn, buộc bị đơn chịu phạt cọc.",
  "temporal_events": [
    {
      "event_type": "contract_signing",
      "subject": "Nguyễn Văn An",
      "timestamp": "2021-01-10"
    },
    {
      "event_type": "contractual_breach",
      "subject": "Trần Thị Bình",
      "timestamp": "2021-03-15"
    },
    {
      "event_type": "lawsuit_filing",
      "subject": "Nguyễn Văn An",
      "timestamp": "2022-06-20"
    }
  ]
}
```

---

## 💻 Quick Start with Hugging Face `datasets`

```python
from datasets import load_dataset

# Load all splits
dataset = load_dataset("datbazuka2502/synapse-civil-bench")

print(dataset)
# DatasetDict({
#     train: Dataset({num_rows: 1460}),
#     validation: Dataset({num_rows: 460}),
#     test: Dataset({num_rows: 920}),
#     counterfactual: Dataset({num_rows: 320})
# })

# Inspect sample record
sample = dataset["test"][0]
print("Case ID:", sample["case_id"])
print("Dispute:", sample["case_title"])
print("Holding:", sample["ground_truth_verdict"])
print("Reasoning:", sample["judicial_holding_reasoning"])
```

---

## ⚖️ Description Logic Ontology Grounding (OWL 2 DL / HermiT)

All concepts are formally grounded in the **Vietnamese Civil Law Ontology (VCLO)** (`vclo_core.owl`):
- **OWL 2 DL Satisfiability:** 100% verified with HermiT Reasoner (0 unsatisfiable classes).
- **Core TBox Rules:**
  - $\text{LapsedContract} \sqsubseteq \text{ExtinguishedContract}$ (Article 429)
  - $\text{UsuriousRate} \sqsubseteq \text{PartialVoid}$ (Article 468)
  - $\text{FormalDefect} \sqcap \ge \frac{2}{3}\text{Performed} \sqsubseteq \text{ValidContract}$ (Article 129)
  - $\text{ForceMajeureInterval} \sqsubseteq \text{TollingInterval}$ (Article 156)

---

## 📜 Citation & Ethical License

This dataset is distributed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

```bibtex
@article{nguyen2026synapselex,
  title     = {SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication},
  author    = {Nguyen, Tien-Dat},
  journal   = {Artificial Intelligence and Law},
  year      = {2026},
  publisher = {Springer},
  note      = {Code and benchmarks available at \url{https://github.com/ntd25022006q/synapselex}}
}
```
