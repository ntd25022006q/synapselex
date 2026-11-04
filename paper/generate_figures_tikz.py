"""
generate_figures_tikz.py
Autonomous Script: Generates pristine academic publication figures for SynapseLex
using standalone LaTeX TikZ and compiles them into vector PDFs and 300 DPI PNGs.
Designed to meet the exact visual standards of NeurIPS / ICML / Springer Q1.
"""

import os
import subprocess
import fitz # PyMuPDF

FIG1_TIKZ = r'''\documentclass[tikz,border=4mm]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,shapes.misc,fit,backgrounds,decorations.pathreplacing,shadows,calc}

% Professional Academic Color Palette (Nature / NeurIPS style)
\definecolor{seqblue}{RGB}{24, 76, 120}
\definecolor{seqbluebg}{RGB}{242, 247, 252}
\definecolor{timecyan}{RGB}{14, 116, 144}
\definecolor{timecyanbg}{RGB}{236, 254, 255}
\definecolor{ontoviolet}{RGB}{79, 70, 229}
\definecolor{ontovioletbg}{RGB}{245, 243, 255}
\definecolor{lawgreen}{RGB}{22, 101, 52}
\definecolor{lawgreenbg}{RGB}{240, 253, 244}
\definecolor{alertred}{RGB}{190, 18, 60}
\definecolor{alertredbg}{RGB}{255, 241, 242}
\definecolor{boxborder}{RGB}{148, 163, 184}
\definecolor{darkslate}{RGB}{30, 41, 59}

\begin{document}
\begin{tikzpicture}[
    font=\sffamily,
    >=Stealth,
    node distance=1.0cm,
    card/.style={
        draw=boxborder!70,
        fill=white,
        rounded corners=4pt,
        drop shadow={opacity=0.10, shadow xshift=1.2pt, shadow yshift=-1.2pt},
        inner sep=6pt
    },
    module/.style={
        draw=#1!80!black,
        fill=#1bg,
        rounded corners=4pt,
        drop shadow={opacity=0.08, shadow xshift=1.2pt, shadow yshift=-1.2pt},
        inner sep=6pt
    },
    tag/.style={
        fill=#1,
        text=white,
        font=\sffamily\bfseries\tiny,
        rounded corners=2pt,
        inner sep=2.5pt
    },
    arrowlabel/.style={
        font=\sffamily\tiny,
        fill=white,
        inner sep=1.5pt,
        text=darkslate
    }
]

% ==============================================================================
% STAGE 1: DYNAMIC CIVIL CASE & TEMPORAL INTERACTION GRAPH
% ==============================================================================
\node[card, text width=4.3cm] (casecard) {
    {\color{seqblue}\textbf{\small 1. Legal Case Fact Sequence}}\\[2pt]
    \rule{4.3cm}{0.4pt}\\[3pt]
    \scriptsize
    \textbf{Claimant $u$ (Buyer)} $\leftrightarrow$ \textbf{Respondent $v$ (Seller)}\\[3pt]
    $\bullet$ \textbf{$t_0$ (2020-01-15):} Deposit Contract ($500$M VND)\\
    $\bullet$ \textbf{$t_1$ (2020-03-01):} Default \& Notice of Breach\\
    $\bullet$ \textbf{$t_2$ (2023-06-20):} Lawsuit filed ($\Delta t = 1,254$\,d)\\[3pt]
    \rule{4.3cm}{0.4pt}\\[2pt]
    \tiny\color{alertred}\textbf{Event Stream:} $\mathcal{S}_{\text{case}} = \{(u, v, r_i, t_i)\}_{i=1}^M$
};
\node[tag=seqblue, above=1pt of casecard.north west, anchor=south west] {STAGE I: EPISODIC INPUT};

\node[card, below=0.6cm of casecard, text width=4.3cm, align=center] (graphnode) {
    {\color{seqblue}\textbf{\small Dynamic Interaction Graph $\mathcal{G}(t)$}}\\[5pt]
    \begin{tikzpicture}[scale=0.9]
        \node[circle, draw=seqblue, fill=seqblue!15, inner sep=3pt, font=\scriptsize\bfseries] (u) at (0, 0) {$u$};
        \node[circle, draw=seqblue, fill=seqblue!15, inner sep=3pt, font=\scriptsize\bfseries] (v) at (3.2, 0) {$v$};
        \draw[->, thick, color=seqblue] (u) to[bend left=25] node[above, font=\tiny] {$e_{1}, t_0$ (Deposit)} (v);
        \draw[->, thick, color=alertred] (v) to[bend left=25] node[below, font=\tiny] {$e_{2}, t_1$ (Breach)} (u);
        \node[draw=gray!50, dashed, rounded corners=2pt, fill=gray!5, inner sep=2pt, font=\tiny] at (1.6, -1.0) {$\Delta t = t_2 - t_1 = 1,254$\,days};
    \end{tikzpicture}
};

\node[draw=seqblue!40, dashed, rounded corners=6pt, fill=seqbluebg!30, fit=(casecard)(graphnode), inner sep=8pt] (stage1box) {};

% ==============================================================================
% STAGE 2: CONTINUOUS HARMONIC ENCODING & AXIOM-TGAT
% ==============================================================================
\node[module=timecyan, right=1.2cm of casecard.north east, anchor=north west, text width=4.5cm] (bochner) {
    {\color{timecyan}\textbf{\small Bochner Continuous Time Kernel}}\\[2pt]
    \rule{4.5cm}{0.4pt}\\[3pt]
    \scriptsize
    $\Phi(\Delta t) = \frac{1}{\sqrt{d_{\tau}}} \left[\cos(\boldsymbol{\omega} \Delta t)^\top \parallel \sin(\boldsymbol{\omega} \Delta t)^\top\right]^\top$\\[2pt]
    \tiny Continuous Fourier Embedding ($\boldsymbol{\omega}_k \sim \mathcal{N}(0, \sigma^2)$)\\[4pt]
    \centering
    \begin{tikzpicture}[xscale=0.4, yscale=0.28]
        \draw[->, gray!60] (0,0) -- (9.2,0) node[right, font=\tiny] {$\Delta t$};
        \draw[->, gray!60] (0,-1.3) -- (0,1.3);
        \draw[domain=0:8.8, samples=60, smooth, thick, color=timecyan] plot (\x, {cos(\x*180/3.14159)});
        \draw[domain=0:8.8, samples=60, smooth, dashed, color=timecyan!60] plot (\x, {sin(\x*180/3.14159)});
    \end{tikzpicture}
};
\node[tag=timecyan, above=1pt of bochner.north west, anchor=south west] {CONTINUOUS TIME EMBEDDING};

\node[module=seqblue, below=0.6cm of bochner, text width=4.5cm] (tgat) {
    {\color{seqblue}\textbf{\small Axiom-TGAT Message Passing ($\times L$)}}\\[2pt]
    \rule{4.5cm}{0.4pt}\\[3pt]
    \scriptsize
    \textbf{Temporal Attention Weights:}\\
    $\alpha_{uv}^{(l)} = \operatorname{Softmax}_v \left(\frac{(\mathbf{h}_u \mathbf{W}_Q)(\mathbf{h}_v \parallel \mathbf{e}_{uv} \parallel \Phi(\Delta t))^\top \mathbf{W}_K^\top}{\sqrt{d}}\right)$\\[4pt]
    \textbf{Aggregation \& Skip Residual $\bigoplus$:}\\
    $\widetilde{\mathbf{h}}_u^{(l)} = \sum_{v \in \mathcal{N}_u} \alpha_{uv}^{(l)} (\mathbf{h}_v \parallel \mathbf{e}_{uv} \parallel \Phi(\Delta t)) \mathbf{W}_V$\\
    $\mathbf{h}_u^{(l)} = \operatorname{LayerNorm}\left(\mathbf{h}_u^{(l-1)} + \widetilde{\mathbf{h}}_u^{(l)}\right)$\\[3pt]
    \tiny\centering\color{seqblue}\textbf{Dynamic Node States:} $\mathbf{z}_{uv}(t) = [\mathbf{h}_u^{(L)}(t) \parallel \mathbf{h}_v^{(L)}(t)]$
};
\node[tag=seqblue, above=1pt of tgat.north west, anchor=south west] {STAGE II: TEMPORAL GNN};

\node[draw=timecyan!50, dashed, rounded corners=6pt, fill=timecyanbg!20, fit=(bochner)(tgat), inner sep=8pt] (stage2box) {};

% ==============================================================================
% STAGE 3: TBOX STATUTORY AXIOMS & HERMIT REASONER
% ==============================================================================
\node[module=ontoviolet, right=1.2cm of bochner.north east, anchor=north west, text width=4.6cm] (tbox) {
    {\color{ontoviolet}\textbf{\small OWL 2 DL Formal Ontology $\mathcal{O}_{\text{civil}}$}}\\[2pt]
    \rule{4.6cm}{0.4pt}\\[3pt]
    \scriptsize
    \textbf{TBox Statutory Axioms ($\mathcal{SROIQ}$):}\\
    $\bullet$ $\text{Valid} \sqcap \text{Void} \sqsubseteq \bot$ \hfill \tiny(Disjointness)\\[2pt]
    $\bullet$ $\text{Voidable} \sqcap \exists \text{curedBy}.(\text{Perform} \ge \frac{2}{3}) \sqsubseteq \text{Valid}$\\
    \null\hfill \tiny(Art. 129(2) Curing)\\[2pt]
    $\bullet$ $\text{Claim} \sqcap \exists \Delta t > 3\,\text{years} \sqsubseteq \text{TimeBarred}$\\
    \null\hfill \tiny(Art. 429 Prescription Bar)\\[3pt]
    \rule{4.6cm}{0.4pt}\\[2pt]
    \textbf{Automated Hypertableau Reasoner:}\\
    $\bullet$ Provable Consistency: $\mathcal{O}_{\text{civil}} \cup \mathcal{A}_{\text{case}} \not\models \bot$\\
    $\bullet$ Penalty: $\mathcal{L}_{\text{onto}} = \sum_{a \in \mathcal{A}_{\text{viol}}} \max(0, -\log P(a))$
};
\node[tag=ontoviolet, above=1pt of tbox.north west, anchor=south west] {STAGE III: TBOX GUARDRAIL};

\node[module=alertred, below=0.6cm of tbox, text width=4.6cm] (statepred) {
    {\color{alertred}\textbf{\small 4-State Automaton Predictor}}\\[2pt]
    \rule{4.6cm}{0.4pt}\\[3pt]
    \scriptsize
    $\mathbf{p}_{\text{state}}(t) = \operatorname{Softmax}(\mathbf{W}_s \mathbf{z}_{uv}(t) + \mathbf{b}_s) \in \Delta^4$\\[3pt]
    States: $\{S_0: \text{Valid}, S_1: \text{Voidable},$\\
    \phantom{States: } $S_2: \text{Void}, S_3: \text{Extinguished}\}$\\[3pt]
    \rule{4.6cm}{0.4pt}\\[2pt]
    \tiny\color{darkslate}\textbf{Total Loss:} $\mathcal{L} = \mathcal{L}_{\text{CE}} + \lambda_{\text{trans}} \mathcal{L}_{\text{trans}} + \lambda_{\text{onto}} \mathcal{L}_{\text{onto}}$
};
\node[tag=alertred, above=1pt of statepred.north west, anchor=south west] {NEURAL PREDICTION};

\node[draw=ontoviolet!50, dashed, rounded corners=6pt, fill=ontovioletbg!20, fit=(tbox)(statepred), inner sep=8pt] (stage3box) {};

% ==============================================================================
% STAGE 4: DEFEASIBLE DUNG FRAMEWORK & ADJUDICATION VERDICT
% ==============================================================================
\node[module=lawgreen, right=1.2cm of tbox.north east, anchor=north west, text width=4.0cm] (dung) {
    {\color{lawgreen}\textbf{\small Defeasible Framework $AF$}}\\[2pt]
    \rule{4.0cm}{0.4pt}\\[3pt]
    \scriptsize
    $AF = \langle \mathcal{A}, \mathcal{R}_{\text{defeat}} \rangle$\\[4pt]
    \centering
    \begin{tikzpicture}[scale=0.92]
        \node[circle, draw=alertred, fill=alertred!10, inner sep=2pt, font=\tiny\bfseries] (aclaim) at (0, 0.9) {$A_{\text{claim}}$};
        \node[circle, draw=gray, fill=gray!10, inner sep=2pt, font=\tiny\bfseries] (adef) at (0, -0.6) {$A_{\text{def}}$};
        \node[circle, draw=lawgreen, fill=lawgreen!20, inner sep=2pt, font=\tiny\bfseries] (abar) at (2.4, 0.9) {$A_{\text{bar}}$};
        
        \draw[->, thick, color=gray] (adef) -- node[left, font=\tiny] {rebut} (aclaim);
        \draw[->, thick, color=alertred, -{Stealth[scale=1.2]}] (abar) -- node[above, font=\tiny\bfseries] {defeat} (aclaim);
        \node[draw=lawgreen, fill=lawgreen!10, rounded corners=2pt, font=\tiny] at (1.2, -0.6) {Art. 429};
    \end{tikzpicture}\\[3pt]
    \rule{4.0cm}{0.4pt}\\[2pt]
    \tiny
    \textbf{Knaster-Tarski Least Fixed Point:}\\
    $GE(AF) = \operatorname{lfp}(F_{AF}) = \{A_{\text{bar}}\}$
};
\node[tag=lawgreen, above=1pt of dung.north west, anchor=south west] {STAGE IV: DEFEASIBLE DUNG HEAD};

\node[card, below=0.6cm of dung, text width=4.0cm, draw=lawgreen!80!black, fill=lawgreenbg] (verdict) {
    \centering
    {\color{lawgreen}\textbf{\small Certified Judicial Decree}}\\[2pt]
    \rule{4.0cm}{0.4pt}\\[3pt]
    \scriptsize
    \textbf{Adjudication Outcome:}\\[2pt]
    \textbf{\color{alertred}\normalsize ACTION DISMISSED}\\[2pt]
    \tiny
    Statute of Limitations Expired\\
    ($\Delta t = 1,254 > 1,095$\,days, Art. 429)\\[3pt]
    \rule{4.0cm}{0.4pt}\\[2pt]
    \scriptsize\color{lawgreen}\textbf{Verification Status:}\\
    $\checkmark$ 100\% TBox Axiom Compliance\\
    $\checkmark$ Grounded Defeasible Proof
};
\node[tag=lawgreen, above=1pt of verdict.north west, anchor=south west] {CERTIFIED VERDICT};

\node[draw=lawgreen!50, dashed, rounded corners=6pt, fill=lawgreenbg!20, fit=(dung)(verdict), inner sep=8pt] (stage4box) {};

% ==============================================================================
% INTER-STAGE CONNECTIONS & DATA FLOW PIPELINE
% ==============================================================================
\draw[->, very thick, color=seqblue] (casecard.east) -- node[above, arrowlabel] {$\{(u,v,r_i,t_i)\}$} (tgat.west);
\draw[->, very thick, color=timecyan] (graphnode.east) -| ++(0.5, 0) |- node[above, arrowlabel, pos=0.7] {$\Delta t$} (bochner.west);
\draw[->, very thick, color=timecyan] (bochner.south) -- node[right, arrowlabel] {$\Phi(\Delta t)$} (tgat.north);

\draw[->, very thick, color=seqblue] (tgat.east) -- node[above, arrowlabel] {$\mathbf{z}_{uv}(t)$} (statepred.west);
\draw[->, very thick, color=seqblue] (tgat.east) -| ++(0.5, 0) |- node[above, arrowlabel, pos=0.7] {ABox Assertions} (tbox.west);
\draw[<->, thick, dashed, color=ontoviolet] (tbox.south) -- node[right, arrowlabel] {$\mathcal{L}_{\text{onto}}$ Guardrail} (statepred.north);

\draw[->, very thick, color=ontoviolet] (tbox.east) -- node[above, arrowlabel] {$\mathcal{A}_{\text{just}}$} (dung.west);
\draw[->, very thick, color=alertred] (statepred.east) -| ++(0.5, 0) |- node[above, arrowlabel, pos=0.7] {$\mathbf{p}_{\text{state}}$} (verdict.west);
\draw[->, very thick, color=lawgreen] (dung.south) -- node[right, arrowlabel] {$GE(AF)$} (verdict.north);

\end{tikzpicture}
\end{document}
'''


