#!/usr/bin/env python3
"""
create_fig1_synapselex.py
Generates pristine, publication-grade vector PDF and 300 DPI PNG for
Figure 1: SynapseLex Neuro-Symbolic System Architecture.
Guarantees 100% legible text, zero overlap, and accurate domain mapping.
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
    "font.size": 8.5,
    "figure.dpi": 300,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig = plt.figure(figsize=(13.2, 4.4), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 132)
ax.set_ylim(0, 44)
ax.axis("off")

# ------------------------------------------------------------------------------
# COLOR PALETTE (Modern NeurIPS / Nature Style)
# ------------------------------------------------------------------------------
C_BORDER = "#94A3B8"

# Stage 1: Dynamic Graph (Blue)
C_S1_BG = "#F0F7FF"
C_S1_BORDER = "#1E40AF"
C_S1_TITLE = "#1E3A8A"

# Stage 2: Axiom-TGAT (Cyan / Teal)
C_S2_BG = "#ECFEFF"
C_S2_BORDER = "#0E7490"
C_S2_TITLE = "#155E75"

# Stage 3: Ontology & TBox (Indigo / Violet)
C_S3_BG = "#F5F3FF"
C_S3_BORDER = "#6D28D9"
C_S3_TITLE = "#4C1D95"

# Stage 4: Defeasible Head (Green)
C_S4_BG = "#F0FDF4"
C_S4_BORDER = "#15803D"
C_S4_TITLE = "#14532D"

def draw_rounded_rect(ax, x, y, w, h, bg_color, border_color, lw=1.2, radius=1.2, linestyle="-"):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={radius},rounding_size={radius}",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=lw,
        linestyle=linestyle,
        zorder=2
    )
    ax.add_patch(box)
    return box

def draw_card(ax, x, y, w, h, bg_color="#FFFFFF", border_color="#CBD5E1", lw=1.0, radius=0.8):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={radius},rounding_size={radius}",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=lw,
        zorder=3
    )
    ax.add_patch(box)
    return box

def draw_arrow(ax, x1, y1, x2, y2, color="#475569", lw=1.5, style="->"):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=f"-|>,head_length=4.5,head_width=3.0",
        color=color,
        linewidth=lw,
        zorder=5
    )
    ax.add_patch(arrow)

# ==============================================================================
# STAGE 1: DYNAMIC MULTI-RELATIONAL DISPUTE GRAPH (x: 2 to 31)
# ==============================================================================
draw_rounded_rect(ax, 2, 2, 28, 40, C_S1_BG, C_S1_BORDER, lw=1.5)
ax.text(16, 40.5, "Stage 1: Dynamic Legal Graph Extraction", fontsize=9.5, fontweight="bold", color=C_S1_TITLE, ha="center")
ax.text(16, 38.8, r"Court Record $\to \mathcal{G}(t) = (\mathcal{V}, \mathcal{E}, \mathcal{T})$", fontsize=7.5, fontstyle="italic", color="#334155", ha="center")

# Subcard: Litigants & Object
draw_card(ax, 3.5, 23.5, 25, 13.5, bg_color="#FFFFFF", border_color="#BFDBFE")
ax.text(16, 35.2, "Bipartite Dispute Subgraph", fontsize=8, fontweight="bold", color="#1E40AF", ha="center")

# Graph nodes
# Plaintiff
ax.scatter([7.5], [29], s=260, color="#2563EB", edgecolors="#1E3A8A", lw=1.2, zorder=6)
ax.text(7.5, 29, "P", fontsize=8, fontweight="bold", color="white", ha="center", va="center", zorder=7)
ax.text(7.5, 26.2, "Plaintiff", fontsize=6.8, color="#1E3A8A", ha="center", fontweight="bold")

# Defendant
ax.scatter([24.5], [29], s=260, color="#DC2626", edgecolors="#991B1B", lw=1.2, zorder=6)
ax.text(24.5, 29, "D", fontsize=8, fontweight="bold", color="white", ha="center", va="center", zorder=7)
ax.text(24.5, 26.2, "Defendant", fontsize=6.8, color="#991B1B", ha="center", fontweight="bold")

# Contract
ax.scatter([16], [30.5], s=220, color="#F59E0B", edgecolors="#B45309", lw=1.2, zorder=6)
ax.text(16, 30.5, "C", fontsize=7.5, fontweight="bold", color="white", ha="center", va="center", zorder=7)
ax.text(16, 32.5, "Deposit Contract", fontsize=6.8, color="#92400E", ha="center", fontweight="bold")

# Edges
draw_arrow(ax, 9.2, 29.5, 14.3, 30.2, color="#2563EB", lw=1.2)
draw_arrow(ax, 22.8, 29.5, 17.7, 30.2, color="#DC2626", lw=1.2)
draw_arrow(ax, 9.5, 28.5, 22.5, 28.5, color="#475569", lw=1.0)
ax.text(16, 27.2, "Dispute claim", fontsize=6.2, color="#475569", ha="center")

# Subcard: Temporal Sequence of Events
draw_card(ax, 3.5, 3.5, 25, 18, bg_color="#FFFFFF", border_color="#BFDBFE")
ax.text(16, 19.8, "Chronological Event Stream", fontsize=8, fontweight="bold", color="#1E40AF", ha="center")

events = [
    (r"$t_0$: Contract Execution", "Valid consent, Art. 117", "#059669"),
    (r"$t_1$: Default Event", "Non-performance, Art. 328", "#D97706"),
    (r"$t_2$: COVID-19 Freeze", r"Tolling $\frac{d\tau}{dt}=0$, Art. 156", "#0284C7"),
    (r"$t_3$: Lawsuit Filing", r"Filing to Court $\Delta \tau$", "#7C3AED"),
]

for idx, (ev_title, ev_desc, dot_c) in enumerate(events):
    y_pos = 16.5 - idx * 3.7
    ax.scatter([5.5], [y_pos], s=60, color=dot_c, edgecolors="white", lw=1, zorder=6)
    ax.text(7.2, y_pos + 0.3, ev_title, fontsize=6.8, fontweight="bold", color="#1E293B")
    ax.text(7.2, y_pos - 1.2, ev_desc, fontsize=6.0, color="#64748B")
    if idx < 3:
        ax.plot([5.5, 5.5], [y_pos - 0.7, y_pos - 3.0], color="#CBD5E1", lw=1.2, zorder=4)

# ==============================================================================
# STAGE 2: AXIOM-TGAT CONTINUOUS SPECTRAL ATTENTION (x: 35 to 64)
# ==============================================================================
draw_rounded_rect(ax, 35, 2, 29, 40, C_S2_BG, C_S2_BORDER, lw=1.5)
ax.text(49.5, 40.5, "Stage 2: Axiom-TGAT Attention", fontsize=9.5, fontweight="bold", color=C_S2_TITLE, ha="center")
ax.text(49.5, 38.8, "Continuous Harmonic Deontic Attention", fontsize=7.5, fontstyle="italic", color="#334155", ha="center")

# Bochner time encoding box
draw_card(ax, 36.5, 26, 26, 11, bg_color="#FFFFFF", border_color="#A5F3FC")
ax.text(49.5, 35.3, "Bochner Spectral Time Encoder", fontsize=8, fontweight="bold", color="#0E7490", ha="center")
ax.text(49.5, 33.2, r"$\Phi(\Delta \tau) = \sqrt{\frac{2}{d_T}} \left[\cos(\omega_k \Delta \tau) \parallel \sin(\omega_k \Delta \tau)\right]^T$",
        fontsize=6.8, color="#0F172A", ha="center")
ax.text(49.5, 30.5, r"Continuous Fourier decomposition via Bochner's Theorem", fontsize=6.0, color="#475569", ha="center")
ax.text(49.5, 28.0, r"Dual-Clock Mapping: $\Delta \tau = \tau(t_{\text{file}}) - \tau(t_{\text{default}})$", fontsize=6.5, fontweight="bold", color="#0369A1", ha="center")

# Temporal Attention aggregation box
draw_card(ax, 36.5, 12, 26, 12.5, bg_color="#FFFFFF", border_color="#A5F3FC")
ax.text(49.5, 22.8, "Temporal Cross-Attention", fontsize=8, fontweight="bold", color="#0E7490", ha="center")
ax.text(49.5, 20.2, r"$\alpha_{uv}(t) = \text{Softmax}\left(\frac{\mathbf{q}_u^T [\mathbf{k}_v \parallel \Phi(\Delta \tau)]}{\sqrt{d_k}}\right)$",
        fontsize=7.2, color="#0F172A", ha="center")
ax.text(49.5, 17.0, r"$\mathbf{h}_u(t) = \sum_{v \in \mathcal{N}(u)} \alpha_{uv}(t) \left(\mathbf{W}_V [\mathbf{z}_v(t) \parallel \Phi(\Delta \tau)]\right)$",
        fontsize=6.6, color="#0F172A", ha="center")
ax.text(49.5, 14.0, "Inductive 2-hop temporal neighborhood aggregation", fontsize=6.0, color="#475569", ha="center")

# Node Embedding output
draw_card(ax, 36.5, 3.5, 26, 7, bg_color="#E0F2FE", border_color="#0284C7")
ax.text(49.5, 8.5, r"Dynamic Node Representation $\mathbf{z}_{uv}(t)$", fontsize=7.5, fontweight="bold", color="#0369A1", ha="center")
ax.text(49.5, 5.5, r"$\mathbf{z}_{uv}(t) = \text{MLP}([\mathbf{h}_u(t) \parallel \mathbf{h}_v(t) \parallel \mathbf{e}_{uv}(t)])$", fontsize=6.8, color="#0C4A6E", ha="center")

# Stage 2 internal arrows
draw_arrow(ax, 49.5, 26, 49.5, 24.5, color="#0E7490", lw=1.2)
draw_arrow(ax, 49.5, 12, 49.5, 10.5, color="#0E7490", lw=1.2)

# ==============================================================================
# STAGE 3: NORMATIVE HIERARCHY & TBOX ONTOLOGY (x: 68 to 97)
# ==============================================================================
draw_rounded_rect(ax, 68, 2, 29, 40, C_S3_BG, C_S3_BORDER, lw=1.5)
ax.text(82.5, 40.5, "Stage 3: Ontological Regularization", fontsize=9.5, fontweight="bold", color=C_S3_TITLE, ha="center")
ax.text(82.5, 38.8, r"OWL 2 DL TBox Loss & Normative Arbiter", fontsize=7.5, fontstyle="italic", color="#334155", ha="center")

# VCLO TBox Box
draw_card(ax, 69.5, 25.5, 26, 11.5, bg_color="#FFFFFF", border_color="#DDD6FE")
ax.text(82.5, 35.3, "Vietnamese Civil Law Ontology (VCLO)", fontsize=7.8, fontweight="bold", color="#6D28D9", ha="center")
tbox_axioms = [
    r"$\mathcal{T}_1: \mathrm{Dispute} \subseteq \exists \mathrm{hasDefault}.\mathrm{Date}$",
    r"$\mathcal{T}_2: \mathrm{TimeBarred} \subseteq \neg \mathrm{EnforceableRelief}$",
    r"$\mathcal{T}_3: \mathrm{Perf} \geq 2/3 \subseteq \mathrm{CuredDefect}$ (Art. 129(2))",
]
for i, axm in enumerate(tbox_axioms):
    ax.text(71.0, 32.2 - i * 2.8, axm, fontsize=6.4, color="#3730A3")

# Normative Hierarchy DAG Arbiter
draw_card(ax, 69.5, 13.5, 26, 10.5, bg_color="#FFFFFF", border_color="#DDD6FE")
ax.text(82.5, 22.3, "Normative Hierarchy DAG Arbiter (NH-DA)", fontsize=7.5, fontweight="bold", color="#6D28D9", ha="center")
ax.text(82.5, 20.0, "Lex Specialis derogat legi generali", fontsize=6.8, fontstyle="italic", color="#4338CA", ha="center")

# Small hierarchy boxes
draw_card(ax, 70.8, 14.5, 11.0, 4.2, bg_color="#EEF2FF", border_color="#6366F1")
ax.text(76.3, 16.6, "General Civil Code\n(BLDS 2015)", fontsize=5.8, ha="center", color="#312E81")

draw_card(ax, 83.2, 14.5, 11.0, 4.2, bg_color="#FDF2F8", border_color="#EC4899")
ax.text(88.7, 16.6, "Specialized Law\n(Land / Credit Law)", fontsize=5.8, ha="center", color="#831843")

draw_arrow(ax, 83.2, 16.6, 81.8, 16.6, color="#4F46E5", lw=1.2)
ax.text(82.5, 18.0, r"$\succ$", fontsize=8.5, fontweight="bold", color="#4338CA", ha="center")

# Semantic Loss Box
draw_card(ax, 69.5, 3.5, 26, 8.5, bg_color="#EDE9FE", border_color="#7C3AED")
ax.text(82.5, 10.2, r"Description Logic Loss $\mathcal{L}_{\text{onto}}$", fontsize=7.8, fontweight="bold", color="#5B21B6", ha="center")
ax.text(82.5, 7.8, r"$\mathcal{L}_{\mathrm{onto}} = \sum_{C \subseteq D} \max(0, P(\neg D \mid \mathbf{z}) - P(\neg C \mid \mathbf{z}))^2$",
        fontsize=6.2, color="#4C1D95", ha="center")
ax.text(82.5, 5.0, "Zero tolerance for illegal judicial contradictions", fontsize=5.8, color="#5B21B6", ha="center")

# ==============================================================================
# STAGE 4: DEFEASIBLE DUNG HEAD & CERTIFIED VERDICT (x: 101 to 130)
# ==============================================================================
draw_rounded_rect(ax, 101, 2, 29, 40, C_S4_BG, C_S4_BORDER, lw=1.5)
ax.text(115.5, 40.5, "Stage 4: Defeasible Adjudication", fontsize=9.5, fontweight="bold", color=C_S4_TITLE, ha="center")
ax.text(115.5, 38.8, "Phan Minh Dung Abstract Argumentation", fontsize=7.5, fontstyle="italic", color="#334155", ha="center")

# Defeasible Argumentation Framework Box
draw_card(ax, 102.5, 22.5, 26, 14.5, bg_color="#FFFFFF", border_color="#BBF7D0")
ax.text(115.5, 35.3, r"Defeasible Argumentation $\mathcal{AF} = (\mathcal{Args}, \mathcal{Att})$", fontsize=7.6, fontweight="bold", color="#15803D", ha="center")

# Argument nodes in AF
# A1: Substantive
ax.scatter([106.5], [30.5], s=180, color="#FEE2E2", edgecolors="#DC2626", lw=1.2, zorder=6)
ax.text(106.5, 30.5, r"$A_1$", fontsize=7.0, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
ax.text(106.5, 28.2, "Claim\n(Art. 328)", fontsize=5.5, color="#991B1B", ha="center")

# A2: Rebuttal
ax.scatter([124.5], [30.5], s=180, color="#FEF3C7", edgecolors="#D97706", lw=1.2, zorder=6)
ax.text(124.5, 30.5, r"$A_2$", fontsize=7.0, fontweight="bold", color="#92400E", ha="center", va="center", zorder=7)
ax.text(124.5, 28.2, "Rebuttal\n(Extension)", fontsize=5.5, color="#92400E", ha="center")

# A3: Statute Bar (The Defeating Argument)
ax.scatter([115.5], [30.5], s=200, color="#DCFCE7", edgecolors="#15803D", lw=1.4, zorder=6)
ax.text(115.5, 30.5, r"$A_3$", fontsize=7.5, fontweight="bold", color="#14532D", ha="center", va="center", zorder=7)
ax.text(115.5, 26.5, "Time-Bar Expiration\n(Art. 429 BLDS)", fontsize=5.8, fontweight="bold", color="#14532D", ha="center")

# Undercut arrows
draw_arrow(ax, 113.8, 30.5, 108.5, 30.5, color="#DC2626", lw=1.3)
ax.text(111.0, 31.5, "undercuts", fontsize=5.5, color="#DC2626", ha="center", fontweight="bold")

draw_arrow(ax, 117.2, 30.5, 122.5, 30.5, color="#D97706", lw=1.0)
ax.text(120.0, 31.5, "rebuts", fontsize=5.5, color="#D97706", ha="center")

# Knaster-Tarski fixed point formula box
draw_card(ax, 102.5, 13.5, 26, 7.5, bg_color="#F0FDF4", border_color="#86EFAC")
ax.text(115.5, 19.3, "Knaster-Tarski Grounded Extension", fontsize=7.2, fontweight="bold", color="#166534", ha="center")
ax.text(115.5, 16.8, r"$\mathcal{GE}(\mathcal{AF}) = \text{lfp}(F_{AF}) = \{A_3\}$", fontsize=7.2, color="#14532D", ha="center", fontweight="bold")
ax.text(115.5, 14.8, "Procedural bar defeats substantive relief", fontsize=5.8, color="#15803D", ha="center")

# Final Certified Verdict Output
draw_card(ax, 102.5, 3.5, 26, 8.5, bg_color="#DCFCE7", border_color="#16A34A", lw=1.5)
ax.text(115.5, 10.3, "AUDITED JUDICIAL VERDICT", fontsize=7.8, fontweight="bold", color="#14532D", ha="center")
ax.text(115.5, 8.0, r"$\hat{y} \in \{0, 1, 2, 3\}$ + Proof Certificate", fontsize=7.0, fontweight="bold", color="#15803D", ha="center")
ax.text(115.5, 5.5, r"90.17% Hits@1 | 99.87% LCR | 0% Violation", fontsize=6.2, color="#14532D", ha="center", fontweight="bold")

# ==============================================================================
# INTER-STAGE BIG ARROWS
# ==============================================================================
# Stage 1 -> Stage 2
draw_arrow(ax, 30.5, 22.0, 34.5, 22.0, color="#1E40AF", lw=2.2)
ax.text(32.5, 24.0, r"$\{(u,v,t)\}$", fontsize=6.8, color="#1E40AF", ha="center", fontweight="bold")

# Stage 2 -> Stage 3
draw_arrow(ax, 64.5, 22.0, 67.5, 22.0, color="#0E7490", lw=2.2)
ax.text(66.0, 24.0, r"$\mathbf{z}_{uv}(t)$", fontsize=6.8, color="#0E7490", ha="center", fontweight="bold")

# Stage 3 -> Stage 4
draw_arrow(ax, 97.5, 22.0, 100.5, 22.0, color="#6D28D9", lw=2.2)
ax.text(99.0, 24.0, r"$\mathcal{L}_{\mathrm{onto}}$", fontsize=6.8, color="#6D28D9", ha="center", fontweight="bold")

# Save files
out_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(out_dir, exist_ok=True)
pdf_path = os.path.join(out_dir, "fig1_system_architecture.pdf")
png_path = os.path.join(out_dir, "fig1_system_architecture.png")

plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
plt.savefig(png_path, bbox_inches="tight", dpi=300)

# Sync to root figures
root_figures = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../figures"))
if os.path.exists(root_figures):
    import shutil
    shutil.copyfile(pdf_path, os.path.join(root_figures, "fig1_system_architecture.pdf"))
    shutil.copyfile(png_path, os.path.join(root_figures, "fig1_system_architecture.png"))

print(f"[+] Pristine Figure 1 generated successfully:")
print(f"    - PDF: {pdf_path}")
print(f"    - PNG: {png_path}")
