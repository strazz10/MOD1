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
label = [16, 24, 32, 40, 48, 64, 78]
axin = axs[4].inset_axes([0.5, 0.5, 0.4, 0.4], xlim=(0.876, 0.886), ylim=(1.03, 1.07))

# ---------- Plot (principali) data from each file ----------

for index,filename in enumerate(files):
    try:
        data = np.loadtxt(filename, skiprows=1)
        x = data[:, 0]
        sort = np.argsort(x)
        
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#ff7f0e', '#2ca02c', '#1f77b4']
        markers = ['o', 's', '^', 'v', 'D', '*', 'p', 'h']
        myrand1 = np.random.randint(0, len(markers))
        myrand2 = np.random.randint(0, len(colors))
        for i in range(num_plots-1):
            y = data[:, 1 + i * 2]
            yerr = data[:, 2 + i * 2]
            axs[i].errorbar(
                x, y, 
                marker=markers[myrand1],
                color=colors[myrand2],
                ls='none',
                label= f'L={label[index]}'  
            )
            
            z = data[:, 9]    
            axs[4].plot(
            x[sort], z[sort]*(4*10**12),            ##correzione dal programma di analisi
            marker=markers[myrand1],
            color=colors[myrand2],
            
            )
            axin.plot(x[sort], z[sort]*4*10**12,
            marker=markers[myrand1],
            color=colors[myrand2])
 
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
ax.indicate_inset_zoom(axin, edgecolor="black")

plt.tight_layout(pad=3.0)
plt.show()

##plots per fss

fig1 = plt.figure(figsize=(13, 13))
gs1 = GridSpec(2, 2, figure=fig1)
axs1 = [fig1.add_subplot(gs[i // 2, i % 2]) for i in range(4)]

for index,filename in enumerate(files):
	colors = ['b', 'g', 'r', 'y', 'k', '#ff7f0e', '#1f77b4']
	markers = ['o', 's', '^', 'v', 'D', '*', 'p', 'h']
	try:
		myrand1 = np.random.randint(0, len(markers))
		myrand2 = np.random.randint(0, len(colors))
			
		data = np.loadtxt(filename, skiprows=1)
		x = data[:, 0]
		x_scaled = (x-np.log(1+np.sqrt(2)))*label[index]
		sort = np.argsort(x_scaled)
			
		m_abs = data[:,3]*(label[index]**(1/8))
		axs1[0].plot(x_scaled, m_abs, marker=markers[myrand1],
		color=colors[myrand2],ls='none',label= f'L={label[index]}')
			
		chi = data[:,7]/(label[index]**(1.75))
		axs1[1].plot(x_scaled, chi, marker=markers[myrand1],
		color=colors[myrand2],ls='none',label= f'L={label[index]}')
			
		cumulant = data[:,9]*(4*10**12)
		axs1[2].plot(x_scaled, cumulant, marker=markers[myrand1],
		color=colors[myrand2],ls='none',label= f'L={label[index]}')
			
		specific = data[:,5]
		axs1[3].plot(x_scaled, specific, marker=markers[myrand1],
		color=colors[myrand2],ls='none',label= f'L={label[index]}')
		
	except Exception as e:
		print(f"Error reading {filename}: {e}")

xlabels1 = [r"$\beta \cdot L^{1/\nu}$"]

ylabels1 = [
    r"$<|m|>\cdot L^{\beta/\nu}$",
    r'$\chi \cdot L^{-\gamma/\nu}$',
    "$U$",
    "C"
]

for i, ax in enumerate(axs1):
    ax.set_xlabel(xlabels1[0], fontsize=15)
    ax.set_ylabel(ylabels1[i], fontsize=15)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(fontsize=9, frameon=False)
    ax.tick_params(axis='both', which='major', labelsize=9)
    ax.set_xlim(-6, 2)

plt.tight_layout(pad=3.0)
plt.show()
                
        
		
		