FIG2_TIKZ = r'''\documentclass[tikz,border=4mm]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,shapes.misc,fit,backgrounds,decorations.pathreplacing,shadows,calc}

% Academic Color Palette
\definecolor{seqblue}{RGB}{24, 76, 120}
\definecolor{seqbluebg}{RGB}{242, 247, 252}
\definecolor{lawgreen}{RGB}{22, 101, 52}
\definecolor{lawgreenbg}{RGB}{240, 253, 244}
\definecolor{alertred}{RGB}{190, 18, 60}
\definecolor{alertredbg}{RGB}{255, 241, 242}
\definecolor{amberdark}{RGB}{180, 83, 9}
\definecolor{amberdarkbg}{RGB}{254, 243, 199}
\definecolor{graydark}{RGB}{75, 85, 99}
\definecolor{graydarkbg}{RGB}{243, 244, 246}
\definecolor{boxborder}{RGB}{148, 163, 184}

\begin{document}
\begin{tikzpicture}[
    font=\sffamily,
    >=Stealth,
    state/.style={
        rectangle,
        rounded corners=5pt,
        draw=#1!80!black,
        fill=#1bg,
        drop shadow={opacity=0.10, shadow xshift=1pt, shadow yshift=-1pt},
        inner sep=6pt,
        text width=3.4cm,
        align=center
    },
    arg/.style={
        circle,
        draw=#1!80!black,
        fill=#1bg,
        drop shadow={opacity=0.12, shadow xshift=1pt, shadow yshift=-1pt},
        inner sep=4pt,
        font=\sffamily\bfseries\scriptsize,
        minimum size=1.1cm,
        align=center
    },
    panel/.style={
        draw=boxborder!60,
        fill=white,
        rounded corners=6pt,
        inner sep=10pt
    }
]

% ==============================================================================
% SUBFIGURE (a): 4-STATE CONTRACT AUTOMATON
% ==============================================================================
\begin{scope}[local bounding box=subfig_a]
    \node[font=\sffamily\bfseries\normalsize, color=seqblue] at (3.5, 3.2) {(a) 4-State Civil Contract Automaton $\mathcal{M}_{\text{state}}$};

    % Initial entry pointer
    \coordinate (start) at (-1.8, 1.8);
    
    % S0: Valid
    \node[state=lawgreen] (S0) at (1.0, 1.8) {
        \textbf{\small $S_0$: Valid Contract}\\[2pt]
        \tiny Fully enforceable rights \& duties\\
        \color{lawgreen}\textbf{(BLDS 2015 Art. 117)}
    };
    \draw[->, very thick, color=lawgreen] (start) -- node[above, font=\tiny\bfseries] {Execute} (S0.west);

    % S1: Voidable
    \node[state=amberdark] (S1) at (6.2, 1.8) {
        \textbf{\small $S_1$: Voidable Contract}\\[2pt]
        \tiny Form flaw / lack of notarization\\
        \color{amberdark}\textbf{(BLDS 2015 Art. 129(1))}
    };

    % S2: Void ab initio
    \node[state=alertred] (S2) at (6.2, -1.8) {
        \textbf{\small $S_2$: Void \textit{ab initio}}\\[2pt]
        \tiny Nullity from inception\\
        \color{alertred}\textbf{(BLDS 2015 Art. 122--123)}
    };

    % S3: Extinguished / Time-Barred
    \node[state=graydark] (S3) at (1.0, -1.8) {
        \textbf{\small $S_3$: Extinguished / Barred}\\[2pt]
        \tiny Claim right extinguished\\
        \color{graydark}\textbf{(BLDS 2015 Art. 429)}
    };

    % Transitions between States
    % S0 -> S1 (Formal flaw discovered)
    \draw[->, thick, color=amberdark] (S0.north east) to[bend left=18] node[above, font=\tiny, align=center] {Formal Defect\\(No Notarization)} (S1.north west);

    % S1 -> S0 (Curing via 2/3 performance Art 129(2)) [CRITICAL SOTA FEATURE]
    \draw[->, very thick, color=lawgreen] (S1.south west) to[bend left=18] node[below, font=\tiny\bfseries, align=center] {\textbf{Cured: Perform $\ge 2/3$}\\\textbf{(Art. 129(2) Non-Monotonic)}} (S0.south east);

    % S1 -> S2 (Court declares void)
    \draw[->, thick, color=alertred] (S1.south) -- node[right, font=\tiny, align=left] {Petition Granted\\(Nullity decree)} (S2.north);

    % S0 -> S2 (Direct void ab initio)
    \draw[->, thick, dashed, color=alertred] (S0.south east) -- node[above, font=\tiny, sloped] {Prohibited Object (Art. 123)} (S2.north west);

    % S0 -> S3 (Prescription bar expired or performance complete)
    \draw[->, very thick, color=alertred] (S0.south) -- node[left, font=\tiny\bfseries, align=right] {$\Delta t > 3$\,years\\(Art. 429 Limitation)} (S3.north);

    % S1 -> S0 (Challenge window expired without suit)
    \draw[->, thick, color=lawgreen, dashed] (S1.north) to[out=135, in=45] node[above, font=\tiny] {2-Yr Challenge Window Expired (Art. 132)} (S0.north);

    % S2 -> S3 (Restitution completed)
    \draw[->, thick, color=graydark] (S2.west) -- node[below, font=\tiny] {Restitution Executed (Art. 131)} (S3.east);
\end{scope}

% ==============================================================================
% SUBFIGURE (b): DEFEASIBLE DUNG ABSTRACT ARGUMENTATION FRAMEWORK
% ==============================================================================
\begin{scope}[xshift=10.2cm, local bounding box=subfig_b]
    \node[font=\sffamily\bfseries\normalsize, color=seqblue] at (2.4, 3.2) {(b) Defeasible Argumentation Framework $AF$};

    % Arguments
    \node[arg=alertred] (A1) at (0.2, 1.8) {$A_1$};
    \node[arg=amberdark] (A2) at (4.6, 1.8) {$A_2$};
    \node[arg=lawgreen] (A3) at (2.4, -0.2) {$A_3$};
    \node[arg=graydark] (A4) at (2.4, -2.2) {$A_4$};

    % Argument Descriptions
    \node[right=2pt of A1.north east, font=\tiny, align=left, anchor=north west] {
        \textbf{Claimant's Claim:}\\
        Forfeit 500M Deposit\\
        (Art. 328 BLDS)\\[1pt]
        \color{alertred}\textbf{[Defeated]}
    };

    \node[left=2pt of A2.north west, font=\tiny, align=right, anchor=north east] {
        \textbf{Counterclaim:}\\
        Oral Extension\\
        Agreement\\[1pt]
        \color{amberdark}\textbf{[Rebutted]}
    };

    \node[right=2pt of A3.east, font=\tiny, align=left, anchor=west] {
        \textbf{Statutory Prescription Bar:}\\
        $\Delta t = 1,254 > 1,095$\,days (3\,yrs)\\
        \color{lawgreen}\textbf{[Accepted in $GE(AF)$]}\\
        \textbf{(Art. 429 BLDS 2015)}
    };

    \node[right=2pt of A4.east, font=\tiny, align=left, anchor=west] {
        \textbf{Force Majeure Reply:}\\
        Unsubstantiated pandemic defense\\
        \color{graydark}\textbf{[Rejected - No Proof]}
    };

    % Defeat and attack relations
    % Mutual attack between A1 and A2
    \draw[<->, thick, color=amberdark] (A1) -- node[above, font=\tiny\bfseries] {rebuts} (A2);

    % Asymmetric defeat from A3 to A1
    \draw[->, very thick, color=alertred, -{Stealth[scale=1.3]}] (A3) to[bend left=15] node[left, font=\tiny\bfseries] {undercuts} (A1);

    % Attempted attack A4 -> A3
    \draw[->, thick, dashed, color=graydark] (A4) -- node[right, font=\tiny] {attacks} (A3);

    % Knaster-Tarski computation summary box
    \node[draw=lawgreen!80!black, fill=lawgreenbg, rounded corners=4pt, inner sep=4pt, font=\tiny, align=center] at (2.4, 0.9) {
        \textbf{Knaster-Tarski Least Fixed Point:}\\
        $F_{AF}(\emptyset) = \{A_3\} \implies F_{AF}^2(\emptyset) = \{A_3\}$\\
        \color{lawgreen}\textbf{Grounded Extension: $GE(AF) = \{A_3\}$}
    };
\end{scope}

% Surrounding boxes for panels
\node[draw=boxborder!40, rounded corners=8pt, fit=(subfig_a), inner sep=8pt] {};
\node[draw=boxborder!40, rounded corners=8pt, fit=(subfig_b), inner sep=8pt] {};

\end{tikzpicture}
\end{document}
'''

