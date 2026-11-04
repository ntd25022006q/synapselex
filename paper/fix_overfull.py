import os

tex_path = os.path.join(os.path.dirname(__file__), "synapselex_paper.tex")

with open(tex_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Subsection title
old_sub = r"\subsection{Transcending Static Monotonicity: Temporal Description Logic ($\mathcal{T}\text{-}\mathcal{SROIQ}$) and Markovian Legal Automata}"
new_sub = r"\subsection[Transcending Monotonicity via Temporal DL]{Transcending Static Monotonicity: Temporal DL ($\mathcal{T}\text{-}\mathcal{SROIQ}$) and Markovian Automata}"

if old_sub in text:
    text = text.replace(old_sub, new_sub)
    print("Fixed subsection title.")

# 2. Proof lines
old_proof_head = r"""\begin{proof}
For each state-verdict pair $(s, y) \in \mathcal{S} \times \mathcal{Y}$, the satisfiability of $\mathcal{T}_{\mathcal{VCLO}} \cup \{ \mathrm{ContractState}(c, s), \mathrm{Verdict}(c, y) \}$ is evaluated by HermiT:
\begin{itemize}[leftmargin=*]
\item For $s = 3$ ($\text{Extinguished}$ under Art.~429): Axiom~\eqref{eq:axiom4} specifies that an extinguished contract forces dismissal: $\text{Contract} \sqcap \exists \text{hasLegalState}.\text{Extinguished} \sqsubseteq \exists \text{mandatesVerdict}.\text{DismissStatuteLapsed}$. Substantive deposit remedies (Forfeiture, DoubleRefund) require an active enforceable obligation."""

new_proof_head = r"""\begin{proof}
For each state-verdict pair $(s, y) \in \mathcal{S} \times \mathcal{Y}$, the joint satisfiability:
\begin{equation}
\mathcal{T}_{\mathcal{VCLO}} \cup \{ \mathrm{State}(c, s), \mathrm{Verdict}(c, y) \}
\end{equation}
is evaluated by HermiT:
\begin{itemize}[leftmargin=*]
\item For $s = 3$ ($\text{Extinguished}$ under Art.~429): Axiom~\eqref{eq:axiom4} specifies that an extinguished contract forces dismissal ($\text{Extinguished} \sqsubseteq \exists \text{mandatesVerdict}.\text{DismissStatuteLapsed}$). Substantive deposit remedies (Forfeiture, DoubleRefund) require an active enforceable obligation."""

if old_proof_head in text:
    text = text.replace(old_proof_head, new_proof_head)
    print("Fixed proof head and axiom text.")

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved.")
