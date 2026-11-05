#!/usr/bin/env python3
"""
generate_fig3_dual_clock.py
Generates Figure 3: Dual-Clock Deontic Continuum & Continuous Bochner Harmonic Mapping.
Illustrates:
  (a) Physical Calendar Time t vs Jurisprudential Procedural Time tau(t):
      - Nominal flow (dtau/dt = 1)
      - Article 156 BLDS 2015 Force Majeure Tolling Freeze (dtau/dt = 0 during COVID-19 court suspension)
      - Article 157 BLDS 2015 Debt Acknowledgment Restart (tau(t) <- 0)
      - Article 429 BLDS 2015 3-Year Prescription Threshold (tau = 1,095 days)
  (b) Continuous Bochner Harmonic Embedding Phi(Delta tau):
      - Orthogonal Fourier basis across 3 frequency modes (omega_1, omega_2, omega_3)
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9.5,
    "axes.titlesize": 10.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "figure.titlesize": 11,
    "text.usetex": False,
    "figure.dpi": 300,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300, gridspec_kw={'width_ratios': [1.3, 1.0]})

# ==============================================================================
# SUBFIGURE (a): DUAL-CLOCK DEONTIC CONTINUUM
# ==============================================================================
# Timeline: 0 to 1,600 physical days
t = np.linspace(0, 1600, 1000)

# Build tau(t):
# Segment 1: [0, 400] nominal progression dtau/dt = 1 -> tau reaches 400
# Segment 2: [400, 650] Article 156 Tolling Freeze (COVID-19 Court Suspension) -> dtau/dt = 0, tau = 400
# Segment 3: [650, 950] nominal progression resumes -> tau reaches 400 + 300 = 700
# Segment 4: at t = 950, Article 157 Partial Debt Repayment / Acknowledgment -> Reset tau <- 0
# Segment 5: [950, 1600] post-restart progression -> tau reaches 650

tau = np.zeros_like(t)
for i, val in enumerate(t):
    if val <= 400:
        tau[i] = val
    elif val <= 650:
        tau[i] = 400.0  # Tolling Freeze
    elif val < 950:
        tau[i] = 400.0 + (val - 650.0)
    else:
        tau[i] = (val - 950.0)  # Restart from 0

# Unconstrained naive calendar time (what vanilla GNNs and LLMs use)
naive_tau = t.copy()

# Plot naive time vs actual jurisprudential time
ax1.plot(t, naive_tau, color="#9E9E9E", linestyle=":", linewidth=1.5, label=r"Naive Calendar Time $t$ (No Tolling)")
ax1.plot(t, tau, color="#0072B2", linewidth=2.2, label=r"Procedural Continuum $\tau(t)$ (SynapseLex)")

# Statutory limitation line: 1,095 days (Art. 429)
ax1.axhline(1095, color="#D55E00", linestyle="--", linewidth=1.4, alpha=0.9, label=r"Art. 429 Time-Bar ($1,095\text{ d} / 3\text{ yr}$)")

# Tolling Freeze shaded region [400, 650]
ax1.axvspan(400, 650, color="#E0F2FE", alpha=0.7, zorder=0)
ax1.text(525, 180, "Art. 156 Tolling Freeze\n(COVID-19 decree,\n" + r"$\frac{d\tau}{dt} = 0$)",
         fontsize=7.2, color="#0369A1", ha="center", va="center",
         bbox=dict(boxstyle="round,pad=0.2", fc="#BAE6FD", ec="#0284C7", lw=0.7, alpha=0.85))

# Debt acknowledgment reset annotation at t = 950
ax1.annotate(r"Art. 157 Restart" + "\n" + r"($\tau \leftarrow 0$)",
             xy=(950, 0), xytext=(820, 280),
             arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2),
             fontsize=7.5, color="#065F46", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#D1FAE5", ec="#10B981", lw=0.7, alpha=0.85))

# Procedural amnesia failure annotation for naive baseline at t = 1,150
ax1.annotate("Vanilla GNN / LLM Failure:\nPremature Statute Dismissal\n(Naive $t > 1,095$ days)",
             xy=(1150, 1150), xytext=(1100, 780),
             arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.2),
             fontsize=7.2, color="#991B1B",
             bbox=dict(boxstyle="round,pad=0.2", fc="#FEE2E2", ec="#EF4444", lw=0.7, alpha=0.85))

ax1.set_xlim(0, 1600)
ax1.set_ylim(-50, 1450)
ax1.set_xlabel("Physical Calendar Time $t$ (Days elapsed)", fontsize=9, fontweight="semibold")
ax1.set_ylabel(r"Procedural Time $\tau(t)$ (Days)", fontsize=9, fontweight="semibold")
ax1.set_title(r"(a) Dual-Clock Deontic Continuum $\tau(t)$", fontsize=9.5, fontweight="bold", pad=6)
ax1.grid(True, linestyle=":", alpha=0.5, color="#BDBDBD")
ax1.legend(loc="upper left", framealpha=0.9, fontsize=7.2)

# ==============================================================================
# SUBFIGURE (b): BOCHNER HARMONIC EMBEDDING BASIS
# ==============================================================================
# Plot harmonic Fourier bases: cos(omega_k * Delta tau)
delta_tau = np.linspace(0, 365, 400)
freqs = [1.0 / 14.0, 1.0 / 90.0, 1.0 / 365.0]  # Bi-weekly, quarterly, annual harmonics
colors = ["#7C3AED", "#2563EB", "#059669"]
labels = [r"Bi-weekly ($\omega_1 = \frac{2\pi}{14}$)", r"Quarterly ($\omega_2 = \frac{2\pi}{90}$)", r"Annual ($\omega_3 = \frac{2\pi}{365}$)"]

for freq, c, lab in zip(freqs, colors, labels):
    phi_k = np.cos(2 * np.pi * freq * delta_tau)
    ax2.plot(delta_tau, phi_k, color=c, linewidth=1.8, label=lab)

ax2.set_xlim(0, 365)
ax2.set_ylim(-1.25, 1.35)
ax2.set_xlabel(r"Elapsed Interval $\Delta \tau$ (Days)", fontsize=9, fontweight="semibold")
ax2.set_ylabel(r"Continuous Basis $\cos(\omega_k \Delta \tau)$", fontsize=9, fontweight="semibold")
ax2.set_title(r"(b) Continuous Bochner Fourier Bases $\Phi(\Delta \tau)$", fontsize=9.5, fontweight="bold", pad=6)
ax2.grid(True, linestyle=":", alpha=0.5, color="#BDBDBD")
ax2.legend(loc="lower right", framealpha=0.9, fontsize=7.2)

plt.tight_layout()

out_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(out_dir, exist_ok=True)
pdf_path = os.path.join(out_dir, "fig3_bochner_dual_clock.pdf")
png_path = os.path.join(out_dir, "fig3_bochner_dual_clock.png")

plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
plt.savefig(png_path, bbox_inches="tight", dpi=300)

root_fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../figures"))
if os.path.exists(root_fig_dir):
    import shutil
    shutil.copyfile(pdf_path, os.path.join(root_fig_dir, "fig3_bochner_dual_clock.pdf"))
    shutil.copyfile(png_path, os.path.join(root_fig_dir, "fig3_bochner_dual_clock.png"))

print(f"[+] Successfully generated pristine vector Dual-Clock Bochner figure:")
print(f"    - PDF: {pdf_path}")
print(f"    - PNG: {png_path}")
