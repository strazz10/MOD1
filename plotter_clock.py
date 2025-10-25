import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.gridspec import GridSpec

# ---------- Configuration ----------
data_dir = "/home/strazz/Magistrale/NumMeth/MOD1/Clock/"  # folder containing your dat files
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
label = [16, 24, 32, 48, 64, 78]

# ---------- Plot data from each file ----------

for index,filename in enumerate(files):
    try:
        data = np.loadtxt(filename, skiprows=1)
        x = data[:, 0]
        sort = np.argsort(x)
        
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#ff7f0e', '#2ca02c', '#1f77b4']
        markers = ['o', 's', '^', 'v', 'D', '*', 'p', 'h']
        
        for i in range(num_plots-1):
            y = data[:, 1 + i * 2]
            yerr = data[:, 2 + i * 2]
            axs[i].errorbar(
                x, y, 
                marker=markers[(np.random.randint(0, len(markers)))],
                color=colors[(np.random.randint(0, len(colors)))],
                ls='none',
                label= f'L={label[index]}'  
            )
        z = data[:, 9]    
        axs[4].plot(
            x[sort], z[sort]*10**13,
            marker=markers[(np.random.randint(0, len(markers)))],
            color=colors[(np.random.randint(0, len(colors)))],
            label= f'L={label[index]}'
        )
            
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        


# ---------- Custom axis labels ----------
xlabels = [r"$\beta$"]

ylabels = [
    "<$\epsilon$>",
    "<|m|>",
    "C",
    "$\chi$",
    "$U$"
]

for i, ax in enumerate(axs):
    ax.set_xlabel(xlabels[0], fontsize=11)
    ax.set_ylabel(ylabels[i], fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(fontsize=9, frameon=False)
    ax.tick_params(axis='both', which='major', labelsize=9)

axs[4].set_xlim(0.82, 0.92)

plt.tight_layout(pad=3.0)
plt.show()
