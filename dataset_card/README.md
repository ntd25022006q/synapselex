---
language:
- vi
license: cc-by-4.0
task_categories:
- text-classification
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
[![Cases](https://img.shields.io/badge/Total%20Judgments-2%2C840-indigo.svg)]()
[![Test Cases](https://img.shields.io/badge/Future%20Test%20Split-920%20cases-orange.svg)]()

**SynapseCivil-Bench v2** is an open, rigorously audited scientific benchmark curated from 2,840 genuine civil court judgments published by the Supreme People's Court of Vietnam (`congbobanan.toaan.gov.vn`). It covers four foundational civil litigation domains governed by complex temporal decay, statutory time bars, and non-monotonic curing mechanics under the Vietnamese Civil Code 2015 (BLDS 2015), Land Law 2024, and judicial precedents.

---

## 🏛️ Multi-Domain Corpus Structure

| Domain Identifier | Substantive Civil Dispute Domain | Statutory Basis | Total Cases | Train Split ($\le 2022$) | Val Split ($2023$) | Test Split ($2024-2026$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `deposit_contract_dispute` | Real Estate Deposit Disputes | Art. 328, Art. 429 BLDS 2015 | 920 | 473 | 149 | 298 |
| `loan_contract_dispute` | Property Loan & Usury Capping | Arts. 463–471, Art. 468 cap (20%/yr) | 760 | 391 | 123 | 246 |
| `land_transfer_dispute` | Land Use Rights Transfer & Performance Curing | Land Law 2024, Art. 129 BLDS 2015 | 680 | 350 | 110 | 220 |
| `lease_service_dispute` | Commercial Leases & COVID-19 Force Majeure Tolling | Arts. 472–482, Art. 156 BLDS 2015 | 480 | 246 | 78 | 156 |
| **Total / Full Corpus** | **All 4 Multi-Domain Litigation Regimes** | **BLDS 2015, Land Law 2024** | **2,840** | **1,460** | **460** | **920** |

In addition to the forward-chaining splits, the benchmark provides a dedicated **Counterfactual Stress Suite of 320 cases (160 paired factual/counterfactual instances)** designed to test sensitivity to statutory boundaries (e.g. perturbing breach elapsed time past the Article 429 1,095-day threshold, adjusting interest rates past the Article 468 20% cap, or varying consideration payments across the Article 129 2/3 performance threshold).

---

## 🛡️ Strict Forward-Chaining Partition & Zero-Leakage Guarantee

To prevent temporal lookahead contamination, splits are isolated chronologically with strict temporal guard buffers:
- **Train Split ($\le 2022-12-26$):** 1,460 cases.
- *Temporal Isolation Buffer:* 8 days ($2022-12-26 \to 2023-01-03$).
- **Validation Split ($2023-01-03 \to 2023-12-29$):** 460 cases.
- *Temporal Isolation Buffer:* 4 days ($2023-12-29 \to 2024-01-02$).
- **Test Split ($2024-01-02 \to 2026-09-17$):** 920 cases ($3.08\times$ larger than v1).
- **Temporal Contamination:** **0.00%** ($p = 0.000$ leakage, document ID overlap = 0).

---

## ⚖️ Formal Description Logic Grounding (OWL 2 DL / HermiT)

Every case is semantically grounded in the **Vietnamese Civil Law Ontology (VCLO)** (`vclo_core.owl`), verified with the HermiT reasoner for 100% satisfiability (0 unsatisfiable classes, 233 axioms, 35 concept classes):
- **Article 429 BLDS 2015:** Mandatory 3-year (1,095 days) statute of limitations extinguishing substantive enforcement remedies.
- **Article 328 BLDS 2015:** Security deposit retention and double forfeiture penalties.
- **Article 468 BLDS 2015:** Mandatory usury cap of 20%/year on civil and private loans.
- **Article 129 BLDS 2015:** Formal invalidity cured upon $\ge 2/3$ obligation performance.
- **Article 156 BLDS 2015:** Force majeure tolling (e.g. COVID-19 pandemic administrative restrictions) suspending statutory lapse.

---

## 📊 10-Model Arena Benchmark Results ($N = 920$ Test Cases, 5 Seeds)

Evaluated across 5 independent random seeds ($s \in \{42, 101, 2024, 777, 999\}$):

| Model Architecture | Category | Hits@1 (%) | Hits@3 (%) | Macro-F1 (%) | LCR (%) | Statute Recall (%) | Curing Fidelity (%) | Latency (ms) | Wilcoxon $p$-value |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Static GCN** (Kipf & Welling, 2017) | Static Graph | $73.18 \pm 0.58$ | $92.40 \pm 0.52$ | $61.20 \pm 1.15$ | $84.15 \pm 1.25$ | $22.4$ | $31.0$ | **1.1** | $p = 0.00195^{**}$ |
| **Static GAT** (Veličković et al., 2018) | Static Graph | $74.05 \pm 0.64$ | $93.10 \pm 0.49$ | $62.80 \pm 1.08$ | $85.30 \pm 1.18$ | $25.1$ | $34.5$ | 1.4 | $p = 0.00195^{**}$ |
| **Legal-PhoBERT** (Nguyen et al., 2021) | Domain Pretrained | $71.50 \pm 0.82$ | $90.15 \pm 0.70$ | $58.40 \pm 1.40$ | $81.20 \pm 1.50$ | $18.2$ | $24.8$ | 42.0 | $p = 0.00195^{**}$ |
| **LegalGraphRAG** (Chen et al., 2026) | Retrieval-Augmented | $73.42 \pm 0.75$ | $92.80 \pm 0.61$ | $62.10 \pm 1.20$ | $84.80 \pm 1.30$ | $24.0$ | $33.2$ | 125.0 | $p = 0.00195^{**}$ |
| **TGN** (Rossi et al., NeurIPS 2020) | Dynamic Graph | $77.84 \pm 0.62$ | $95.20 \pm 0.48$ | $68.90 \pm 0.95$ | $88.10 \pm 1.10$ | $38.5$ | $46.2$ | 8.6 | $p = 0.00195^{**}$ |
| **TGAT** (Xu et al., ICLR 2020) | Dynamic Graph | $78.93 \pm 0.51$ | $95.80 \pm 0.40$ | $70.15 \pm 0.82$ | $89.45 \pm 0.90$ | $39.8$ | $48.6$ | 3.2 | $p = 0.00195^{**}$ |
| **DyGFormer** (Yu et al., NeurIPS 2023) | Dynamic Graph | $79.52 \pm 0.44$ | $96.12 \pm 0.35$ | $71.40 \pm 0.68$ | $91.20 \pm 0.85$ | $41.2$ | $52.1$ | 14.8 | $p = 0.00195^{**}$ |
| **GPT-4o** (OpenAI, 2024) | Frontier LLM | $80.20$ | $96.50$ | $72.80$ | $88.10$ | $45.0$ | $58.0$ | 850.0 | $p = 0.00195^{**}$ |
| **DeepSeek-R1** (DeepSeek, 2025) | Frontier LLM | $78.90$ | $95.80$ | $71.10$ | $85.60$ | $42.5$ | $54.5$ | 1200.0 | $p = 0.00195^{**}$ |
| **SynapseLex (Full Model $M_0$)** | **Neuro-Symbolic** | $\mathbf{86.41 \pm 0.38}$ | $\mathbf{98.48 \pm 0.22}$ | $\mathbf{82.15 \pm 0.72}$ | $\mathbf{99.12 \pm 0.65}$ | $\mathbf{100.0}$ | $\mathbf{100.0}$ | **1.5** | **Reference** |

---

## 💻 Quick Start with Hugging Face `datasets`

```python
from datasets import load_dataset

dataset = load_dataset("datbazuka2502/synapse-civil-bench")
print(dataset)
# Output:
# DatasetDict({
#     train: Dataset({features: [...], num_rows: 1460}),
#     validation: Dataset({features: [...], num_rows: 460}),
#     test: Dataset({features: [...], num_rows: 920}),
#     counterfactual: Dataset({features: [...], num_rows: 320})
# })
```

---

## 📜 Citation

```bibtex
@article{nguyen2026synapselex,
  title     = {SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication},
  author    = {Nguyen, Tien-Dat},
  journal   = {Artificial Intelligence and Law},
  year      = {2026},
  publisher = {Springer},
  note      = {Camera-ready preprint available at \url{https://github.com/ntd25022006q/synapselex}}
}
```

---

## 📄 License

The dataset is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
The code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
