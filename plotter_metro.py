import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## plot per il gen metropolis di prova
filename = 'metropolis_test.dat'  
data = np.loadtxt(filename, comments='#')

state = data[100:, 0]
numbers = data[100:, 1] #skip delle prime 100 iterazioni


x_fit = np.linspace(min(numbers) - 1, max(numbers) + 1, 250) #gaussiana di prova
gaussian = norm.pdf(x_fit, 0, 1)
num_bins = 60

plt.figure()
plt.plot(x_fit, gaussian, 'r-', linewidth=2, label='Normalized Gaussian')
plt.hist(numbers, bins=num_bins, edgecolor='black', alpha=0.7, density=True, label='Generated Numbers')

plt.title('Metropolis-sampled Gauss PDF')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(data[:,0], data[:,1], 'r-', linewidth=2)

plt.title('Sampled Values')
plt.xlabel('Iteration')
plt.ylabel('Result')
plt.grid(True)
plt.show()
