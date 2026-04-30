import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# =====================
# Plot 2: C2233 vs C2332 plane
# =====================

# Experimental bounds (TeV^-2)
C_2233_NA64_FUT = 1.4e2
C_2233_NA64_CUR = 1.0e4
C_2332_GLOBAL = 3.0e-2
C_2332_ERROR = 2.3e-2

# Unitarity at sqrt(s)=1 TeV: |C| <= 2 pi in TeV^-2 convention
U = 2.0 * np.pi
x_lim = 10.0 * U
y_lim = 10.0 * U

fig, ax = plt.subplots(figsize=(5.4, 5.0))

# Unitarity boundary and allowed region
x = np.linspace(-U, U, 500)
y = np.linspace(-U, U, 500)
X, Y = np.meshgrid(x, y)
inside = (np.abs(X) <= U) & (np.abs(Y) <= U)

ax.contourf(X, Y, inside.astype(float), levels=[0.5, 1.5],
            colors=['orange'], alpha=0.4, zorder=5)
ax.contour(X, Y, inside.astype(float), levels=[0.5],
           colors=['orange'], linewidths=2, zorder=6)

x_line = np.linspace(-U, U, 500)
# Define the region inside the four thick lines
X, Y = np.meshgrid(x_line, x_line)
inside = (
    (X + 0*Y <  U) &
    (X + 0*Y > -U) &
    (0*X - Y <  U) &
    (0*X - Y > -U)
)

ax.contourf(X, Y, inside.astype(float),
            levels=[0.5, 1.5],
            colors=['orange'],
            alpha=0.2,
            zorder=5)

ax.contour(X, Y, inside.astype(float),
           levels=[0.5],
           colors=['orange'],
           linewidths=2,    
           zorder=6)       


# Dashed unitarity lines
ax.hlines([-U, U], -250, 250, color='orange', lw=2, ls='--')
ax.vlines([-U, U], -100, 100, color='orange', lw=2, ls='--')

# Experimental bands
ax.axhspan(C_2332_GLOBAL - C_2332_ERROR, C_2332_GLOBAL + C_2332_ERROR,
           color='tomato', alpha=0.55, zorder=5,
           label=r'Global fit $|C_{2332}^{\ell\ell}|$')
ax.axvspan(-C_2233_NA64_FUT, C_2233_NA64_FUT,
           color='steelblue', alpha=0.30, zorder=4,
           label=r'NA64$\mu$ future $|C_{2233}^{\ell\ell}|$')
# ax.axvspan(-C_2233_NA64_CUR, C_2233_NA64_CUR,
#            color='cornflowerblue', alpha=0.20, zorder=3,
#            label=r'NA64$\mu$ current $|C_{2233}^{\ell\ell}|$')

# Axes styling
ax.set_xscale('symlog', linthresh=1.0e-1)
ax.set_yscale('symlog', linthresh=2.0e-2)
ax.set_xlim(-x_lim, x_lim)
ax.set_ylim(-y_lim, y_lim)
ax.set_xlabel(r'$C_{2233}^{\ell\ell} (1\,\mathrm{TeV}/\Lambda)^2$', fontsize=14)
ax.set_ylabel(r'$C_{2332}^{\ell\ell} (1\,\mathrm{TeV}/\Lambda)^2$', fontsize=14)
ax.axvline(0, color='k', lw=0.4)
ax.axhline(0, color='k', lw=0.4)
ax.grid(alpha=0.2)

# Legend
unitarity_patch = Patch(color='orange', alpha=0.4, label='Unitarity bound')
handles, labels = ax.get_legend_handles_labels()
handles.append(unitarity_patch)
leg = ax.legend(handles=handles, fontsize=10, loc='lower right', bbox_to_anchor=(1.02, -0.01), framealpha=0.9)
leg.set_zorder(20)

plt.tight_layout()
plt.savefig('plot2_c2233_c2332.png', dpi=300)
plt.show()
