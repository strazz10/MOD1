import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the first fit function: y = c0 + c1 * x**c2
def func1(x, c0, c1, c2):
    return c0 + c1 * x**c2

# Define the second fit function: y = bc + b1 * x**(-1/b2)
def func2(x, bc, b1, b2):
    return bc + b1 * x**(-1/b2)

# Example data for Fit 1 (first set of data)
x1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Example x-data for Fit 1
y1 = np.array([2.1, 3.2, 5.1, 6.8, 9.0, 12.1, 15.0, 18.2, 21.4, 24.0])  # Example y-data for Fit 1
yerr1 = np.array([0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2])  # Example errors in y for Fit 1

# Example data for Fit 2 (second set of data)
x2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Example x-data for Fit 2
y2 = np.array([1.8, 2.5, 4.0, 5.5, 7.3, 10.0, 13.1, 16.0, 19.5, 23.0])  # Example y-data for Fit 2
yerr2 = np.array([0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.3, 0.3, 0.2, 0.1])  # Example errors in y for Fit 2

# Perform the first fit (Fit 1) with func1
popt1, pcov1 = curve_fit(func1, x1, y1, sigma=yerr1)
perr1 = np.sqrt(np.diag(pcov1))  # Standard deviation errors for parameters

# Perform the second fit (Fit 2) with func2
popt2, pcov2 = curve_fit(func2, x2, y2, sigma=yerr2)
perr2 = np.sqrt(np.diag(pcov2))

# Calculate chi-squared for both fits
residuals1 = y1 - func1(x1, *popt1)
chi_squared1 = np.sum((residuals1 / yerr1) ** 2)
reduced_chi_squared1 = chi_squared1 / (len(x1) - len(popt1))  # reduced chi-squared for Fit 1

residuals2 = y2 - func2(x2, *popt2)
chi_squared2 = np.sum((residuals2 / yerr2) ** 2)
reduced_chi_squared2 = chi_squared2 / (len(x2) - len(popt2))  # reduced chi-squared for Fit 2

# Print the results for both fits
print("Fit 1 results:")
print(f"Parameters: {popt1}")
print(f"Errors: {perr1}")
print(f"Chi-squared: {chi_squared1:.4f}")
print(f"Reduced Chi-squared: {reduced_chi_squared1:.4f}")

print("\nFit 2 results:")
print(f"Parameters: {popt2}")
print(f"Errors: {perr2}")
print(f"Chi-squared: {chi_squared2:.4f}")
print(f"Reduced Chi-squared: {reduced_chi_squared2:.4f}")

# Plot the data and fits
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot Fit 1
ax1.errorbar(x1, y1, yerr=yerr1, fmt='o', label="Data for Fit 1")
ax1.plot(x1, func1(x1, *popt1), 'r-', label="Fit 1: y = c0 + c1 * x**c2")
ax1.set_title("Fit 1")
ax1.set_xlabel("x1")
ax1.set_ylabel("y1")
ax1.legend()

# Plot Fit 2
ax2.errorbar(x2, y2, yerr=yerr2, fmt='o', label="Data for Fit 2")
ax2.plot(x2, func2(x2, *popt2), 'g-', label="Fit 2: y = bc + b1 * x**(-1/b2)")
ax2.set_title("Fit 2")
ax2.set_xlabel("x2")
ax2.set_ylabel("y2")
ax2.legend()

plt.tight_layout()
plt.show()

