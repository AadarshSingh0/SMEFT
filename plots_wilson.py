import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
plt.rcParams.update({'font.size': 11, 'font.family': 'serif', 
                     'mathtext.fontset': 'stix', 'axes.linewidth': 1.2})

# ==================== INPUT NUMBERS ====================
c_hat_2222_current = 0.23
c_2332_current = 0.053

# NA64 bounds (TeV^-2)
na64_2222_current_gev2 = 1e4
na64_2222_future_gev2  = 1.4e2
na64_2233_current_gev2 = 1e4
na64_2233_future_gev2  = 1.4e2

# ==================== DATA ====================
data = [
    { "label": r"$\hat{C}_{\ell\ell}^{2222}$", "na64_cur": na64_2222_current_gev2, 
      "na64_fut": na64_2222_future_gev2, "coll": c_hat_2222_current },
    { "label": r"$C_{\ell\ell}^{2233}$", "na64_cur": na64_2233_current_gev2, 
      "na64_fut": na64_2233_future_gev2, "coll": 0 },
    { "label": r"$C_{\ell\ell}^{2332}$", "na64_cur": 0, "na64_fut": 0, 
      "coll": c_2332_current }
]

labels = [d["label"] for d in data]
na64_cur = [d["na64_cur"] for d in data]
na64_fut = [d["na64_fut"] for d in data]
coll    = [d["coll"] for d in data]

x = np.arange(len(labels))
width = 0.25

# ==================== PRD-STYLE PLOT ====================
fig, ax = plt.subplots(figsize=(7.5, 5.5))

# Bars with PRD styling
bars1 = ax.bar(x - width, na64_cur, width, color='#E69F00',  # orange
               edgecolor='black', linewidth=0.8, alpha=0.9, 
               label='NA64 current')
bars2 = ax.bar(x,         na64_fut, width, color='#E69F00', hatch='//////',
               edgecolor='black', linewidth=0.8, alpha=0.9,
               label='NA64 future')
bars3 = ax.bar(x + width, coll,     width, color='#56B4E9',  # cornflowerblue
               edgecolor='black', linewidth=0.8, alpha=0.9,
               label='Global fit')

# Log scale + limits
ax.set_yscale('log')
ax.set_ylim(5e-4, 2e4)
ax.set_ylabel(r'$|C/\Lambda^2|$ [TeV$^{-2}$]', fontsize=14)

# Axes styling
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, rotation=0)
ax.tick_params(axis='both', which='major', labelsize=11, width=1.2)

# Professional grid
ax.grid(True, axis='y', which='both', alpha=0.3, linestyle='-', linewidth=0.6)
ax.grid(True, axis='y', which='minor', alpha=0.15, linestyle=':')

# Legend (PRD style: outside, compact)
ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.9), 
          fontsize=11, frameon=True, fancybox=False, shadow=False, ncol=1)

# Spine cleanup
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

# Title
ax.set_title('Wilson Coefficient Bounds', fontsize=14, pad=15)

plt.tight_layout()
plt.savefig("wilson_comparison.png", dpi=600, bbox_inches='tight')
plt.show()