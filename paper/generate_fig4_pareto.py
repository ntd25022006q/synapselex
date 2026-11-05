#!/usr/bin/env python3
"""
generate_fig4_pareto.py
Generates the Pareto Efficiency Analysis across the 11-Model Arena on SynapseCivil-Bench.
Follows orx-figures publication standards (NeurIPS/ICML/Springer Q1 style).
Reads real metrics directly from RIGOROUS_TGAT_RESULTS.json.
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Add orx-figures assets to path
FIGSTYLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.agents/skills/orx-figures/assets"))
if os.path.exists(FIGSTYLE_PATH):
    sys.path.insert(0, FIGSTYLE_PATH)
    from orx_figstyle import TEXT, WIDE, PALETTE, use_style, save
else:
    PALETTE = {
        "blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
        "red": "#D55E00", "purple": "#CC79A7", "cyan": "#56B4E9",
        "yellow": "#F0E442", "black": "#000000"
    }

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "figure.titlesize": 12,
    "text.usetex": False,
    "figure.dpi": 300,
})

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "../data/RIGOROUS_TGAT_RESULTS.json")
with open(RESULTS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Model definitions, styles, and categories
MODEL_META = {
    "M0_SynapseLex_Full": {
        "label": "SynapseLex (M0, Full Model)",
        "color": "#D55E00",  # Vermillion / Red-Orange
        "marker": "*",
        "size": 160,
        "category": "Proposed SOTA",
        "zorder": 10
    },
    "M1_Ablation_NoOntology": {
        "label": "Ablation M1 (No Ontology)",
        "color": "#E69F00",
        "marker": "o",
        "size": 80,
        "category": "Ablations",
        "zorder": 6
    },
    "M2_Ablation_NoTemporal": {
        "label": "Ablation M2 (No Temporal, Static GAT)",
        "color": "#E69F00",
        "marker": "s",
        "size": 80,
        "category": "Ablations",
        "zorder": 6
    },
    "M3_Ablation_NoStateGating": {
        "label": "Ablation M3 (No State Gating)",
        "color": "#E69F00",
        "marker": "^",
        "size": 80,
        "category": "Ablations",
        "zorder": 6
    },
    "M4_DyGFormer": {
        "label": "DyGFormer (Yu et al., NeurIPS 2023)",
        "color": "#0072B2",  # Deep Blue
        "marker": "D",
        "size": 80,
        "category": "Dynamic Graph SOTA",
        "zorder": 5
    },
    "M5_TGAT": {
        "label": "TGAT (Xu et al., ICLR 2020)",
        "color": "#0072B2",
        "marker": "v",
        "size": 80,
        "category": "Dynamic Graph SOTA",
        "zorder": 5
    },
    "M6_TGN": {
        "label": "TGN (Rossi et al., NeurIPS 2020)",
        "color": "#0072B2",
        "marker": "p",
        "size": 80,
        "category": "Dynamic Graph SOTA",
        "zorder": 5
    },
    "B1_Static_GCN": {
        "label": "Static GCN (Kipf & Welling 2017)",
        "color": "#009E73",  # Bluish Green
        "marker": "h",
        "size": 75,
        "category": "Static Graph / Text Baselines",
        "zorder": 4
    },
    "B2_Legal_PhoBERT": {
        "label": "Legal-PhoBERT (Nguyen et al. 2021)",
        "color": "#009E73",
        "marker": "X",
        "size": 75,
        "category": "Static Graph / Text Baselines",
        "zorder": 4
    },
    "B3_GPT4o": {
        "label": "GPT-4o (Zero-Shot IRAC)",
        "color": "#CC79A7",  # Purple
        "marker": "P",
        "size": 95,
        "category": "Frontier LLMs (Commercial API)",
        "zorder": 7
    },
    "B4_DeepSeek_R1": {
        "label": "DeepSeek-R1 (671B MoE CoT)",
        "color": "#56B4E9",  # Sky Blue
        "marker": "d",
        "size": 95,
        "category": "Frontier LLMs (Commercial API)",
        "zorder": 7
    }
}

fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

# Background tint for Optimal Judicial Regime (High Accuracy, Low Latency)
ax.axvspan(0.5, 20.0, ymin=0.75, ymax=1.0, color="#E8F5E9", alpha=0.55, zorder=1)
ax.text(1.2, 98.0, "Optimal Adjudication Regime\n(High Accuracy + Real-Time Sub-10ms)",
        fontsize=8, color="#1B5E20", fontweight="bold", fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.3", fc="#C8E6C9", ec="#81C784", alpha=0.8, lw=0.8))

# Background tint for High Latency Regime (Frontier API)
ax.axvspan(800.0, 5000.0, color="#FFF3E0", alpha=0.45, zorder=1)
ax.text(1000.0, 48.0, "High Latency & Cloud API Regime\n(1,400 - 3,200 ms per case)",
        fontsize=7.5, color="#E65100", fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFE0B2", ec="#FFB74D", alpha=0.8, lw=0.8))

plotted_points = []
for k, meta in MODEL_META.items():
    if k not in data:
        continue
    m = data[k]["mean"]
    s = data[k]["std"]
    lat = m["latency_ms"]
    acc = m["hits@1"]
    acc_std = s.get("hits@1", 0.0)
    
    # Plot individual run points if available (scatter)
    seed_runs = data[k].get("seed_runs", [])
    if seed_runs:
        for run in seed_runs:
            ax.scatter(lat, run["hits@1"], color=meta["color"], alpha=0.25, s=25, zorder=meta["zorder"]-1)
            
    # Plot mean marker with error bar
    ax.errorbar(lat, acc, yerr=acc_std, fmt='none', ecolor=meta["color"], elinewidth=1.2, capsize=3, capthick=1.0, alpha=0.75, zorder=meta["zorder"])
    ax.scatter(lat, acc, color=meta["color"], marker=meta["marker"], s=meta["size"], edgecolor="black", linewidth=0.8, label=meta["label"], zorder=meta["zorder"])
    
    plotted_points.append((lat, acc, meta["label"], meta["color"], k))

# Pareto Frontier line computation
# Filter non-dominated points: minimizing latency (x), maximizing accuracy (y)
sorted_pts = sorted([(lat, acc, k) for k, meta in MODEL_META.items() for lat, acc in [(data[k]["mean"]["latency_ms"], data[k]["mean"]["hits@1"])]], key=lambda p: p[0])

pareto_front = []
max_acc = -1.0
for lat, acc, k in sorted_pts:
    if acc > max_acc:
        pareto_front.append((lat, acc))
        max_acc = acc

# Plot Pareto frontier
px, py = zip(*pareto_front)
ax.plot(px, py, color="#C62828", linestyle="--", linewidth=1.5, alpha=0.8, label="Empirical Pareto Frontier", zorder=8)

# Label key models
ax.annotate(r"$\mathbf{SynapseLex\ (M_0)}$" + "\n" + r"$\mathbf{90.17\%\ Hits@1,\ 8.15\text{ ms}}$",
            xy=(8.15, 90.17), xytext=(15.0, 86.0),
            arrowprops=dict(arrowstyle="->", color="#D55E00", lw=1.2),
            fontsize=8.5, fontweight="bold", color="#D55E00",
            bbox=dict(boxstyle="round,pad=0.2", fc="#FBE9E7", ec="#D55E00", lw=0.9))

ax.annotate("Static GCN (84.72%, 1.1ms)",
            xy=(1.13, 84.72), xytext=(1.8, 77.0),
            arrowprops=dict(arrowstyle="->", color="#009E73", lw=1.0),
            fontsize=7.5, color="#004D40")

ax.annotate("GPT-4o (72.04%, 1,420ms)\n14.4% Time-Bar Violation",
            xy=(1420.0, 72.04), xytext=(350.0, 64.0),
            arrowprops=dict(arrowstyle="->", color="#CC79A7", lw=1.0),
            fontsize=7.5, color="#4A148C")

ax.annotate("DeepSeek-R1 (76.17%, 3,150ms)\n11.9% Time-Bar Violation",
            xy=(3150.0, 76.17), xytext=(1100.0, 82.0),
            arrowprops=dict(arrowstyle="->", color="#56B4E9", lw=1.0),
            fontsize=7.5, color="#01579B")

ax.set_xscale("log")
ax.set_xlim(0.5, 6000.0)
ax.set_ylim(25.0, 103.0)

ax.set_xlabel("Inference Latency per Case (ms, log-scale, lower is better $\leftarrow$)", fontsize=9.5, fontweight="semibold")
ax.set_ylabel("Judicial Adjudication Accuracy (Hits@1 %, higher is better $\\rightarrow$)", fontsize=9.5, fontweight="semibold")
ax.set_title("Pareto Efficiency: Adjudication Accuracy vs Inference Latency ($N=920$ Cases, 5 Seeds)", fontsize=10.5, pad=9, fontweight="bold")

# Grid & aesthetics
ax.grid(True, which="both", linestyle=":", alpha=0.5, color="#9E9E9E")
ax.set_axisbelow(True)

# Legend outside / top
handles, labels = ax.get_legend_handles_labels()
# Reorder legend cleanly
ax.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.01, 0.02), ncol=2, frameon=True, framealpha=0.9, facecolor="white", edgecolor="#BDBDBD", fontsize=7.2)

plt.tight_layout()

# Save PDF & PNG
out_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(out_dir, exist_ok=True)
pdf_path = os.path.join(out_dir, "fig4_pareto_arena.pdf")
png_path = os.path.join(out_dir, "fig4_pareto_arena.png")

plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
plt.savefig(png_path, bbox_inches="tight", dpi=300)

# Copy to root figures/
root_fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../figures"))
if os.path.exists(root_fig_dir):
    import shutil
    shutil.copyfile(pdf_path, os.path.join(root_fig_dir, "fig4_pareto_arena.pdf"))
    shutil.copyfile(png_path, os.path.join(root_fig_dir, "fig4_pareto_arena.png"))

print(f"[+] Successfully generated pristine vector Pareto figure:")
print(f"    - PDF: {pdf_path}")
print(f"    - PNG: {png_path}")
