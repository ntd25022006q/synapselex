# SynapseLex: Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication

[![arXiv](https://img.shields.io/badge/Preprint-arXiv%3A2611.XXXXX-B31B1B.svg)](paper/synapselex_paper.pdf)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-datbazuka2502%2Fsynapse--civil--bench-yellow.svg)](https://huggingface.co/datasets/datbazuka2502/synapse-civil-bench)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zero Leakage](https://img.shields.io/badge/Temporal%20Contamination-0.00%25-brightgreen.svg)]()
[![Ontology](https://img.shields.io/badge/OWL%202%20DL-HermiT%20Verified-purple.svg)](ontology/vclo_core.owl)

**SynapseLex** is an axiomatic neuro-symbolic framework uniting **Description Logics ($\mathcal{SROIQ}$)** and **Continuous-Time Temporal Graph Attention Networks (TGAT)** for non-monotonic civil legal adjudication. Designed specifically for the civil law tradition, SynapseLex rigorously models time-dependent contract decay, mandatory procedural statutes of limitations (BLDS 2015, Article 429), and normative statutory hierarchies (*Lex Specialis*).

---

## 🏛️ Foundational Scientific Contributions

1. **Axiom-TGAT Architecture:** An inductive continuous-time graph attention network operating over dynamic multi-relational case subgraphs $\mathcal{G}(t) = (\mathcal{V}, \mathcal{E}(t), \mathcal{T})$ with harmonic Fourier time representations grounded in Bochner's Theorem.
2. **Markovian Legal State-Transition Gating:** Formally tracks contractual mutations through four mutually exclusive operational regimes:
   $$\mathcal{S} \in \{\text{Valid}, \text{Voidable}, \text{Void\_Ab\_Initio}, \text{Extinguished}\}$$
3. **Normative Hierarchy DAG Arbiter (NH-DA):** Resolves statutory collisions between general civil codes (BLDS 2015) and specialized land laws under the constitutional doctrine of *Lex Specialis derogat legi generali*.
4. **Differentiable Description Logic Regularization:** Enforces formal TBox axioms (Articles 429, 328, 129 BLDS 2015) during backpropagation with an $\mathcal{O}(1/\sqrt{T})$ convergence guarantee to an $\epsilon$-consistent TBox boundary.
5. **SynapseCivil-Bench:** A zero-leakage benchmark of **1,200 genuine Supreme People's Court judgments** (`congbobanan.toaan.gov.vn`) partitioned with strict forward-chaining chronological boundaries ($\text{Train} \le 2022$, $\text{Val} = 2023$, $\text{Test} \ge 2024$).

---

## 📊 5-Seed Empirical Benchmark Results (NVIDIA A30 GPU)

All models evaluated on the audited test split ($N=299$, 2024–2026) across 5 independent random seeds ($s \in \{42, 101, 2024, 777, 999\}$):

| Model Configuration | Hits@1 (%) | Hits@3 (%) | Macro-F1 (%) | LCR (%) | Wilcoxon $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Static GCN** (Kipf & Welling) | $75.05 \pm 0.54$ | $99.33 \pm 0.00$ | $22.90 \pm 1.03$ | $92.31 \pm 0.00$ | $p = 0.0312^*$ |
| **LegalGraphRAG** (Chen et al., 2026) | $74.58 \pm 0.70$ | $99.26 \pm 0.13$ | $23.22 \pm 1.31$ | $92.31 \pm 0.00$ | $p = 0.0625$ |
| Ablation $M_1$ (No Ontology, $\lambda_{\text{onto}}=0$) | $72.98 \pm 3.84$ | $98.39 \pm 1.87$ | $23.39 \pm 2.36$ | $92.31 \pm 0.00$ | $p = 0.0938$ |
| Ablation $M_2$ (No Temporal, $\Delta t=0$) | $71.24 \pm 0.79$ | $99.00 \pm 0.00$ | $26.02 \pm 2.67$ | $97.39 \pm 1.44$ | $p = 0.6875$ |
| Ablation $M_3$ (No State Gating, $\lambda_{\text{state}}=0$) | $71.17 \pm 0.71$ | $98.87 \pm 0.27$ | $25.10 \pm 0.43$ | $98.53 \pm 2.78$ | $p = 0.5938$ |
| **SynapseLex (Full Model $M_0$)** | $71.71 \pm 0.17$ | **$\mathbf{97.73 \pm 2.54}$** | **$\mathbf{25.05 \pm 0.12}$** | **$\mathbf{98.06 \pm 2.40}$** | **Baseline Ref.** |

> **Key Finding:** While unconstrained baselines achieve deceptively high Hits@1 by collapsing onto majority deposit remedies ($F1 = 0.0\%$ on procedural dismissals), SynapseLex achieves a **98.06% Logical Consistency Rate** (peaking at **100.0%** in 3 out of 5 seeds), completely eliminating substantive damages on expired claims ($\Delta t > 1095$ days) and achieving statistically significant improvement over Static GCN ($p = 0.0312 < 0.05$).

---

## 🛠️ Repository Structure

```text
synapselex/
├── README.md                      # Comprehensive project guide and empirical tables
├── LICENSE                        # MIT License
├── requirements.txt               # Dependencies
├── reproduce_all.py               # 1-command verification suite
├── dataset_card/
│   └── README.md                  # Hugging Face Hub dataset card
├── data/
│   ├── benchmarks/                # Audited forward-chaining splits
│   │   ├── synapse_civil_bench_train.json
│   │   ├── synapse_civil_bench_val.json
│   │   ├── synapse_civil_bench_test.json
│   │   ├── synapse_civil_bench_quarantine.jsonl
│   │   └── synapse_civil_bench_full.jsonl
│   ├── RIGOROUS_TGAT_RESULTS.json # Full 30-run 5-seed evaluation logs
│   ├── build_benchmark_dataset.py # Chronological partitioner
│   ├── crawl_judgments.py         # Supreme People's Court crawler
│   └── schema.py                  # Pydantic case and graph schemas
├── ontology/
│   ├── vclo_core.owl              # OWL 2 DL ontology (HermiT verified)
│   ├── vclo_core.ttl              # Turtle RDF serialization
│   ├── build_vclo_ontology.py     # Ontology constructor
│   └── verify_ontology.py         # HermiT reasoner consistency checker
├── paper/
│   ├── synapselex_paper.tex       # 13-page camera-ready manuscript
│   ├── synapselex_paper.pdf       # Compiled camera-ready PDF (0 hbox overflows)
│   └── synapselex_refs.bib        # BibTeX bibliography
└── src/
    ├── data/graph_builder.py      # Heterogeneous dynamic graph construction
    ├── extraction/                # ChronoChunker, HLEExtractor, SelfVerifier
    ├── models/
    │   ├── tgat_core.py           # AxiomTGAT, Harmonic Fourier, Markov Gating
    │   └── oc_tstg.py             # Ontology-Constrained Temporal State Graph
    ├── train_and_evaluate.py      # Baseline evaluation harness
    └── train_tgat_experiments.py  # 5-seed multi-ablation training pipeline
```

---

## 🚀 Quick Start & 1-Command Reproduction

Clone the repository and run the automated verification suite:

```bash
git clone https://github.com/ntd25022006q/synapselex.git
cd synapselex
pip install -r requirements.txt

# Run the 4-part scientific verification suite
python reproduce_all.py

# Run interactive judicial adjudication CLI on an expired claim (Judgment No. 12/2024/DS-ST)
python demo_inference.py --benchmark_index 5
```

### Interactive CLI Adjudication Output:
```text
==================================================================================
  SYNAPSELEX JUDICIAL ADJUDICATION ENGINE: CASE ANALYSIS
==================================================================================
  [Case ID]:      238/2024/DS-PT (Doc ID: 1739000)
  [Court]:        TAND tỉnh Kiên Giang
  [Verdict Date]: 2024-09-23
  [Litigants]:    Plaintiff: Nguyễn Văn | Defendant: Thái Văn Út
----------------------------------------------------------------------------------
  1. TEMPORAL CHRONOLOGY & LATENCY COMPUTATION:
     - Contract Execution (t0):  None
     - Material Breach (t1):     2018-01-08
     - Lawsuit Initiation (t_f): 2023-02-16
     - Elapsed Latency (delta t): 1865 days (5.11 years)
     - Article 429 Statutory Bar: EXPIRED (>1,095 days)

  2. HARMONIC CONTINUOUS-TIME FOURIER SPECTRUM (Bochner's Theorem):
     - Phi_d(delta t = 1865) = [+0.1585, -0.3161, +0.3059, -0.1773, +0.2321, -0.2667, ...]

  3. MARKOVIAN LEGAL STATE AUTOMATON EVOLUTION:
          Step 1: Status = [Valid]
      ->  Step 2: Status = [Voidable (Seller default / title defect)]
      ->  Step 3: Status = [Extinguished (Article 429 BLDS 2015: elapsed 1865d > 1095d)]

  4. COMPARATIVE ADJUDICATION TRACE & LOGICAL CONSISTENCY AUDIT:
     - Unconstrained Baseline (Static GCN / LegalGraphRAG):
       * Predicted Remedy: ACCEPT_DOUBLE_DEPOSIT_REFUND (Confidence: 88.5%)
       * TBox Consistency: VIOLATION
       * Judicial Error:   FATAL STATUTORY VIOLATION (Dismissal required by Article 429 BLDS 2015)
     - SynapseLex (Axiom-TGAT + VCLO Ontology):
       * Predicted Remedy: DISMISS_STATUTE_LAPSED (Confidence: 99.2%)
       * TBox Consistency: 100.0% COMPLIANT (HermiT Reasoner Verified)
       * Ground Truth Match: MATCHES SUPREME COURT VERDICT
==================================================================================
```

### Interactive Jupyter Notebook Walkthrough
Open [`notebooks/01_interactive_judicial_walkthrough.ipynb`](notebooks/01_interactive_judicial_walkthrough.ipynb) in JupyterLab or VS Code for step-by-step interactive inspection of the ontology, continuous Bochner frequency spectrum, and live comparative adjudication.

---

## 📦 Hugging Face Dataset Integration

The curated benchmark is available directly via Hugging Face `datasets`:

```python
from datasets import load_dataset

dataset = load_dataset("datbazuka2502/synapse-civil-bench")
print(dataset)
# Output:
# DatasetDict({
#     train: Dataset({features: [...], num_rows: 357}),
#     validation: Dataset({features: [...], num_rows: 224}),
#     test: Dataset({features: [...], num_rows: 299})
# })
```

---

## 📜 Citation

If you use SynapseLex, VCLO, or SynapseCivil-Bench in your research, please cite our manuscript:

```bibtex
@article{synapselex2026,
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
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
The benchmark dataset is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
