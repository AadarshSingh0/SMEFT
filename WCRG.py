import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PRD-style single-panel plot (clean, publication-ready)
# -------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 13,
    "mathtext.fontset": "cm",
    "axes.labelsize": 13,
    "axes.titlesize": 13,
    "legend.fontsize": 10.5,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "lines.linewidth": 2.2,
})

# -------------------------------------------------
# Data
# -------------------------------------------------
sqrt_s = np.logspace(-1, 4.5, 800)
unitarity = (2 * np.pi / (sqrt_s**2)) * 1e6   # TeV^{-2}

# Horizontal bounds (exactly as you used in your original scripts)
# NA64 gives IDENTICAL current/future bounds for Ĉ_ll^{2222} and Ĉ_ll^{2233}
# (confirmed in arXiv:2511.11801, Table I & Fig. 5)
na64_current = 1e4
na64_future  = 1.4e2

bounds = [
    (r"NA64 current ($\hat{C}_{ll}^{2222}$ & $C_{ll}^{2233}$)", na64_current, "orange", "-"),
    (r"NA64 future ($\hat{C}_{ll}^{2222}$ & $C_{ll}^{2233}$)",  na64_future,  "orange", "--"),
    (r"Global fit ($\hat{C}_{ll}^{2222}$)",                          0.23,         "blue",   "-"),
    (r"Global fit ($C_{ll}^{2332}$)",                          0.053,        "blue",   "--"),
]

# Vertical guide lines
exp_scales = [
    ("NA64",          0.10,   "orange"),
    ("LEP / Global fit\n(μ = m_Z)", 91.0,   "blue"),
    ("FCC-ee",        365.0,  "gray"),
    ("CEPC",          240.0,  "gray"),
    ("ILC",           500.0,  "gray"),
    ("CLIC",         3000.0,  "gray"),
    ("MuC",         10000.0,  "gray"),
    ("HL-LHC",      14000.0,  "gray"),
]

# -------------------------------------------------
# Figure (single panel — exactly what you asked for)
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 6.0))

# Unitarity
ax.loglog(sqrt_s, unitarity, color="red", lw=2.5, label="Unitarity")

# Horizontal bounds + crossing points
for label, y, color, ls in bounds:
    ax.hlines(y, xmin=sqrt_s.min(), xmax=sqrt_s.max(),
              colors=color, linestyles=ls, linewidth=2.2, label=label)
    s_cross = np.sqrt(2 * np.pi * 1e6 / y)
    if sqrt_s.min() < s_cross < sqrt_s.max():
        ax.plot(s_cross, y, "o", color=color, ms=6, zorder=5)

# Vertical guides
y_text_pos = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-3, 1e-4]
for i, (label, x, color) in enumerate(exp_scales):
    ax.axvline(x, color=color, ls=":", lw=1.1, alpha=0.65)
    ax.text(x * 1.04, y_text_pos[i % len(y_text_pos)], label,
            rotation=90, va="bottom", ha="left", fontsize=11.5,
            color=color, bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=1.0))

# Axes
ax.set_xlabel(r"$\sqrt{s}\ \mathrm{[GeV]}$", fontsize=15)
ax.set_ylabel(r"$|C_{ll}|/\Lambda^2\ \mathrm{[TeV^{-2}]}$", fontsize=15)

ax.set_xlim(9e-2, 3e4)
ax.set_ylim(1e-6, 1e5)

ax.grid(True, which="major", axis="both", alpha=0.25)
ax.grid(False, which="minor")

ax.legend(loc="upper right", fontsize=9, frameon=True, fancybox=False, edgecolor="0.8")

# Caption-ready title (you can remove or edit)
# ax.text(0.03, 0.93, "NA64μ vs global fit on $\hat{C}_{ll}$ (μ-τ sector)",
#         transform=ax.transAxes, fontsize=11, fontstyle="italic")

plt.tight_layout()
# plt.savefig("wilson_comparison_single_panel_PRD.pdf", dpi=600, bbox_inches="tight")
plt.savefig("wilson_comparison_with_unitarity.png", dpi=600, bbox_inches="tight")

plt.show()

# -------------------------------------------------
# Crossing scales (for your reference)
# -------------------------------------------------
print("\nCrossing scales with unitarity:")
for label, y, _, _ in bounds:
    s_cross = np.sqrt(2 * np.pi * 1e6 / y)
    print(f"  {label}: √s_cross ≈ {s_cross:.3g} GeV")