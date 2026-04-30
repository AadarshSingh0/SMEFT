import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# =====================
# Plot 3: scalar/vector dominated regions
# =====================

xmin, xmax = -8.0, 8.0
ymin, ymax = -8.0, 8.0
N = 500

x = np.linspace(xmin, xmax, N)
y = np.linspace(ymin, ymax, N)
X, Y = np.meshgrid(x, y)

bound = 2 * np.pi

# Base allowed box: |x| < 1, |y| < 1
inside = (X > -bound) & (X < bound) & (Y > -bound) & (Y < bound)

# Model-dominance regions inside the plane
scalar_mask = (X + Y > 0.0) & (X > 0.0) & (Y > 0.0)
vector_mask = (X + Y <= 0.0) & (X <= 0.0) & (Y <= 0.0)

fig, ax = plt.subplots(figsize=(5.4, 5.0))

# Allowed region and boundary
ax.contourf(X, Y, inside.astype(float), levels=[0.5, 1.5],
            colors=['steelblue'], alpha=0.6)
ax.contour(X, Y, inside.astype(float), levels=[0.5],
           colors=['steelblue'], linewidths=1)

# Dominance regions
ax.contourf(X, Y, scalar_mask.astype(float), levels=[0.5, 1.5],
            colors=['orange'], alpha=0.4)
ax.contourf(X, Y, vector_mask.astype(float), levels=[0.5, 1.5],
            colors=['green'], alpha=0.4)

# Reference lines
ax.axhline(0, color='k', linewidth=0.5)
ax.axvline(0, color='k', linewidth=0.5)
ax.plot(x, -x, color='k', lw=0.5, ls='--')
ax.text(-1.85, 1.95, r'$C_{\ell\ell}^{2233} + C_{\ell\ell}^{2332}$',
        rotation=315, fontsize=10, color='k', ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# Axes styling
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel(r'$s\, C_{2233}^{\ell\ell}/\Lambda^2$', fontsize=14)
ax.set_ylabel(r'$s\, C_{2332}^{\ell\ell}/\Lambda^2$', fontsize=14)
ax.grid(alpha=0.2)

# Legend
allowed_patch = Patch(color='steelblue', alpha=0.6, label='Allowed region')
scalar_patch = Patch(color='orange', alpha=0.4, label='Scalar region')
vector_patch = Patch(color='green', alpha=0.4, label='Vector region')
ax.legend(handles=[allowed_patch, scalar_patch, vector_patch], fontsize=9, loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.savefig('plot3_scalar_vector_regions.png', dpi=300)
plt.show()
