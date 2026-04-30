import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# 1. Define where your file is located
csv_dir = "mu-e_data/"
filename = "filtered_data_x.csv"
filename2= "filtered_data_y.csv"
filename3 = "ship_filtered_data_x.csv"
filename4= "ship_filtered_data_y.csv"
filename5 = "Belle.csv"
filename6 = "NA64.csv"
filename7 = "Dune.csv"

legend_elements = []


filepath = os.path.join(csv_dir, filename)
filepath2 = os.path.join(csv_dir, filename2)
filepath3 = os.path.join(csv_dir, filename3)
filepath4 = os.path.join(csv_dir, filename4)
filepath5 = os.path.join(csv_dir, filename5)
filepath6 = os.path.join(csv_dir, filename6)
filepath7 = os.path.join(csv_dir, filename7)

# 2. Load the data into a table (DataFrame)
# Tell pandas the first row is data, not header, and assign custom names
df = pd.read_csv(filepath, header=None, names=['x', 'y'])
df2 = pd.read_csv(filepath2, header=None, names=['x', 'y'])
df3 = pd.read_csv(filepath3, header=None, names=['x', 'y'])
df4 = pd.read_csv(filepath4, header=None, names=['x', 'y'])
df5 = pd.read_csv(filepath5, header=None, names=['x', 'y'])
df6 = pd.read_csv(filepath6, header=None, names=['x', 'y'])
df7 = pd.read_csv(filepath7, header=None, names=['x', 'y'])
# Now you can multiply 'x' without errors
df['energy_in_MeV'] = df['x'] * 1000
df2['energy_in_MeV'] = df2['x'] * 1000
df3['energy_in_MeV'] = df3['x'] * 1000
df4['energy_in_MeV'] = df4['x'] * 1000
df5['energy_in_MeV'] = df5['x'] * 1000
df6['energy_in_MeV'] = df6['x'] * 1000
df7['energy_in_MeV'] = df7['x'] * 1000
# 4. Plot the data using your new MeV column
plt.figure(figsize=(8, 6))
plt.plot(df['energy_in_MeV'], df['y'], color='grey')
plt.plot(df2['energy_in_MeV'], df2['y'], color='grey')
plt.plot(df3['energy_in_MeV'], df3['y'], color='green')
plt.plot(df4['energy_in_MeV'], df4['y'], color='green')
plt.plot(df5['energy_in_MeV'], df5['y'], color='blue')
plt.plot(df6['energy_in_MeV'], df6['y'], color='red')
plt.plot(df7['energy_in_MeV'], df7['y'], color='orange')


# 1. Plot the SM GF line
xmin, xmax = 2, 1e4
x_line3 = np.logspace(np.log10(xmin), np.log10(xmax), 400)
y_line3 = (1.166e-11)**0.5 * x_line3
# plt.plot(x_line3, y_line3, color='white', linestyle='dashed', linewidth=2.5)

# 2. Add the Vertical line
plt.axvline(x=3.5, color='#00B7EB', linestyle=':', linewidth=2.5, alpha=0.8)

# 3. Add JUNO and T2HK lines
x_juno = np.logspace(np.log10(3.5), np.log10(xmax), 400)
x_T2HK = np.logspace(np.log10(600), np.log10(xmax), 400)
y_juno = 1.0 * 1e-6 * x_juno
y_T2HK = 2.0 * 1e-6 * x_T2HK

plt.plot(x_juno, y_juno, color='#00B7EB', linestyle='--', linewidth=2.8)
# plt.plot(x_T2HK, y_T2HK, color='#32CD32', linestyle='--', linewidth=2.8)

# 4. Add text labels directly on the plot instead of a legend
plt.text(55, 4e-5, 'JUNO', color='#00B7EB', fontsize=10, fontweight='bold')
# plt.text(1000, 5e-4, 'T2HK', color='#32CD32', fontsize=10, fontweight='bold')
# plt.text(5, 3e-5, r'SM $G_F$', color='white', fontsize=10, rotation=35)

# 1. Ensure your grey data is sorted by x
df = df.sort_values('energy_in_MeV')
# df2 = df2.sort_values('energy_in_MeV')
# 2. Define the plotting boundaries
x_min = 2
x_max = 1e4
y_max = 1e-2

# 3. Create a polygon for shading
# We go from the data up to the top limit, then across to the left
# We essentially create a set of points that define the 'shaded' polygon
shade_color = "lightgrey"   # or "#d9d9d9"

plt.fill_between(
    df["energy_in_MeV"], df["y"], y_max,
    color=shade_color, alpha=1.0, label="Excluded Region"
)

plt.fill_between(
    df2["energy_in_MeV"], df2["y"], y_max,
    color=shade_color, alpha=1.0
)

plt.fill_betweenx(
    [df["y"].min(), y_max],
    x_min, df["energy_in_MeV"].iloc[0],
    color=shade_color, alpha=1.0
)

plt.fill_betweenx(
    [df2["y"].min(), y_max],
    x_min, df2["energy_in_MeV"].iloc[0],
    color=shade_color, alpha=1.0
)

plt.xscale('log')
plt.yscale('log')

plt.xlim(2, 1e4)
plt.ylim(1e-9, 1e-3) 
plt.tick_params(axis='both', which='major', labelsize=14)

# Place text at specific data points
plt.text(4500, 1e-4, 'Belle', color='blue', fontsize=10)
plt.text(250, 5e-5, 'NA64', color='red', fontsize=10)
plt.text(30, 1e-5, 'Dune', color='orange', fontsize=10)
plt.text(150, 1e-6, 'Ship', color='green', fontsize=10)
plt.text(10, 1e-8, 'Excluded Region', color='grey', fontsize=12, fontweight='bold')

# 5. Add labels so the plot is clear
plt.xlabel('Mediator mass m$_{Z\'}$ [MeV]',fontsize=15)
plt.ylabel('$g_{\mu e}$ Mediator-Neutrino coupling',fontsize=15)
plt.grid(True, ls=":", alpha=0.5)
plt.savefig("Constraints_Mu-e.png")  # Save the plot as a PNG file
plt.show()

