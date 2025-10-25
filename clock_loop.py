import numpy as np                 ##analisi dati per clock, script per i loop
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:             ##check
    print("Usage: python your_script.py <input_file>")
    sys.exit(1)
                                      
input_file = sys.argv[1]                          ##input dal terminale
data = np.loadtxt(input_file, comments='#')    

volume = data[0, 0]
beta = data[0, 1]

en = data[1:, 0]
magn = data[1:, 1]
n = len(en)

k = 10**3                ##parametro blocking stimato da altro script, n divisibile per k

mean_en_matrix = np.reshape(en, (int(n/k), k))               ##energia
mean_en_block = (k/n)*np.sum(np.sum(mean_en_matrix/k, axis=1).tolist())
est_var_en = (k/n)*(k/(n-k))*np.sum((np.sum(mean_en_matrix/k, axis=1).tolist()-mean_en_block)**2)
sigma_e = np.sqrt(est_var_en)

mean_magn_matrix = np.reshape(magn, (int(n/k), k))            ##magnetizzazione
mean_magn_block = (k/n)*np.sum(np.sum(mean_magn_matrix/k, axis=1).tolist())
est_var_magn = (k/n)*(k/(n-k))*np.sum((np.sum(mean_magn_matrix/k, axis=1).tolist()-mean_magn_block)**2)
sigma_m = np.sqrt(est_var_magn)

U = np.sum(magn**4)/(n*np.sum(magn**2)**2)           ##cumulante per stima grafica (?) --> sbagliato!!


R = 500          ##bootstrap
w = 25  
iterations = 10**4         
i = 0
sigma_C0 = np.empty(R)
sigma_chi0 = np.empty(R)
while i<R:
	s1 = 0 #per il calore specifico
	s2 = 0
	k1 = 0 #per la suscettività
	k2 = 0
	j = 0
	while j<iterations:
		myrand = np.random.randint(1, n)
		x_j = en[myrand]
		y_j = magn[myrand]
		s1 = s1 + x_j**2
		s2 = s2 + x_j
		k1 = k1 + y_j**2
		k2 = k2 + y_j
		j = j+1
	s1 = s1/n
	s2 = s2/n
	s2 = s2**2
	k1 = k1/n
	k2 = k2/n
	k2 = k2**2
	sigma_C0[i] = volume*(s1-s2)
	sigma_chi0[i] = volume*(k1-k2)
	i = i+1


variance_en = (k/n)*np.sum(np.sum((mean_en_matrix**2)/k, axis=1).tolist()) - mean_en_block**2    ##calore specifico
C = volume*variance_en

mean_sigmaC_matrix = np.reshape(sigma_C0, (int(R/w), w))          
mean_sigmaC_block = (w/R)*np.sum(np.sum(mean_sigmaC_matrix/w, axis=1).tolist())
sigma_C = np.sqrt((w/R)*(w/(R-w))*(np.sum((np.sum((mean_sigmaC_matrix)/w, axis=1).tolist()-mean_sigmaC_block)**2)))


variance_magn = (k/n)*np.sum(np.sum((mean_magn_matrix**2)/k, axis=1).tolist()) - mean_magn_block**2   ##suscettività
chi = volume*variance_magn

mean_sigmaChi_matrix = np.reshape(sigma_chi0, (int(R/w), w))      
mean_sigmaChi_block = (w/R)*np.sum(np.sum(mean_sigmaChi_matrix/w, axis=1).tolist())
sigma_chi = np.sqrt((w/R)*(w/(R-w))*(np.sum((np.sum((mean_sigmaChi_matrix)/w, axis=1).tolist()-mean_sigmaChi_block)**2)))

print(beta, mean_en_block, sigma_e, mean_magn_block, sigma_m, C, sigma_C, chi, sigma_chi, U)  

