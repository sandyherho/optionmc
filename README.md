# OptionMC: Monte Carlo Option Pricing

[![PyPI version](https://img.shields.io/pypi/v/optionmc.svg)](https://pypi.org/project/optionmc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/956375821.svg)](https://doi.org/10.5281/zenodo.15099722)

A Python package for pricing European options using Monte Carlo simulation, featuring variance reduction techniques and publication-quality visualizations. Designed for educational purposes and financial engineering applications.

## Features

- European call and put option pricing with Monte Carlo simulation
- Variance reduction using antithetic variates
- Comparison with Black-Scholes analytical solutions
- Publication-quality visualizations:
  - Price convergence analysis
  - Stock price and payoff distributions
  - Parameter sensitivity analysis
- Command-line interface for quick pricing and visualization
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

# Custom output directory
optionmc price --output-dir my_results
```

## Mathematical Background

### Black-Scholes Option Pricing

The Black-Scholes model provides analytical solutions for European options, assuming:
- Lognormal distribution of stock prices
- Constant volatility and risk-free rate
- No transaction costs or dividends
- Continuous trading

For a European call option, the Black-Scholes formula is:

$$C = S_0 N(d_1) - Ke^{-rT} N(d_2)$$

For a European put option:

$$P = Ke^{-rT} N(-d_2) - S_0 N(-d_1)$$

Where:
- $S_0$ is the initial stock price
- $K$ is the strike price
- $r$ is the risk-free rate
- $T$ is the time to maturity (in years)
- $N(\cdot)$ is the cumulative distribution function of the standard normal distribution
- $d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$
- $d_2 = d_1 - \sigma\sqrt{T}$

### Monte Carlo Simulation

The Monte Carlo approach for option pricing follows these steps:

1. **Simulate stock price paths** using Geometric Brownian Motion (GBM):

   $$S_T = S_0 \exp\left((r - \frac{\sigma^2}{2})T + \sigma\sqrt{T}Z\right)$$

   where $Z \sim N(0,1)$ is a standard normal random variable.

2. **Calculate payoffs** at maturity:
   - Call option: $\max(S_T - K, 0)$
   - Put option: $\max(K - S_T, 0)$

3. **Discount and average** the payoffs to get the option price:
   - Call price: $C = e^{-rT} \mathbb{E}[\max(S_T - K, 0)]$
   - Put price: $P = e^{-rT} \mathbb{E}[\max(K - S_T, 0)]$

### Variance Reduction Techniques

This package implements the **antithetic variates** technique, which:

1. Uses pairs of negatively correlated random variables $(Z, -Z)$ in the simulation
2. Averages the results to reduce variance
3. Typically achieves the same accuracy with fewer simulations

## Package Structure

- `models.py`: Core option pricing algorithms
- `visualization.py`: Plotting functions for analysis
- `cli.py`: Command-line interface
- `utils.py`: Utility functions for saving/loading results

## Limitations and Considerations

While powerful, the Monte Carlo approach has several limitations to consider:

1. **Computational Intensity**: Requires many iterations for accurate results, especially for:
   - Out-of-the-money options (K/S₀ >> 1 for calls, K/S₀ << 1 for puts)
   - Options with low volatility
   - Options near expiration

2. **Convergence Rate**: Monte Carlo error decreases as O(1/√n), meaning:
   - To halve the error, you need 4 times more simulations
   - Variance reduction techniques help but don't eliminate this issue

3. **Model Assumptions**:
   - Assumes geometric Brownian motion for stock prices
   - Constant volatility and interest rates
   - No transaction costs or early exercise
   - Perfect liquidity and continuous trading

4. **Implementation Considerations**:
   - Random number generator quality affects results
   - Numerical precision issues with very small probabilities
   - Not suitable for real-time pricing without optimizations

5. **Alternative Methods**: For European options, consider:
   - Analytical solutions (Black-Scholes) when available
   - Binomial/trinomial trees for smaller problems
   - Finite difference methods for some exotic options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Sandy Herho (sandy.herho@email.ucr.edu)

## Citation

If you use this package in your research, please cite it as:

```
@article{herho2025optionmc,
  author       = {Herho, Sandy},
  title        = {{OptionMC}: {A} {Python} package for {Monte} {Carlo} option pricing},
  journal      = {xxxx},
  year         = {2025},
  volume       = {xxx},
  number       = {xxx},
  pages        = {xxx},
  doi          = {10.5281/zenodo.15099722},
  url          = {https://doi.org/10.5281/zenodo.15099722}
}
```
