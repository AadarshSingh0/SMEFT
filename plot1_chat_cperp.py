import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

INV_V2 = 1.0 / 0.24622**2   # 1/v^2 in TeV^-2 (= 16.50); global-fit c's are in units of 1/v^2


# =====================
# Plot 1: rotated (Chat, Cperp) plane
# =====================

# Couplings
G_L = 0.65
G_Y = 0.36
# Falkowski: c_hat = c_ll + alpha_F c_le with alpha_F = 2 gY^2/(gL^2 + 3 gY^2) ~ 0.32.
# In our normalisation c_ll = 2 v^2 C_ll and c_le = v^2 C_le, so the constrained
# direction is C_ll + (alpha_F/2) C_le: the rotation angle uses alpha = alpha_F/2 ~ 0.16.
alpha = (2.0 * G_Y**2) / (G_L**2 + 3.0 * G_Y**2) / 2.0

# Experimental bounds (TeV^-2)
C_HAT_NA64_CUR = 1.0e4
C_HAT_NA64_FUT = 1.7e2
C_2222_GLOBAL = -2.0e-2 * INV_V2 / 2
C_2222_ERROR = 21.0e-2 * INV_V2 / 2

# Plot ranges
chat_max = 1.2 * C_HAT_NA64_CUR
cperp_max = 2.0e4

# Unitarity bounds (TeV^-2) at sqrt(s)=1 TeV
U_LL = 2.0 * np.pi
U_Le = 4.0 * np.pi
DEN = 1.0 + alpha**2

chat_vals = np.concatenate([
    np.linspace(-chat_max, -10.0 * U_LL, 500),
    np.linspace(-10.0 * U_LL, -U_LL, 500),
    np.linspace(-U_LL, U_LL, 2000),
    np.linspace(U_LL, 10.0 * U_LL, 500),
    np.linspace(10.0 * U_LL, chat_max, 500),
])

# Unitarity lines
Cperp_LL_pos = (chat_vals + DEN * U_LL) / alpha
Cperp_LL_neg = (chat_vals - DEN * U_LL) / alpha
Cperp_Le_pos = DEN * U_Le - alpha * chat_vals
Cperp_Le_neg = -DEN * U_Le - alpha * chat_vals

fig, ax = plt.subplots(figsize=(5.4, 5.0))

# Experimental bands
# ax.axvspan(-C_HAT_NA64_CUR, C_HAT_NA64_CUR, color='red', alpha=0.12, label='NA64 current')
# ax.axvspan(-C_HAT_NA64_FUT, C_HAT_NA64_FUT, color='blue', alpha=0.18, label='NA64 future')

# NA64mu bounds |c_LL/v^2|^2 + |c_Le/v^2|^2 <= B^2 (arXiv:2511.11801, Eq. 5.12; small cross term neglected)
# in the normalisation of Falkowski et al., where c_LL/v^2 = 2 C_ll and c_Le/v^2 = C_le in ours.
# -> ellipse 4 C_ll^2 + C_le^2 <= B^2, drawn in the rotated (Chat, Cperp) plane
g = np.logspace(-2, 4.5, 700)
g = np.concatenate([-g[::-1], g])
CH_big, CP_big = np.meshgrid(g, g)
CLL_big = (CH_big - alpha * CP_big) / DEN
CLE_big = (alpha * CH_big + CP_big) / DEN
for B, col, a in [(C_HAT_NA64_CUR, 'red', 0.12), (C_HAT_NA64_FUT, 'blue', 0.18)]:
    ax.contourf(CH_big, CP_big, ((4 * CLL_big**2 + CLE_big**2) <= B**2).astype(float),
                levels=[0.5, 1.5], colors=[col], alpha=a)
ax.axvspan(C_2222_GLOBAL - C_2222_ERROR, C_2222_GLOBAL + C_2222_ERROR,
           color='green', alpha=0.35, label='Global fit')

# Unitarity lines
ax.plot(chat_vals, Cperp_LL_pos, 'k--', lw=1.5, label=r'Unitarity ($C_{LL}$)')
ax.plot(chat_vals, Cperp_LL_neg, 'k--', lw=1.5)
ax.plot(chat_vals, Cperp_Le_pos, 'k-', lw=1.5, label=r'Unitarity ($C_{Le}$)')
ax.plot(chat_vals, Cperp_Le_neg, 'k-', lw=1.5)

# Exact algebraic allowed region
CHAT, CPERP = np.meshgrid(
    np.linspace(-1.0e2, 1.0e2, 800),
    np.linspace(-1.0e2, 1.0e2, 800)
)
inside = (
    (np.abs(CHAT - alpha * CPERP) <= DEN * U_LL) &
    (np.abs(CPERP + alpha * CHAT) <= DEN * U_Le)
)
ax.contourf(CHAT, CPERP, inside.astype(float), levels=[0.5, 1.5],
            colors=['orange'], alpha=0.35, zorder=5)

# Axes styling
ax.set_xscale('symlog', linthresh=1.0e-1)
ax.set_yscale('symlog', linthresh=1.0e-1)
ax.set_xlim(-chat_max, chat_max)
ax.set_ylim(-cperp_max, cperp_max)
ax.set_xlabel(r'$\hat C_{2222} (1\,\mathrm{TeV}/\Lambda)^2$', fontsize=14)
ax.set_ylabel(r'$C_{\perp} (1\,\mathrm{TeV}/\Lambda)^2$', fontsize=14)
ax.axhline(0, color='k', lw=0.5)
ax.axvline(0, color='k', lw=0.5)
ax.grid(alpha=0.2)
ax.tick_params(axis='x', labelrotation=90)

# Legend
rhombus_patch = Patch(color='orange', alpha=0.4, label='Unitarity bound')
handles, labels = ax.get_legend_handles_labels()
handles = [Patch(color='red', alpha=0.12, label='NA64 current'),
           Patch(color='blue', alpha=0.18, label='NA64 future')] + handles
handles.append(rhombus_patch)
leg = ax.legend(handles=handles, fontsize=8, loc='lower right', bbox_to_anchor=(1.02, -0.01), framealpha=0.9)
leg.set_zorder(20)

plt.tight_layout()
plt.savefig('plot1_chat_cperp.png', dpi=300)
plt.show()
