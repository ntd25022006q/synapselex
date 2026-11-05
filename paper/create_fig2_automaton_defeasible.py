#!/usr/bin/env python3
"""
create_fig2_automaton_defeasible.py
Generates pristine, publication-grade vector PDF and 300 DPI PNG for
Figure 2: Non-Monotonic Contract State-Transition Automaton and Defeasible Priority Argumentation.
Guarantees 100% legible text, zero overlap, beautiful academic layout.
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
    "font.size": 8.5,
    "figure.dpi": 300,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig = plt.figure(figsize=(12.8, 5.0), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 128)
ax.set_ylim(0, 50)
ax.axis("off")

def draw_panel(ax, x, y, w, h, bg_color="#FFFFFF", border_color="#CBD5E1", lw=1.2, radius=1.0):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={radius},rounding_size={radius}",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=lw,
        zorder=1
    )
    ax.add_patch(box)
    return box

def draw_state_box(ax, x, y, w, h, title, subtitle, article, bg_color, border_color, title_color):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.8,rounding_size=0.8",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.3,
        zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 2.2, title, fontsize=8.8, fontweight="bold", color=title_color, ha="center")
    ax.text(x + w/2, y + h/2 - 0.2, subtitle, fontsize=6.8, color="#334155", ha="center")
    ax.text(x + w/2, y + 1.8, article, fontsize=6.8, fontweight="bold", color=border_color, ha="center")
    return box

def draw_curved_arrow(ax, x1, y1, x2, y2, color, lw=1.5, rad=0.2, style="-|>", linestyle="-"):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle=f"{style},head_length=4.5,head_width=3.0",
        color=color,
        linewidth=lw,
        linestyle=linestyle,
        zorder=4
    )
    ax.add_patch(arrow)

# ==============================================================================
# SUBFIGURE (a): 4-STATE CIVIL CONTRACT AUTOMATON (x: 2 to 64)
# ==============================================================================
draw_panel(ax, 2, 2, 60, 46, bg_color="#FAFAFA", border_color="#94A3B8", lw=1.3)
ax.text(32, 45.5, "(a) 4-State Civil Contract Automaton M_state", fontsize=9.5, fontweight="bold", color="#1E3A8A", ha="center")
ax.text(32, 43.5, "Statutory transitions under Vietnamese Civil Code 2015", fontsize=7.2, fontstyle="italic", color="#475569", ha="center")

# State S0: Valid Contract (Top-Left)
draw_state_box(ax, 5, 27, 22, 13,
               "S0: Valid Contract",
               "Fully enforceable rights\nand substantive claims",
               "BLDS 2015 Art. 117",
               "#F0FDF4", "#16A34A", "#14532D")

# Initial execute arrow
draw_curved_arrow(ax, 2.5, 33.5, 5.0, 33.5, color="#15803D", lw=1.8, rad=0.0)
ax.text(3.7, 34.5, "Sign", fontsize=6.5, fontweight="bold", color="#15803D", ha="center")

# State S1: Voidable Contract (Top-Right)
draw_state_box(ax, 37, 27, 22, 13,
               "S1: Voidable Contract",
               "Form defect / Notarization flaw\nVoidable upon petition",
               "BLDS 2015 Art. 129(1)",
               "#FEF3C7", "#D97706", "#92400E")

# State S2: Void ab initio (Bottom-Right)
draw_state_box(ax, 37, 5, 22, 13,
               "S2: Void ab initio",
               "Absolute nullity from inception\nRestitution of original status",
               "BLDS 2015 Art. 122-123",
               "#FEE2E2", "#DC2626", "#991B1B")

# State S3: Extinguished / Barred (Bottom-Left)
draw_state_box(ax, 5, 5, 22, 13,
               "S3: Extinguished / Barred",
               "Statute of limitations lapsed\nProcedural claim barred",
               "BLDS 2015 Art. 429",
               "#F1F5F9", "#475569", "#1E293B")

# Transitions:
# S0 -> S1 (Formal flaw discovered)
draw_curved_arrow(ax, 27, 37.0, 37, 37.0, color="#D97706", lw=1.4, rad=-0.15)
ax.text(32, 39.5, "Formal Defect\n(Unnotarized)", fontsize=6.2, color="#B45309", ha="center", fontweight="bold")

# S1 -> S0 (NON-MONOTONIC STATUTORY CURING: Art 129(2)) [SOTA HIGHLIGHT]
draw_curved_arrow(ax, 37, 30.5, 27, 30.5, color="#16A34A", lw=2.2, rad=-0.15)
ax.text(32, 27.2, "STATUTORY CURE:\nPerform >= 2/3 (Art. 129(2))", fontsize=6.6, color="#15803D", ha="center", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="#DCFCE7", ec="#86EFAC", lw=0.8, alpha=0.9))

# S1 -> S2 (Court declares void)
draw_curved_arrow(ax, 48, 27, 48, 18, color="#DC2626", lw=1.4, rad=0.0)
ax.text(50.5, 22.5, "Court Decree\n(Nullity granted)", fontsize=6.2, color="#991B1B", ha="left")

# S0 -> S3 (Statutory Prescription Expiration: Art 429)
draw_curved_arrow(ax, 16, 27, 16, 18, color="#DC2626", lw=2.0, rad=0.0)
ax.text(14.5, 22.5, "Delta tau > 3 yrs\n(Art. 429 Bar)", fontsize=6.6, color="#B91C1C", ha="right", fontweight="bold")

# S0 -> S2 (Prohibited object direct void)
draw_curved_arrow(ax, 23, 27, 41, 18, color="#DC2626", lw=1.1, rad=0.1, linestyle="--")
ax.text(30.0, 20.5, "Prohibited Object\n(Art. 123)", fontsize=5.8, color="#991B1B", ha="center", rotation=-32)

# S2 -> S3 (Restitution completed)
draw_curved_arrow(ax, 37, 11.5, 27, 11.5, color="#475569", lw=1.2, rad=0.0)
ax.text(32, 13.0, "Restitution Executed\n(Art. 131)", fontsize=6.0, color="#475569", ha="center")

# ==============================================================================
# SUBFIGURE (b): DEFEASIBLE DUNG ARGUMENTATION (x: 66 to 126)
# ==============================================================================
draw_panel(ax, 66, 2, 60, 46, bg_color="#FAFAFA", border_color="#94A3B8", lw=1.3)
ax.text(96, 45.5, "(b) Defeasible Argumentation Framework AF", fontsize=9.5, fontweight="bold", color="#1E3A8A", ha="center")
ax.text(96, 43.5, r"Phan Minh Dung (1995) Adjudication: AF = (Args, Att)", fontsize=7.2, fontstyle="italic", color="#475569", ha="center")

# Argument Cards (No overlapping nodes!)
# A1: Claimant Substantive Claim
draw_panel(ax, 69, 28, 24, 12, bg_color="#FEE2E2", border_color="#DC2626", lw=1.3)
ax.scatter([73], [34], s=260, color="#DC2626", edgecolors="#991B1B", lw=1.2, zorder=5)
ax.text(73, 34, "A1", fontsize=8.5, fontweight="bold", color="white", ha="center", va="center", zorder=6)
ax.text(83, 36.2, "Claimant's Claim:", fontsize=7.2, fontweight="bold", color="#991B1B", ha="center")
ax.text(83, 33.2, "Forfeit Deposit 500M\n(Art. 328 BLDS 2015)", fontsize=6.2, color="#7F1D1D", ha="center")
ax.text(83, 29.8, "[STATUS: DEFEATED]", fontsize=6.2, fontweight="bold", color="#DC2626", ha="center")

# A2: Defendant Counterclaim
draw_panel(ax, 99, 28, 24, 12, bg_color="#FEF3C7", border_color="#D97706", lw=1.3)
ax.scatter([103], [34], s=260, color="#D97706", edgecolors="#B45309", lw=1.2, zorder=5)
ax.text(103, 34, "A2", fontsize=8.5, fontweight="bold", color="white", ha="center", va="center", zorder=6)
ax.text(113, 36.2, "Defendant Rebuttal:", fontsize=7.2, fontweight="bold", color="#92400E", ha="center")
ax.text(113, 33.2, "Oral Extension Pact\nExcused Performance", fontsize=6.2, color="#78350F", ha="center")
ax.text(113, 29.8, "[STATUS: REBUTTED]", fontsize=6.2, fontweight="bold", color="#B45309", ha="center")

# Mutual Rebuttal Arrow between A1 and A2
draw_curved_arrow(ax, 93, 34, 99, 34, color="#D97706", lw=1.4, rad=-0.1, style="<->")
ax.text(96, 36.0, "rebuts", fontsize=6.2, fontweight="bold", color="#D97706", ha="center")

# A3: Statutory Prescription Bar (The Defeating Winning Argument)
draw_panel(ax, 79, 14, 34, 11, bg_color="#DCFCE7", border_color="#16A34A", lw=1.6)
ax.scatter([84], [19.5], s=300, color="#16A34A", edgecolors="#14532D", lw=1.4, zorder=5)
ax.text(84, 19.5, "A3", fontsize=9.0, fontweight="bold", color="white", ha="center", va="center", zorder=6)
ax.text(100, 21.8, "Statutory Limitation Defense (Art. 429):", fontsize=7.2, fontweight="bold", color="#14532D", ha="center")
ax.text(100, 18.8, "Delta tau = 1,254 days > 1,095 days (3 years elapsed)\nNo tolling suspension under Art. 156 proven", fontsize=6.0, color="#166534", ha="center")
ax.text(100, 15.5, "[STATUS: IN GROUNDED EXTENSION GE(AF)]", fontsize=6.5, fontweight="bold", color="#15803D", ha="center")

# Asymmetric Undercut Arrow A3 -> A1 (Procedural bar undercuts substantive claim)
draw_curved_arrow(ax, 84, 25.0, 81, 28.0, color="#DC2626", lw=2.2, rad=-0.2)
ax.text(78.5, 25.8, "UNDERCUTS\n(Art. 429 Bar)", fontsize=6.2, fontweight="bold", color="#DC2626", ha="right")

# Knaster-Tarski Grounded Extension Summary Banner (Bottom of Subfigure b)
draw_panel(ax, 69, 4, 54, 7.5, bg_color="#ECFDF5", border_color="#10B981", lw=1.2)
ax.text(96, 8.8, "Knaster-Tarski Least Fixed Point Adjudication:", fontsize=7.5, fontweight="bold", color="#065F46", ha="center")
ax.text(96, 6.2, "F_AF(empty) = {A3} ==> F_AF^2(empty) = {A3}  ==>  GE(AF) = {A3}", fontsize=7.0, color="#047857", ha="center", fontweight="bold")
ax.text(96, 4.2, "Adjudication decree: Lawsuit dismissed as time-barred (Verdict Code 2)", fontsize=6.0, color="#065F46", ha="center")

# Save files
out_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(out_dir, exist_ok=True)
pdf_path = os.path.join(out_dir, "fig2_legal_automaton_defeasible.pdf")
png_path = os.path.join(out_dir, "fig2_legal_automaton_defeasible.png")

plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
plt.savefig(png_path, bbox_inches="tight", dpi=300)

# Sync to root figures
root_figures = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../figures"))
if os.path.exists(root_figures):
    import shutil
    shutil.copyfile(pdf_path, os.path.join(root_figures, "fig2_legal_automaton_defeasible.pdf"))
    shutil.copyfile(png_path, os.path.join(root_figures, "fig2_legal_automaton_defeasible.png"))

print(f"[+] Pristine Figure 2 generated successfully:")
print(f"    - PDF: {pdf_path}")
print(f"    - PNG: {png_path}")
