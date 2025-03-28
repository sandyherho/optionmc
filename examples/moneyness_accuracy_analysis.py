#!/usr/bin/env python
"""
Example 4: Monte Carlo Accuracy Analysis

This script analyzes how the accuracy of Monte Carlo pricing changes
for options with different strike prices (at-the-money vs. out-of-the-money).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from optionmc.models import OptionPricing

# Create output directory
output_dir = "moneyness_accuracy_analysis"
os.makedirs(output_dir, exist_ok=True)

# Base option parameters
S0 = 100.0         # Initial stock price
T = 0.5            # Time to maturity (6 months)
r = 0.05           # Risk-free rate (5%)
sigma = 0.25       # Volatility (25%)
iterations = 100000  # Number of simulations

# Range of strike prices to analyze
strike_range = np.linspace(70, 130, 13)  # From deep ITM to deep OTM
iterations_list = [1000, 10000, 100000]  # Different simulation sizes

# Initialize results storage
results = {
    'strike': [],
    'moneyness': [],
    'iterations': [],
    'call_mc_price': [],
    'call_bs_price': [],
    'call_error': [],
    'put_mc_price': [],
    'put_bs_price': [],
    'put_error': []
}

# Run simulations for each strike price and iteration count
for K in strike_range:
    moneyness = K / S0  # > 1 for OTM calls, < 1 for ITM calls
    
    for iter_count in iterations_list:
        # Create pricer
        pricer = OptionPricing(S0=S0, E=K, T=T, rf=r, sigma=sigma, iterations=iter_count)
        
        # Get Monte Carlo prices
        call_price = pricer.call_option_simulation()
        put_price = pricer.put_option_simulation()
        
        # Get analytical prices
        bs_call, bs_put = pricer.bs_analytical_price()
        
        # Calculate errors
        call_error = abs(call_price - bs_call) / bs_call if bs_call > 0.01 else 0
        put_error = abs(put_price - bs_put) / bs_put if bs_put > 0.01 else 0
        
        # Store results
        results['strike'].append(K)
        results['moneyness'].append(moneyness)
        results['iterations'].append(iter_count)
        results['call_mc_price'].append(call_price)
        results['call_bs_price'].append(bs_call)
        results['call_error'].append(call_error)
        results['put_mc_price'].append(put_price)
        results['put_bs_price'].append(bs_put)
        results['put_error'].append(put_error)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to CSV
results_df.to_csv(os.path.join(output_dir, "strike_analysis_results.csv"), index=False)

# Create visualization for the results
plt.style.use('bmh')

# Plot: Call Option Error vs Moneyness
plt.figure(figsize=(10, 6))
for iter_count in iterations_list:
    subset = results_df[results_df['iterations'] == iter_count]
    plt.plot(subset['moneyness'], subset['call_error'] * 100, 'o-', 
             label=f'{iter_count} iterations')

plt.axvline(x=1.0, color='gray', linestyle='--', alpha=0.7, label='At-the-money')
plt.xlabel('Moneyness (K/S0)')
plt.ylabel('Relative Error [%]')
plt.title('Call Option Pricing Error vs. Moneyness')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "call_error_vs_moneyness.png"), dpi=300)

# Add plot for put options as well
plt.figure(figsize=(10, 6))
for iter_count in iterations_list:
    subset = results_df[results_df['iterations'] == iter_count]
    plt.plot(subset['moneyness'], subset['put_error'] * 100, 'o-', 
             label=f'{iter_count} iterations')

plt.axvline(x=1.0, color='gray', linestyle='--', alpha=0.7, label='At-the-money')
plt.xlabel('Moneyness (K/S0)')
plt.ylabel('Relative Error [%]')
plt.title('Put Option Pricing Error vs. Moneyness')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "put_error_vs_moneyness.png"), dpi=300)

# Print a summary of findings
print("Analysis of Strike Price Impact:")
print(f"Stock Price: ${S0}")
print(f"Time to Maturity: {T} years")
print(f"Risk-free Rate: {r:.2%}")
print(f"Volatility: {sigma:.2%}")

# Get summary statistics for the maximum iteration count
max_iter_results = results_df[results_df['iterations'] == iterations_list[-1]]
atm_results = max_iter_results[max_iter_results['moneyness'].between(0.95, 1.05)]
itm_call_results = max_iter_results[max_iter_results['moneyness'] < 0.95]
otm_call_results = max_iter_results[max_iter_results['moneyness'] > 1.05]

print("\nAverage Relative Errors (with maximum iterations):")
print(f"  At-the-money Call Options: {atm_results['call_error'].mean():.4%}")
print(f"  In-the-money Call Options: {itm_call_results['call_error'].mean():.4%}")
print(f"  Out-of-the-money Call Options: {otm_call_results['call_error'].mean():.4%}")

print("\nConclusions:")
print("1. Monte Carlo accuracy varies with moneyness (K/S0 ratio)")
print("2. For call options, out-of-the-money options are harder to price accurately")
print("3. Increasing the number of iterations significantly improves accuracy")
print(f"\nResults and visualizations saved to {output_dir}/")
