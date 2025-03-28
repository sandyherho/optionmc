#!/usr/bin/env python
"""
Example 3: Parameter Sensitivity Analysis

This script demonstrates how to analyze the sensitivity of option prices
to various parameters such as volatility, time to maturity, and interest rate.
"""
import os
import numpy as np
import pandas as pd
from optionmc.models import OptionPricing
from optionmc.visualization import OptionVisualizer

# Create output directory
output_dir = "parameter_sensitivity_analysis"
os.makedirs(output_dir, exist_ok=True)

# Base option parameters
S0 = 100.0       # Initial stock price
K = 100.0        # Strike price
T = 1.0          # Time to maturity (1 year)
r = 0.05         # Risk-free rate (5%)
sigma = 0.2      # Volatility (20%)
iterations = 50000  # Number of simulations

# Create visualizer
visualizer = OptionVisualizer(output_dir=output_dir)

# 1. Analyze volatility sensitivity
vol_range = np.linspace(0.1, 0.5, 20)
vol_call_prices = []
vol_put_prices = []
vol_call_analytical = []
vol_put_analytical = []

for vol in vol_range:
    pricer = OptionPricing(S0=S0, E=K, T=T, rf=r, sigma=vol, iterations=iterations)
    
    # Monte Carlo prices
    call_price = pricer.call_option_simulation()
    put_price = pricer.put_option_simulation()
    
    # Analytical prices
    bs_call, bs_put = pricer.bs_analytical_price()
    
    vol_call_prices.append(call_price)
    vol_put_prices.append(put_price)
    vol_call_analytical.append(bs_call)
    vol_put_analytical.append(bs_put)

# Create volatility sensitivity plots
visualizer.plot_parameter_sensitivity(
    vol_range, vol_call_prices, 'Volatility',
    analytical_prices=vol_call_analytical,
    title='Call Option Price Sensitivity to Volatility',
    filename='call_volatility_sensitivity'
)

visualizer.plot_parameter_sensitivity(
    vol_range, vol_put_prices, 'Volatility',
    analytical_prices=vol_put_analytical,
    title='Put Option Price Sensitivity to Volatility',
    filename='put_volatility_sensitivity'
)

# 2. Analyze time to maturity sensitivity
time_range = np.linspace(0.1, 2.0, 20)
time_call_prices = []
time_put_prices = []
time_call_analytical = []
time_put_analytical = []

for time in time_range:
    pricer = OptionPricing(S0=S0, E=K, T=time, rf=r, sigma=sigma, iterations=iterations)
    
    # Monte Carlo prices
    call_price = pricer.call_option_simulation()
    put_price = pricer.put_option_simulation()
    
    # Analytical prices
    bs_call, bs_put = pricer.bs_analytical_price()
    
    time_call_prices.append(call_price)
    time_put_prices.append(put_price)
    time_call_analytical.append(bs_call)
    time_put_analytical.append(bs_put)

# Create time sensitivity plots
visualizer.plot_parameter_sensitivity(
    time_range, time_call_prices, 'Time to Maturity [years]',
    analytical_prices=time_call_analytical,
    title='Call Option Price Sensitivity to Time to Maturity',
    filename='call_time_sensitivity'
)

visualizer.plot_parameter_sensitivity(
    time_range, time_put_prices, 'Time to Maturity [years]',
    analytical_prices=time_put_analytical,
    title='Put Option Price Sensitivity to Time to Maturity',
    filename='put_time_sensitivity'
)

# Print results summary
print("Parameter Sensitivity Analysis:")
print(f"Base Option Parameters: S0=${S0}, K=${K}, T={T}, r={r:.2%}, σ={sigma:.2%}")
print("\nAnalysis Results:")
print("1. Volatility Impact:")
print("   - Call Option: Positive impact. Higher volatility → Higher price")
print("   - Put Option: Positive impact. Higher volatility → Higher price")
print("2. Time to Maturity Impact:")
print("   - Call Option: Positive impact. Longer time → Higher price")
print("   - Put Option: Variable impact, depends on other parameters")
print(f"\nResults and visualizations saved to {output_dir}/")
