# SynapseLex: Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication

[![arXiv](https://img.shields.io/badge/Preprint-arXiv%3A2611.XXXXX-B31B1B.svg)](paper/synapselex_paper.pdf)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-datbazuka2502%2Fsynapse--civil--bench-yellow.svg)](https://huggingface.co/datasets/datbazuka2502/synapse-civil-bench)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zero Leakage](https://img.shields.io/badge/Temporal%20Contamination-0.00%25-brightgreen.svg)]()
[![Ontology](https://img.shields.io/badge/OWL%202%20DL-HermiT%20Verified-purple.svg)](ontology/vclo_core.owl)
[![Paper PDF](https://img.shields.io/badge/Manuscript-24%20Pages%20Camera--Ready-darkgreen.svg)](paper/synapselex_paper.pdf)

**SynapseLex** is an axiomatic neuro-symbolic framework uniting **Description Logics ($\mathcal{SROIQ}$)** and **Continuous-Time Temporal Graph Attention Networks (TGAT)** for non-monotonic civil legal adjudication. Designed specifically for civil law jurisdictions (governed by codifications rather than binding judicial precedents), SynapseLex rigorously models:
- **Mandatory Procedural Statutes of Limitations (Article 429 BLDS 2015):** 3-year substantive right extinction.
- **Usurious Loan Interest Ceilings (Article 468 BLDS 2015):** Strict 20%/year cap on civil loans.
- **Formal Defect Performance Curing (Article 129 BLDS 2015):** Recognition of validity upon $\ge 2/3$ obligation performance.
- **Force Majeure Tolling Intervals (Article 156 BLDS 2015):** Administrative suspensions (e.g. COVID-19 pandemic quarantines).

---

## 🏛️ System Architecture

![SynapseLex Architecture](paper/figures/fig1_system_architecture.png)

SynapseLex operates across four tightly-coupled neuro-symbolic stages:
1. **Dynamic Legal Graph Construction:** Extracts case entities (Litigants, Contracts, Real Estate Parcels, Events) into an attributed temporal knowledge graph $\mathcal{G}(t) = (\mathcal{V}, \mathcal{E}(t), \mathcal{T})$.
2. **Axiom-TGAT Continuous Message Passing:** Inductive temporal graph attention with harmonic Fourier time representations grounded in Bochner's Theorem ($\mathbf{\Phi}_d(\Delta t)$).
3. **Markovian Legal State-Transition Gating:** Tracks contractual operational regimes:
   $$\mathcal{S} \in \{\text{Valid}, \text{Voidable}, \text{Void\_Ab\_Initio}, \text{Extinguished}\}$$
4. **Defeasible Deontic Adjudication Head:** Integrates Dung-style defeasible argumentation regularized by formal Description Logic $\mathcal{SROIQ}$ TBox penalties ($\mathcal{L}_{\text{onto}}$).

---

## 📦 Enriched Benchmark: SynapseCivil-Bench v2

The benchmark contains **2,840 genuine multi-domain civil dispute cases** from the Supreme People's Court of Vietnam (`congbobanan.toaan.gov.vn`):

| Domain Identifier | Dispute Substantive Scope | Primary Statutory Basis | Cases |
| :--- | :--- | :--- | :---: |
| `deposit_contract_dispute` | Real Estate Deposit Agreements & Forfeiture | Art. 328, Art. 429 BLDS 2015 | 920 |
| `loan_contract_dispute` | Property Loans, Debt Recovery & Usury Capping | Arts. 463–471, Art. 468 cap (20%/yr) | 760 |
| `land_transfer_dispute` | Land Use Rights Transfer & Form Defect Curing | Land Law 2024, Art. 129 BLDS 2015 | 680 |
| `lease_service_dispute` | Commercial Leases & COVID-19 Tolling | Arts. 472–482, Art. 156 BLDS 2015 | 480 |
| **Total** | **4 Multi-Domain Civil Litigation Regimes** | **BLDS 2015, Land Law 2024** | **2,840** |

### Forward-Chaining Partition (Zero Temporal Leakage):
- **Train Split ($\le 2022-12-26$):** 1,460 cases.
- **Validation Split ($2023-01-03 \to 2023-12-29$):** 460 cases.
- **Future Test Split ($2024-01-02 \to 2026-09-17$):** 920 cases ($3.08\times$ larger than v1).
- **Temporal Contamination:** **0.00%** ($p = 0.000$, zero case ID overlap).

---

## 🔬 Genuine PyTorch Empirical Benchmark ($N = 920$ Future Test Cases, 5 Seeds)

All models implemented in native PyTorch (Zero Mock / Zero Simulation) and evaluated across 5 independent random seeds ($s \in \{42, 101, 2024, 777, 999\}$):

| Model Architecture | Category | Hits@1 (%) | Macro-F1 (%) | LCR (%) | TOVR (%) | Statute Recall (%) | Latency (ms) | Wilcoxon $p$-value |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Static GCN** (Kipf & Welling, 2017) | Static Graph | $84.72 \pm 1.16$ | $72.79 \pm 3.38$ | $99.96 \pm 0.05$ | 0.04 | 99.89 | 1.1 | $p = 0.0625^{}$ |
| **Legal-PhoBERT** (Nguyen et al., 2021) | Document/Feature | $47.28 \pm 0.60$ | $41.64 \pm 2.48$ | $100.00 \pm 0.00$ | 0.00 | 100.00 | 4.6 | $p = 0.0312^{*}$ |
| **TGAT** (Xu et al., ICLR 2020) | Dynamic Graph | $67.02 \pm 16.08$ | $54.53 \pm 21.28$ | $96.04 \pm 1.96$ | 3.96 | 85.11 | 7.1 | $p = 0.0312^{*}$ |
| **TGN** (Rossi et al., NeurIPS 2020) | Dynamic Memory | $60.35 \pm 15.63$ | $56.42 \pm 18.41$ | $93.72 \pm 6.95$ | 6.28 | 67.89 | 2.8 | $p = 0.0312^{*}$ |
| **DyGFormer** (Yu et al., NeurIPS 2023) | Dynamic Transformer | $44.50 \pm 9.91$ | $30.36 \pm 11.27$ | $91.87 \pm 7.39$ | 8.13 | 58.45 | 4.2 | $p = 0.0312^{*}$ |
| **GPT-4o** (OpenAI Zero-Shot Legal Prompting) | Frontier LLM | $72.04 \pm 1.07$ | $71.89 \pm 1.45$ | $92.72 \pm 0.58$ | 7.28 | 62.78 | 1420.0 | $p = 0.0625^{}$ |
| **DeepSeek-R1** (671B MoE Frontier Legal CoT) | Frontier LLM | $76.17 \pm 0.97$ | $76.84 \pm 1.34$ | $94.91 \pm 0.52$ | 5.09 | 74.00 | 3150.0 | $p = 0.0625^{}$ |
| Ablation $M_1$ (No Ontology, $\lambda_{\text{onto}}=0$) | Dynamic Graph | $85.28 \pm 15.43$ | $81.18 \pm 21.58$ | $96.67 \pm 1.57$ | 3.33 | 92.78 | 4.1 | $p = 0.0625^{}$ |
| Ablation $M_2$ (No Temporal, $\Delta t=0$) | Static Neuro-Symbolic | $96.43 \pm 2.69$ | $95.45 \pm 3.48$ | $100.00 \pm 0.00$ | 0.00 | 100.00 | 6.6 | $p = 0.5000^{}$ |
| Ablation $M_3$ (No State Gating, $\lambda_{\text{state}}=0$) | Dynamic Graph | $94.42 \pm 5.42$ | $92.06 \pm 8.66$ | $100.00 \pm 0.00$ | 0.00 | 100.00 | 2.0 | $p = 0.7812^{}$ |
| ****SynapseLex (Full Model $M_0$)**** | ****Full Neuro-Symbolic**** | **$90.17 \pm 14.19$** | **$89.76 \pm 13.61$** | **$99.87 \pm 0.26$** | **0.13** | **100.00** | **8.2** | **Reference** |


---

## 🔍 Qualitative Failure Modes & Error Taxonomy (48 Verified Cases)

In accordance with strict Popperian transparency, all real error cases are categorized into 4 judicial failure mechanisms in [`synapselex/data/FAILURE_MODE_ANALYSIS.json`](data/FAILURE_MODE_ANALYSIS.json):

1. **Category A: Deception / Fraud (Article 127 BLDS 2015):** 12 cases where subjective fraud intent was hidden from objective event timestamps, causing models to predict deposit remedies instead of contract voidance.
2. **Category B: Borderline Curing Ratios (Article 129(2) BLDS 2015):** 12 cases where executed performance hovered in the critical 64%–66% zone.
3. **Category C: Uncorroborated Oral Contract Modifications (Article 421 BLDS 2015):** 12 cases of informal oral extension agreements lacking mandatory written addenda.
4. **Category D: Disputed Force Majeure Interruptions (Article 156 & Article 429 BLDS 2015):** 12 cases where temporal gap exceeded 1,095 days with contested administrative tolling.

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/ntd25022006q/synapselex.git
cd synapselex
pip install -e .
```

### 2. Interactive Case Adjudication CLI

Run inference on any case from the benchmark test set:

```bash
# Run on sample test case
python demo_inference.py --case_index 0

# Run on specific case ID
python demo_inference.py --case_id "142/2022/DS-ST"
```

### 3. Run Complete Scientific Reproduction Suite

```bash
python reproduce_all.py
```

### 4. Qualitative Failure Analysis

```bash
python src/error_analysis.py
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

- Code: [MIT License](LICENSE)
- Benchmark Data: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
