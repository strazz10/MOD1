import numpy as np                 ##analisi dati per ising 2d, script per i loop
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:             ##check
    print("Usage: python your_script.py <input_file>")
    sys.exit(1)
                                      
input_file = sys.argv[1]                          ##input dal terminale
data = np.loadtxt(input_file, comments='#')    

en = data[1:, 0]
magn = data[1:, 1]
magn_abs = abs(magn)
n = len(en)
volume = data[0, 0]
beta = data[0, 1]

k = 10**3    ##parametro blocking stimato da altro script, n divisibile per k

def square(x):
	return x**2

def power4(x):
	return x**4

mean_en_matrix = np.reshape(en, (int(n/k), k))
mean_magn_matrix = np.reshape(magn_abs, (int(n/k), k))
mean_magn0_matrix = np.reshape(magn, (int(n/k), k))    ##si riferisce a quella senza val. assoluto

mean_en = np.sum(en)/n       ##valori medi e deviazioni standard 
mean_magn = np.sum(magn_abs)/n

mean_en_block = (k/n)*np.sum(np.sum(mean_en_matrix/k, axis=1).tolist())
mean_magn_block = (k/n)*np.sum(np.sum(mean_magn_matrix/k, axis=1).tolist())
mean_magn0_block = (k/n)*np.sum(np.sum(mean_magn0_matrix/k, axis=1).tolist())

est_var_en = (k/n)*(k/(n-k))*np.sum((np.sum(mean_en_matrix/k, axis=1).tolist()-mean_en_block)**2) 
est_var_magn = (k/n)*(k/(n-k))*np.sum((np.sum(mean_magn_matrix/k, axis=1).tolist()-mean_magn_block)**2)
est_var_magn0 = (k/n)*(k/(n-k))*np.sum((np.sum(mean_magn0_matrix/k, axis=1).tolist()-mean_magn0_block)**2)

variance_en = (k/n)*np.sum(np.sum((mean_en_matrix**2)/k, axis=1).tolist()) - mean_en_block**2
variance_magn = (k/n)*np.sum(np.sum((mean_magn_matrix**2)/k, axis=1).tolist()) - mean_magn_block**2

sigma_e = np.sqrt(est_var_en)
sigma_m = np.sqrt(est_var_magn)
sigma_m0 = np.sqrt(est_var_magn0)
 
##grandezze importanti

C = volume*variance_en      #calore spec
chi = volume*(k/n)*np.sum(np.sum((mean_magn_matrix**2)/k, axis=1).tolist())     #suscettività
chi2 = volume*variance_magn

##funzioni bootstrap varie
	

R = 500          
w = 25  
iterations = 10**4         
i = 0
sigma_C0 = np.empty(R)
sigma_chi20 = np.empty(R)
while i<R:
	s1 = 0 #per il calore specifico
	s2 = 0
	k1 = 0 #per la suscettività2
	k2 = 0
	j = 0
	while j<iterations:
		myrand = np.random.randint(1, n)
		x_j = en[myrand]
		y_j = magn[myrand]
		s1 = s1 + square(x_j)
		s2 = s2 + x_j
		k1 = k1 + square(y_j)
		k2 = k2 + y_j
		j = j+1
	s1 = s1/n
	s2 = s2/n
	s2 = s2**2
	k1 = k1/n
	k2 = k2/n
	k2 = k2**2
	sigma_C0[i] = volume*(s1-s2)
	sigma_chi20[i] = volume*(k1-k2)
	i = i+1

mean_sigmaC_matrix = np.reshape(sigma_C0, (int(R/w), w))
mean_sigmaChi2_matrix = np.reshape(sigma_chi20, (int(R/w), w))
mean_sigmaC_block = (w/R)*np.sum(np.sum(mean_sigmaC_matrix/w, axis=1).tolist())
mean_sigmaChi2_block = (w/R)*np.sum(np.sum(mean_sigmaChi2_matrix/w, axis=1).tolist())
sigma_C = np.sqrt((w/R)*(w/(R-w))*(np.sum((np.sum((mean_sigmaC_matrix)/w, axis=1).tolist()-mean_sigmaC_block)**2)))
sigma_chi2 = np.sqrt((w/R)*(w/(R-w))*(np.sum((np.sum((mean_sigmaChi2_matrix)/w, axis=1).tolist()-mean_sigmaChi2_block)**2)))

print(beta, mean_en_block, sigma_e, np.sum(magn)/n, sigma_m0, mean_magn_block, sigma_m, C, sigma_C, chi2, sigma_chi2)
