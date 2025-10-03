import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

##roba analisi(?)
filename = 'metropolis_test.dat'  
data = np.loadtxt(filename, comments='#')

state = data[:, 0]
numbers = data[:, 1]

N = len(numbers)
mean_start = 0 #parametri distribuzione di partenza
sigma_start = 1

##metodo blocking

k = 5000 ##n/k deve essere intero

def function1(x): #funzione da mediare
	return x

def function2(x): #funzione da mediare
	return x**2
	
matrix1 = np.reshape(function1(numbers), (int(N/k), k))
matrix2 = np.reshape(function2(numbers), (int(N/k), k))

mean1 = (1/N)*np.sum(function1(numbers)) #valori medi
mean2 = (1/N)*np.sum(function2(numbers))

std1 = np.sqrt((k/N)*(k/(N-k))*np.sum((np.sum(matrix1/k, axis=1).tolist()-mean1)**2)) ##sigma
std2 = np.sqrt((k/N)*(k/(N-k))*np.sum((np.sum(matrix2/k, axis=1).tolist()-mean2)**2))

print(f'<x> = {mean1} +- {std1}')
print(f'<x^2> = {mean2} +- {std2}')

#sembra funzioni relativamente ok


