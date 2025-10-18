import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load data from file L
data = np.loadtxt('MeasurementsPeriodic/total_measures_80.dat')
L = 80

# Extract columns
x = data[:, 0]  # x values (first column)
y1 = data[:, 7]  # first set of data values (7th column)    
yerr1 = data[:, 8]  # corresponding errors for set 1 (8th column)
y2 = data[:, 9]  # second set of data values (9th column)
yerr2 = data[:, 10]  # corresponding errors for set 2 (10th column)

# Define the quadratic fit function (a*x^2 + b*x + c)
def fit_function(x, a, bc, ymax):
    return a*(x - bc)**2 + ymax

# Define the x range for fitting (you can change these values)
x_min_1 = 0.689   # Minimum value of x for the first fit
x_max_1 = 0.695  # Maximum value of x for the first fit

x_min_2 = 0.689   # Minimum value of x for the second fit
x_max_2 = 0.694   # Maximum value of x for the second fit

# Create masks for selecting x ranges for each fit
mask1 = (x >= x_min_1) & (x <= x_max_1)  # Mask for the first data set (Data Set 1)
mask2 = (x >= x_min_2) & (x <= x_max_2)  # Mask for the second data set (Data Set 2)

# Apply the masks to select the data within the specified ranges
x_fit1 = x[mask1]
y_fit1 = y1[mask1]
yerr_fit1 = yerr1[mask1]

x_fit2 = x[mask2]
y_fit2 = y2[mask2]
yerr_fit2 = yerr2[mask2]

# Fit the data to the quadratic function for both sets of measurements
params1, cov1 = curve_fit(fit_function, x_fit1, y_fit1, p0=(-1, 0.69, 5), sigma=yerr_fit1, absolute_sigma=True, maxfev=50000)
params2, cov2 = curve_fit(fit_function, x_fit2, y_fit2, p0=(-1, 0.69, 200), sigma=yerr_fit2, absolute_sigma=True, maxfev=50000)

# Generate fitted data
y_fit1_vals = fit_function(x_fit1, *params1)
y_fit2_vals = fit_function(x_fit2, *params2)

# Calculate residuals for both fits
residuals1 = y_fit1 - y_fit1_vals
residuals2 = y_fit2 - y_fit2_vals

# Calculate chi-squared for both fits
chi_squared1 = np.sum((residuals1 / yerr_fit1)**2)
chi_squared2 = np.sum((residuals2 / yerr_fit2)**2)

# Calculate the degrees of freedom (dof) for both fits
dof1 = len(x_fit1) - len(params1)  # dof = N - number of parameters
dof2 = len(x_fit2) - len(params2)

# Calculate reduced chi-squared for both fits
reduced_chi_squared1 = chi_squared1 / dof1
reduced_chi_squared2 = chi_squared2 / dof2

# Extract the errors on the parameters from the covariance matrix (diagonal elements)
errors1 = np.sqrt(np.diag(cov1))  # Errors for Fit 1
errors2 = np.sqrt(np.diag(cov2))  # Errors for Fit 2

# Print the fit parameters, errors, and chi-squared values
print("Fit 1 (Data Set 1):")
print(f"  Parameters: a = {params1[0]:.4f} ± {errors1[0]:.4f}, bc = {params1[1]:.4f} ± {errors1[1]:.4f}, ymax = {params1[2]:.4f} ± {errors1[2]:.4f}")
print(f"  Chi-squared: {chi_squared1:.4f}, Reduced Chi-squared: {reduced_chi_squared1:.4f}")
print()

print("Fit 2 (Data Set 2):")
print(f"  Parameters: a = {params2[0]:.4f} ± {errors2[0]:.4f}, bc = {params2[1]:.4f} ± {errors2[1]:.4f}, ymax = {params2[2]:.4f} ± {errors2[2]:.4f}")
print(f"  Chi-squared: {chi_squared2:.4f}, Reduced Chi-squared: {reduced_chi_squared2:.4f}")
print()

# Plot the data and the fit for the first data set (Data Set 1)
plt.figure(figsize=(10, 6))
plt.errorbar(x_fit1, y_fit1, yerr=yerr_fit1, fmt='o', label='Data Set 1', color='blue')
plt.plot(x_fit1, y_fit1_vals, label='Fit 1 (Quadratic)', color='blue', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data Set 1 and Quadratic Fit')
plt.legend()
plt.tight_layout()
plt.show()  # Show the plot for Fit 1

# Plot the residuals for the first data set (Data Set 1)
plt.figure(figsize=(10, 6))
plt.errorbar(x_fit1, residuals1, yerr=yerr_fit1, fmt='o', label='Residuals 1', color='blue')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('x')
plt.ylabel('Residuals')
plt.title('Residuals for Fit 1')
plt.legend()
plt.tight_layout()
plt.show()  # Show the residuals plot for Fit 1

# Plot the data and the fit for the second data set (Data Set 2)
plt.figure(figsize=(10, 6))
plt.errorbar(x_fit2, y_fit2, yerr=yerr_fit2, fmt='o', label='Data Set 2', color='red')
plt.plot(x_fit2, y_fit2_vals, label='Fit 2 (Quadratic)', color='red', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data Set 2 and Quadratic Fit')
plt.legend()
plt.tight_layout()
plt.show()  # Show the plot for Fit 2

# Plot the residuals for the second data set (Data Set 2)
plt.figure(figsize=(10, 6))
plt.errorbar(x_fit2, residuals2, yerr=yerr_fit2, fmt='o', label='Residuals 2', color='red')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('x')
plt.ylabel('Residuals')
plt.title('Residuals for Fit 2')
plt.legend()
plt.tight_layout()
plt.show()  # Show the residuals plot for Fit 2

# Open the text file in append mode ('a')
with open('fit_results.txt', 'a') as file:
    # If this is the first time running, write headers (you can control this by checking the file's contents or adding logic)
    if file.tell() == 0:  # If the file is empty, write the headers
        file.write("Fit Results\n")
        file.write("=====================\n\n")
        file.write("Fit   a        a_error  x_center  x_center_error  ymax    ymax_error  Chi_squared  Reduced_Chi_squared\n")
        file.write("----------------------------------------------------------\n")
    
    # Write results for C (Data Set 1)
    file.write(f"C     {params1[0]:.4f}  {errors1[0]:.4f}   {params1[1]:.4f}   {errors1[1]:.4f}      {params1[2]:.4f}   {errors1[2]:.4f}    {chi_squared1:.4f}      {reduced_chi_squared1:.4f}\n")
    
    # Write results for chi (Data Set 2)
    file.write(f"chi   {params2[0]:.4f}  {errors2[0]:.4f}   {params2[1]:.4f}   {errors2[1]:.4f}      {params2[2]:.4f}   {errors2[2]:.4f}    {chi_squared2:.4f}      {reduced_chi_squared2:.4f}\n")
    
print("Results appended to 'fit_results.txt'")

# Function to save results to the same fit results file
def save_number_to_fit_results_file(filename, L):
    with open(filename, 'a') as file:
        file.write(f"L: {L}\n")  # Save the value of L in a human-readable format

# Save the number L to the fit results file
save_number_to_fit_results_file('fit_results.txt', L)

print(f"Number {L} appended to fit_results.txt")