def main():
    os.makedirs('synapselex/paper/figures', exist_ok=True)
    os.makedirs('synapselex/paper/high_res_previews', exist_ok=True)
    
    # Write TikZ TeX files
    with open('synapselex/paper/figures/fig1_standalone.tex', 'w', encoding='utf-8') as f:
        f.write(FIG1_TIKZ)
    with open('synapselex/paper/figures/fig2_standalone.tex', 'w', encoding='utf-8') as f:
        f.write(FIG2_TIKZ)
    print("Wrote fig1_standalone.tex and fig2_standalone.tex")

    # Compile with pdflatex
    for name in ['fig1_standalone', 'fig2_standalone']:
        print(f"Compiling {name}.tex with pdflatex...")
        res = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'{name}.tex'],
            cwd='synapselex/paper/figures',
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            print(f"Error compiling {name}.tex:")
            print(res.stdout[-600:])
            raise RuntimeError(f"pdflatex failed on {name}.tex")
        else:
            print(f"Successfully compiled {name}.pdf")

    # Copy to production figure names
    import shutil
    shutil.copyfile('synapselex/paper/figures/fig1_standalone.pdf', 'synapselex/paper/figures/fig1_system_architecture.pdf')
    shutil.copyfile('synapselex/paper/figures/fig2_standalone.pdf', 'synapselex/paper/figures/fig2_legal_automaton_defeasible.pdf')

    # Convert to 300 DPI PNG using PyMuPDF
    for src_pdf, out_png in [
        ('synapselex/paper/figures/fig1_system_architecture.pdf', 'synapselex/paper/figures/fig1_system_architecture.png'),
        ('synapselex/paper/figures/fig2_legal_automaton_defeasible.pdf', 'synapselex/paper/figures/fig2_legal_automaton_defeasible.png'),
    ]:
        doc = fitz.open(src_pdf)
        pix = doc[0].get_pixmap(dpi=300)
        pix.save(out_png)
        print(f"Rendered {out_png} at 300 DPI ({pix.width}x{pix.height})")

    # Copy to preview locations
    brain_previews = r'C:\Users\ntd25\.gemini\antigravity-cli\brain\b2e0731e-b452-4487-92bc-7902a0e0f131\previews'
    os.makedirs(brain_previews, exist_ok=True)
    shutil.copyfile('synapselex/paper/figures/fig1_system_architecture.png', os.path.join(brain_previews, 'fig1_system_architecture.png'))
    shutil.copyfile('synapselex/paper/figures/fig2_legal_automaton_defeasible.png', os.path.join(brain_previews, 'fig2_legal_automaton_defeasible.png'))
    shutil.copyfile('synapselex/paper/figures/fig1_system_architecture.png', 'paper_figures/fig1_system_architecture.png')
    shutil.copyfile('synapselex/paper/figures/fig2_legal_automaton_defeasible.png', 'paper_figures/fig2_legal_automaton_defeasible.png')
    print("Updated all preview PNG assets successfully.")

if __name__ == '__main__':
    main()
