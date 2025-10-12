import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.gridspec import GridSpec

# ---------- Configuration ----------
data_dir = "/yourpath/"  # folder containing your dat files
file_pattern = "*.dat"  
num_plots = 5

# ---------- Load all data files ----------
files = sorted(glob.glob(data_dir + file_pattern))
if not files:
    raise FileNotFoundError("No .dat files found in directory.")

print(f"Found {len(files)} files.")

# ---------- Setup figure and axes ----------
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(3, 2, figure=fig)

axs = [fig.add_subplot(gs[i // 2, i % 2]) for i in range(4)]
axs.append(fig.add_subplot(gs[2, :]))  
label = [2]

# ---------- Plot data from each file ----------
for index,filename in enumerate(files):
    try:
        data = np.loadtxt(filename, skiprows=1)
        x = data[:, 0]
        
        marker = ['r2', 'go', 'cx', 'r+', 'k1']
        
        for i in range(num_plots):
            y = data[:, 1 + i * 2]
            yerr = data[:, 2 + i * 2]
            axs[i].errorbar(
                x, y, yerr=yerr,
                fmt=marker[i],
                label= f'L={label[index]}'  
            )
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# ---------- Custom axis labels ----------
xlabels = [r"$\beta$"]

ylabels = [
    "<e>",
    "<m>",
    "<|m|>",
    "C",
    "$\chi$"
]

for i, ax in enumerate(axs):
    ax.set_xlabel(xlabels[0], fontsize=11)
    ax.set_ylabel(ylabels[i], fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(fontsize=9, frameon=False)
    ax.tick_params(axis='both', which='major', labelsize=9)

plt.tight_layout(pad=3.0)
plt.show()
