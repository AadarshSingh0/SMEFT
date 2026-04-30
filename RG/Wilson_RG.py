import wilson 
import smelli
from wilson import Wilson
import flavio
from flavio import np_prediction
import matplotlib.pyplot as plt
import numpy as np


# mywilson = Wilson ({ 'uG_33': 1e-6} , scale=1e3, eft='SMEFT', basis='Warsaw')

# # running up to 100 TeV and translating to the 'Warsaw up' basis
# wc = mywilson.match_run( scale =1e5 , eft ='SMEFT', basis = 'Warsaw up')
# # running and matching to WET at 100 GeV in the 'JMS' basis
# wc = mywilson.match_run( scale =100 , eft ='WET', basis = 'JMS')
# # running and matching to WET -3 at 2 GeV in the 'flavio' basis
# wc = mywilson.match_run( scale =2 , eft ='WET-3', basis = 'flavio')

# mywilson = Wilson({ 'lq3_3333': 1e-6} , scale=1e3, eft='SMEFT', basis='Warsaw')
# vsm = flavio.sm_prediction('Rtaul(B->D*lnu)')
# v1 =flavio.np_prediction('Rtaul(B->D*lnu)', mywilson)

# v2 = np_prediction('<Rmue>(B+->Kll)', mywilson, 1, 6)
# print(vsm/v1)
# print(v2)


# VeeLL_2222, VeeLR_2222 in JMS
# ll_2222, le_2222 in Warsaw

# Start with SMEFT coefficient at high scale
smeft_wc = wilson.Wilson(
    {'ll_2233': 2.0},
    scale=100.0,
    eft='SMEFT',
    basis='Warsaw'
)

# Match and run down to WET at 90 GeV
wet_wc = smeft_wc.match_run(scale=90.0, eft='WET', basis='JMS')

# Extract the LEFT coefficient
left_value = wet_wc.dict.get('VeeLL_2233')
print(f"VeeLL_2233 at 90 GeV = {left_value}")
# Expected output: ~1.0 (2.0 / 2 = 1.0, accounting for small RG effects)

# Initialize your Wilson coefficient at 10 GeV in the WET/LEFT
# The operator name follows the WCxf convention: 'LeeVLL_2222'
my_wc = wilson.Wilson(
    {'VnueLL_2332': 1.0},   # Your coefficient value (you can change this)
    scale=0.330,              # Initial scale in GeV
    eft='WET',               # Weak Effective Theory (LEFT is a subset of WET)
    basis='JMS'             # Use the standard WCxf basis
)

# Run the coefficient to the new scale (20 GeV)
# This stays within the same EFT (WET → WET)
my_wc_run = my_wc.match_run(scale=91.0,              # Initial scale in GeV
    eft='WET',               # Weak Effective Theory (LEFT is a subset of WET)
    basis='JMS')
    
# Extract and print the coefficient value
# result = my_wc_at_20.get_wc()


value = my_wc_run.dict.get('VnueLL_2332')
print(f"VnueLL_2332 = {value}")

# print(f"VeeLL_2233 at 20 GeV: {my_wc_at_20}")


 # ------------------------------------------ Start  --------------------------------------------#

my_wc_smeft = wilson.Wilson(
    {'le_2222': 1.0},   # Your coefficient value (you can change this)
    scale=91.0,              # Initial scale in GeV
    eft='SMEFT',               # Weak Effective Theory (LEFT is a subset of WET)
    basis='Warsaw'             # Use the standard WCxf basis
)

# Run the coefficient to the new scale (20 GeV)
# This stays within the same EFT (WET → WET)
my_wc_smeft_run = my_wc_smeft.match_run(scale=1000,              # Initial scale in GeV
    eft='SMEFT',               # Weak Effective Theory (LEFT is a subset of WET)
    basis='Warsaw')
    
# Extract and print the coefficient value
# result = my_wc_at_20.get_wc()


value = my_wc_smeft_run.dict.get('le_2222')
print(f"le_2222 = {value}")


## 1) ------------------ Combined running and matching ------------------ ##


# --- Step 1: WET/LEFT running from low scale to 91 GeV ---
start_left = wilson.Wilson(
    {'VeeLR_2222': 1.0},   # your initial coefficient at 0.33 GeV
    scale=0.33,
    eft='WET',
    basis='JMS'
)

# Choose step sizes (e.g., 5 GeV from 1 to 91, plus the starting point)
left_scales = [0.33] + list(range(1, 92, 1))
if left_scales[-1] != 91:
    left_scales.append(91)

left_vals = []
for s in left_scales:
    wc_at_s = start_left.match_run(scale=s,
    eft='WET',
    basis='JMS')
    left_vals.append(wc_at_s.dict.get('VeeLR_2222').real)  # take real part
    print(f"LEFT: scale {s:5.1f} GeV → VeeLR_2222 = {left_vals[-1]:.6f}")

# Value at 91 GeV VnueLL_2332 for 2332.
left_at_91 = left_vals[-1]

# --- Step 2: Matching (identity) ---
# In wilson, ll_2233 at 91 GeV = VeeLL_2233 at 91 GeV
smeft_start_val = left_at_91

# --- Step 3: SMEFT running from 91 GeV to high scale ---
start_smeft = wilson.Wilson(
    {'le_2222': smeft_start_val},
    scale=91.0,
    eft='SMEFT',
    basis='Warsaw'
)

smeft_scales = list(range(91, 30001, 50))
if smeft_scales[-1] != 1000:
    smeft_scales.append(1000)

smeft_vals = []
for s in smeft_scales:
    wc_at_s = start_smeft.match_run(scale=s,
    eft='SMEFT',
    basis='Warsaw')
    smeft_vals.append(wc_at_s.dict.get('le_2222').real)
    print(f"SMEFT: scale {s:5.1f} GeV → le_2222 = {smeft_vals[-1]:.6f}")

# --- Combine and plot ---
all_scales = left_scales + smeft_scales[1:]  # avoid duplicate 91
all_vals = left_vals + smeft_vals[1:]

plt.figure(figsize=(8,5))
plt.plot(all_scales, all_vals, 'o-', markersize=3, linewidth=1)
plt.axvline(x=91, color='k', linestyle='--', alpha=0.5, label='Matching scale')
plt.xlabel('Scale [GeV]')
plt.ylabel('Coefficient')
plt.title('Running of VeeLL_2233 (LEFT) → ll_2233 (SMEFT)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('running_plot.png', dpi=150)
plt.show()


# ------------------------ Stroing the results for later use ------------------------ #
import csv

with open('running_data_2222.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['scale_GeV', 'coefficient'])  # header
    for s, v in zip(all_scales, all_vals):
        writer.writerow([s, v])