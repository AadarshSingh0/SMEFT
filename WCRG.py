import numpy as np
import matplotlib.pyplot as plt

INV_V2 = 1.0 / 0.24622**2   # 1/v^2 in TeV^-2 (= 16.50); global-fit c's are in units of 1/v^2


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
unitarity_1f = (2 * np.pi / (sqrt_s**2)) * 1e6   # TeV^-2, single-flavour [C_ll]_2222
unitarity_2f = (4 * np.pi / (sqrt_s**2)) * 1e6   # TeV^-2, two-flavour [C_ll]_2233, [C_ll]_2332

# NA64mu (arXiv:2511.11801, Table 1, 90% CL) in our normalisation:
# the 2222 bounds are halved (NA64mu follows Falkowski et al., factor 1/2 in [O_ll]_2222)
na64_current_2222 = 1e4 / 2
na64_current_2233 = 1e4
na64_future_2222  = 1.7e2 / 2
na64_future_2233  = 1.3e2

# (label, value, colour, linestyle, unitarity prefactor: 2*pi for 2222, 4*pi for 2233/2332)
bounds = [
    (r"NA64 current ($\hat{C}_{ll}^{2222}$)", na64_current_2222, "orange", "-",  2 * np.pi),
    (r"NA64 current ($C_{ll}^{2233}$)",       na64_current_2233, "orange", "-.", 4 * np.pi),
    (r"NA64 future ($\hat{C}_{ll}^{2222}$)",  na64_future_2222,  "orange", "--", 2 * np.pi),
    (r"NA64 future ($C_{ll}^{2233}$)",        na64_future_2233,  "orange", ":",  4 * np.pi),
    (r"Global fit ($\hat{C}_{ll}^{2222}$)",   0.23 * INV_V2 / 2, "blue",   "-",  2 * np.pi),
    (r"Global fit ($C_{ll}^{2332}$)",         0.053 * INV_V2,    "blue",   "--", 4 * np.pi),
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
    # ("HL-LHC",      14000.0,  "gray"),
]

# -------------------------------------------------
# Figure (single panel — exactly what you asked for)
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 6.0))

# Unitarity
ax.loglog(sqrt_s, unitarity_1f, color="red", lw=2.5, label=r"Unitarity $2\pi/s$ ($C_{ll}^{2222}$)")
ax.loglog(sqrt_s, unitarity_2f, color="red", lw=2.5, ls="--",
          label=r"Unitarity $4\pi/s$ ($C_{ll}^{2233}$, $C_{ll}^{2332}$)")

# Horizontal bounds + crossing points (each with its own unitarity line)
for label, y, color, ls, upref in bounds:
    ax.hlines(y, xmin=sqrt_s.min(), xmax=sqrt_s.max(),
              colors=color, linestyles=ls, linewidth=2.2, label=label)
    s_cross = np.sqrt(upref * 1e6 / y)
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

ax.legend(loc=(0.05,0.05), fontsize=9, frameon=True, fancybox=False, edgecolor="0.8")

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
for label, y, _, _, upref in bounds:
    s_cross = np.sqrt(upref * 1e6 / y)
    print(f"  {label}: √s_cross ≈ {s_cross:.3g} GeV")