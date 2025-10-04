import numpy as np
import matplotlib.pyplot as plt

filename = 'ising.dat'       ##analisi dati per ising 2d
data = np.loadtxt(filename, comments='#')

en = data[1000:, 0]
magn = data[1000:, 1]
magn = abs(magn)
n = len(en)

k = 1      ##parametro blocking, n divisibile per k

def square(x):
	return x**2

def power4(x):
	return x**4
	
mean_en_matrix = np.reshape(en, (int(n/k), k))
mean_magn_matrix = np.reshape(magn, (int(n/k), k))

mean_en = np.sum(en)/n       ##valori medi e deviazioni standard 
mean_magn = np.sum(magn)/n

var_en = (k/(n-k))*np.sum((np.sum(mean_en_matrix/k, axis=1).tolist()-mean_en)**2)
var_magn = (k/(n-k))*np.sum((np.sum(mean_magn_matrix/k, axis=1).tolist()-mean_magn)**2)

print(f'<e> =  {mean_en}, var_e = {var_en}')
print(f'<|m|> =  {mean_magn}, var_m = {var_magn}')

mean_magnsquare = np.sum(square(magn))/n 
mean_magnsquare_matrix = np.reshape(square(magn), (int(n/k), k))
print(f'<m^2> =  {mean_magnsquare}')

mean_magnfourth = np.sum(power4(magn))/n
mean_quartic = mean_magnfourth/(mean_magnsquare**2) 
print(f'<m^4>/<m^2>^2 =  {mean_quartic}')

def bootstrap_quartic():
	R = 200            ##bootstrap per la varianza m^4/m^2^2
	w = 20             ##parametro blocking per il bootstrap
	i = 0
	quartic = np.empty(R)
	while i<R:
		s1 = 0
		s2 = 0
		j = 0
		while j<n:
			x_j = magn[np.random.randint(1, n)]
			s1 = s1 + square(x_j)
			s2 = s2 + power4(x_j)
			j = j+1
		s1 = s1/n
		s2 = s2/n
		quartic[i] = s2/(s1**2)
		i = i+1
	mean_quartic_matrix = np.reshape(quartic, (int(n/w), w))
	var_quartic = (w/(n-w))*np.sum((np.sum(mean_quartic_matrix/w, axis=1).tolist()-mean_quartic)**2)
	print(f'var_m = {var_quartic}')
	return var_quartic
	
#bootstrap_quartic()  
##togliere il commento per calcolare (lentissimo)



