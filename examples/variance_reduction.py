#!/usr/bin/env python
"""
Example 2: Variance Reduction with Antithetic Variates

This script compares standard Monte Carlo simulation with the antithetic
variates technique for variance reduction in option pricing.
"""
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from optionmc.models import OptionPricing

# Create output directory
output_dir = "variance_reduction"
os.makedirs(output_dir, exist_ok=True)

# Define option parameters
S0 = 100.0       # Initial stock price
K = 100.0        # Strike price
T = 1.0          # Time to maturity (1 year)
r = 0.05         # Risk-free rate (5%)
sigma = 0.2      # Volatility (20%)

# Function to run simulations with different iterations
def run_simulations(iterations_list):
    results = {
        'iterations': [],
        'standard_price': [],
        'standard_time': [],
        'antithetic_price': [],
        'antithetic_time': [],
        'standard_error': [],
        'antithetic_error': [],
        'analytical_price': []
    }
    
    for iterations in iterations_list:
        # Create pricer
        pricer = OptionPricing(S0=S0, E=K, T=T, rf=r, sigma=sigma, iterations=iterations)
        
        # Get analytical price
        bs_call, _ = pricer.bs_analytical_price()
        
        # Standard Monte Carlo
        start_time = time.time()
        standard_price = pricer.call_option_simulation()
        standard_time = time.time() - start_time
        
        # Antithetic Monte Carlo
        start_time = time.time()
        antithetic_price = pricer.antithetic_call_simulation()
        antithetic_time = time.time() - start_time
        
        # Calculate errors
        standard_error = abs(standard_price - bs_call) / bs_call
        antithetic_error = abs(antithetic_price - bs_call) / bs_call
        
        # Store results
        results['iterations'].append(iterations)
        results['standard_price'].append(standard_price)
        results['standard_time'].append(standard_time)
        results['antithetic_price'].append(antithetic_price)
        results['antithetic_time'].append(antithetic_time)
        results['standard_error'].append(standard_error)
        results['antithetic_error'].append(antithetic_error)
        results['analytical_price'].append(bs_call)
    
    return pd.DataFrame(results)

# Run simulations with increasing number of iterations
iterations_list = np.logspace(2, 5, 10).astype(int)
results_df = run_simulations(iterations_list)

# Save results to CSV
results_df.to_csv(os.path.join(output_dir, "variance_reduction_comparison.csv"), index=False)

# Create custom visualizations
plt.style.use('bmh')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot price convergence
ax1.plot(results_df['iterations'], results_df['standard_price'], 'o-', label='Standard MC')
ax1.plot(results_df['iterations'], results_df['antithetic_price'], 's-', label='Antithetic Variates')
ax1.plot(results_df['iterations'], results_df['analytical_price'], '--', label='Analytical Solution')
ax1.set_xscale('log')
ax1.set_xlabel('Number of Iterations')
ax1.set_ylabel('Option Price [$]')
ax1.set_title('Price Convergence Comparison')
ax1.legend()

# Plot relative error
ax2.plot(results_df['iterations'], results_df['standard_error'] * 100, 'o-', label='Standard MC')
ax2.plot(results_df['iterations'], results_df['antithetic_error'] * 100, 's-', label='Antithetic Variates')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('Number of Iterations')
ax2.set_ylabel('Relative Error [%]')
ax2.set_title('Error Comparison')
ax2.legend()

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "variance_reduction_comparison.png"), dpi=300)

# Print results summary
print("Variance Reduction with Antithetic Variates:")
print(f"Option Parameters: S0=${S0}, K=${K}, T={T}, r={r:.2%}, σ={sigma:.2%}")
print(f"Analytical Price (Black-Scholes): ${results_df['analytical_price'].iloc[-1]:.4f}")
print("\nResults for maximum iterations:")
print(f"Standard Monte Carlo Price: ${results_df['standard_price'].iloc[-1]:.4f}")
print(f"  Error: {results_df['standard_error'].iloc[-1]:.4%}")
print(f"  Computation Time: {results_df['standard_time'].iloc[-1]:.4f} sec")
print(f"Antithetic Variates Price: ${results_df['antithetic_price'].iloc[-1]:.4f}")
print(f"  Error: {results_df['antithetic_error'].iloc[-1]:.4%}")
print(f"  Computation Time: {results_df['antithetic_time'].iloc[-1]:.4f} sec")
print(f"\nResults and visualizations saved to {output_dir}/")
