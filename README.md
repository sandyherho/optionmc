# OptionMC: Monte Carlo Option Pricing

[![PyPI version](https://badge.fury.io/py/optionmc.svg)](https://badge.fury.io/py/optionmc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for pricing European options using Monte Carlo simulation, featuring variance reduction techniques and educational visualizations.

## Features

- European call and put option pricing with Monte Carlo simulation
- Variance reduction using antithetic variates 
- Comparison with Black-Scholes analytical solutions
- Publication-quality visualizations:
  - Price convergence analysis
  - Stock price and payoff distributions
  - Parameter sensitivity analysis
- Command-line interface for quick pricing
- Comprehensive examples for educational purposes

## Installation

```bash
pip install optionmc
```

## Quick Start

```python
from optionmc.models import OptionPricing

# Create option pricing model
model = OptionPricing(
    S0=100,     # Initial stock price
    E=100,      # Strike price
    T=1.0,      # Time to maturity (1 year)
    rf=0.05,    # Risk-free rate (5%)
    sigma=0.2,  # Volatility (20%)
    iterations=100000  # Number of simulations
)

# Calculate option prices
call_price = model.call_option_simulation()
put_price = model.put_option_simulation()

# Get analytical solutions for comparison
bs_call, bs_put = model.bs_analytical_price()

# Print results
print(f"Call Option Price: ${call_price:.4f} (Black-Scholes: ${bs_call:.4f})")
print(f"Put Option Price: ${put_price:.4f} (Black-Scholes: ${bs_put:.4f})")
```

## Command Line Usage

```bash
# Basic option pricing
optionmc price --s0 100 --strike 95 --volatility 0.25 --time 0.5

# Using antithetic variates for variance reduction
optionmc price --method antithetic --iterations 500000
```

## Example Visualizations

OptionMC generates publication-quality visualizations:

- Convergence analysis showing how Monte Carlo estimates approach analytical solutions
- Stock price and payoff distributions for both call and put options
- Sensitivity analysis for parameters like volatility and time to maturity

## Documentation

For detailed usage examples, see the `examples/` directory:

1. **Basic Option Pricing** - Core functionality demonstration
2. **Variance Reduction** - Comparison of standard MC vs. antithetic variates
3. **Parameter Sensitivity** - Analysis of how option prices respond to parameter changes
4. **Moneyness Analysis** - Exploring pricing accuracy for different strike prices

## Mathematical Background

OptionMC implements the standard Monte Carlo approach for option pricing:
1. Simulate stock price paths using Geometric Brownian Motion
2. Calculate option payoffs at maturity 
3. Average the discounted payoffs to get the option price

For European options, the payoff functions are:
- Call option: max(S - K, 0)
- Put option: max(K - S, 0)

Where S is the stock price at maturity and K is the strike price.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Sandy Herho (sandy.herho@email.ucr.edu)

## Citation

If you use this package in your research, please cite it as:

```
Herho, S. (2025). OptionMC: A Python package for Monte Carlo option pricing.
```
