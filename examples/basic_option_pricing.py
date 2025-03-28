#!/usr/bin/env python
"""
Example 1: Basic Option Pricing

This script demonstrates the basic usage of OptionMC for pricing
European call and put options using Monte Carlo simulation.
"""
import os
from optionmc.models import OptionPricing
from optionmc.visualization import OptionVisualizer

# Create output directory
output_dir = "basic_option_pricing"
os.makedirs(output_dir, exist_ok=True)

# Define option parameters
S0 = 100.0        # Initial stock price
K = 100.0         # Strike price
T = 1.0           # Time to maturity (1 year)
r = 0.05          # Risk-free rate (5%)
sigma = 0.2       # Volatility (20%)
iterations = 100000  # Number of simulations

# Create the option pricing model
pricer = OptionPricing(S0=S0, E=K, T=T, rf=r, sigma=sigma, iterations=iterations)

# Calculate option prices
call_price, (stock_prices, call_payoffs) = pricer.call_option_simulation(return_paths=True)
put_price, (_, put_payoffs) = pricer.put_option_simulation(return_paths=True)

# Get Black-Scholes analytical solutions for comparison
bs_call, bs_put = pricer.bs_analytical_price()

# Create visualizer for plots
visualizer = OptionVisualizer(output_dir=output_dir)

# Plot price distributions
visualizer.plot_price_distribution(
    stock_prices, call_payoffs,
    title=f"Stock Price and Call Option Payoff Distributions (S0=${S0}, K=${K})",
    filename="call_distributions"
)

visualizer.plot_price_distribution(
    stock_prices, put_payoffs,
    title=f"Stock Price and Put Option Payoff Distributions (S0=${S0}, K=${K})",
    filename="put_distributions"
)

# Print results
print("Option Pricing Results:")
print(f"Initial Stock Price: ${S0:.2f}")
print(f"Strike Price: ${K:.2f}")
print(f"Time to Maturity: {T} year(s)")
print(f"Risk-free Rate: {r:.2%}")
print(f"Volatility: {sigma:.2%}")
print("\nCall Option:")
print(f"  Monte Carlo Price: ${call_price:.4f}")
print(f"  Black-Scholes Price: ${bs_call:.4f}")
print(f"  Difference: ${abs(call_price - bs_call):.4f} ({abs(call_price - bs_call) / bs_call:.4%})")
print("\nPut Option:")
print(f"  Monte Carlo Price: ${put_price:.4f}")
print(f"  Black-Scholes Price: ${bs_put:.4f}")
print(f"  Difference: ${abs(put_price - bs_put):.4f} ({abs(put_price - bs_put) / bs_put:.4%})")
print(f"\nResults and visualizations saved to {output_dir}/")
