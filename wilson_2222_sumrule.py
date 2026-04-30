import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10, 'font.family': 'serif', 
                     'mathtext.fontset': 'stix', 'axes.linewidth': 1.1})

fig, ax = plt.subplots(figsize=(5, 4.0))

# Global fit: -0.02 ± 0.21 TeV^-2 (converted from -2±21 ×10^-2)
C_global = -0.02
xerr_left = 0.21    # right edge: +0.19  
xerr_right = 0.19   # left edge: -0.23
theo_bound = 2*np.pi

x = np.linspace(-25, 25, 1000)

# 1. UV regions (zorder=1)
ax.axvspan(-25, 0, color="green", alpha=0.5, zorder=1, label='Vector UV')
ax.axvspan(0, 25, color="orange", alpha=0.5, zorder=1, label='Scalar UV')

# 2. Theory lines (zorder=10)
ax.axvline(-theo_bound, color='black', lw=1.8, ls=':', zorder=10, label='Unitarity')
ax.axvline(+theo_bound, color='black', lw=1.8, ls=':', zorder=10)
ax.axvline(0, color='black', lw=1.2, ls='--', zorder=10)

# 3. Global fit error band (corrected to match data point)
ax.axvspan(C_global-xerr_left, C_global+xerr_right, color='#56B4E9', alpha=0.35, zorder=20)

# 4. Data point with proper error bars
ax.errorbar([C_global], [0], xerr=[[xerr_left],[xerr_right]], 
            fmt='ko', ms=7, capsize=4, capthick=1.5, elinewidth=1.5, 
            zorder=30, label=r'Global fit')

# Axes styling (PRD quality)
ax.set_xlim(-25, 25)
ax.set_ylim(-0.08, 0.08)
ax.set_yticks([])
ax.set_xlabel(r'$C_{\ell\ell}^{2222}/\Lambda^2$ [TeV$^{-2}$]', fontsize=13)
ax.set_title(r'$\mathcal{O}_{\ell\ell}^{2222}$', fontsize=14, pad=12)

# Symlog + zero line
ax.set_xscale('symlog', linthresh=0.1)
ax.axhline(0, color='black', lw=0.8, alpha=0.7)

# Professional legend
ax.legend(fontsize=8, loc='upper left', bbox_to_anchor=(0.69, 1.0), 
          frameon=True, fancybox=False, ncol=1)

# PRD styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.1)
ax.spines['bottom'].set_linewidth(1.1)
ax.tick_params(axis='x', which='both', width=1.1, length=3)
ax.grid(True, axis='x', alpha=0.2, which='both')

plt.tight_layout()
plt.savefig("Spin_sum.png", dpi=600, bbox_inches='tight', facecolor='white')
plt.show()