import numpy as np
import matplotlib.pyplot as plt

filename = 'ising.dat'       ##analisi parametro blocking per ising 2d
data = np.loadtxt(filename, comments='#')

en = data[:, 0]
magn = data[:, 1]
magn = abs(magn)
n = len(en)

def square(x):
	return x**2

def power4(x):
	return x**4


test_k = [] 
for a in range(0,8):
	for b in range(0,8):
		div = 2**a * 5**b
		test_k.append(div) 

test_k = np.sort(test_k)
end = len(test_k)
var_en_array = np.empty(end)
var_magn_array = np.empty(end)
i = 0	

while i < end:
	k = test_k[i]
	mean_en_matrix = np.reshape(en, (int(n/k), k))
	mean_magn_matrix = np.reshape(magn, (int(n/k), k))
	
	mean_en_block = (k/n)*np.sum(np.sum(mean_en_matrix/k, axis=1).tolist())   
	mean_magn_block = (k/n)*np.sum(np.sum(mean_magn_matrix/k, axis=1).tolist())
	
	var_en_array[i] = (k/n)*(k/(n-k))*np.sum((np.sum(mean_en_matrix/k, axis=1).tolist()-mean_en_block)**2) 
	var_magn_array[i] = (k/n)*(k/(n-k))*np.sum((np.sum(mean_magn_matrix/k, axis=1).tolist()-mean_magn_block)**2)
	i = i + 1

plt.figure(figsize=(8, 6))
plt.loglog(test_k, np.sqrt(var_en_array), label='$\sigma_e$', linestyle='solid', color='blue')
plt.loglog(test_k, np.sqrt(var_magn_array), label='$\sigma_{|m|}$', linestyle='solid', color='orange')

plt.xlabel('blocking parameter k')
plt.ylabel('estimated $\sigma_{e,|m|}$')
plt.xlim(5, 10**5)
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
