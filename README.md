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

### Black-Scholes Option Pricing: Derivation and Implementation

The Black-Scholes model provides analytical solutions for European options based on a partial differential equation approach. This package implements the closed-form solution as a benchmark for Monte Carlo simulations.

#### Derivation Overview

The derivation starts with several key assumptions:
- Stock prices follow geometric Brownian motion
- Markets are frictionless with no arbitrage opportunities
- Volatility and risk-free rate remain constant
- Trading occurs continuously
- No dividends are paid during the option's life

Under these assumptions, the stock price follows the stochastic differential equation:

$dS_t = \mu S_t dt + \sigma S_t dW_t$

Where $W_t$ is a Wiener process (Brownian motion), $\mu$ is the drift, and $\sigma$ is the volatility.

The Black-Scholes partial differential equation is:

$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$

Solving this equation with appropriate boundary conditions yields the closed-form solutions:

For a European call option:

$C = S_0 \Phi(d_1) - Ke^{-rT} \Phi(d_2)$

For a European put option:

$P = Ke^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1)$

Where:
- $S_0$ is the initial stock price
- $K$ is the strike price
- $r$ is the risk-free rate
- $T$ is the time to maturity (in years)
- $\Phi(\cdot)$ is the cumulative distribution function of the standard normal distribution
- $d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$
- $d_2 = d_1 - \sigma\sqrt{T}$

#### Why Use the Analytical Solution?

This package implements both Monte Carlo simulation and the analytical Black-Scholes solution for several reasons:

1. **Benchmarking**: The analytical solution provides a precise benchmark to validate the accuracy of Monte Carlo simulations
2. **Educational Value**: Comparing both methods helps users understand the trade-offs between analytical and numerical approaches
3. **Efficiency**: For standard European options, the analytical solution is computationally more efficient
4. **Error Analysis**: Having an exact solution allows for precise error measurements in the Monte Carlo implementation

#### Limitations of the Black-Scholes Model

Despite its elegance, the Black-Scholes model has several limitations:

1. **Constant Volatility**: Assumes volatility remains constant throughout the option's life, contradicting observed "volatility smiles" in markets
2. **Log-normal Distribution**: Assumes returns follow a normal distribution, which often understates the probability of extreme market moves
3. **Continuous Trading**: Assumes continuous hedging with no transaction costs, which is impractical in real markets
4. **Constant Interest Rates**: Assumes risk-free rates remain fixed, which may not hold for longer-dated options
5. **No Early Exercise**: Only applies to European options, not American options that allow early exercise
6. **No Dividends**: The basic model doesn't account for dividend payments (though extensions exist)

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

### Monte Carlo Simulation Limitations

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

### Package-Specific Limitations

The current implementation of OptionMC has several limitations:

1. **European Options Only**: Limited to European-style options; does not support American or exotic options
2. **Single-Factor Models**: Only models stock price as the underlying stochastic process
3. **Basic Variance Reduction**: Implements antithetic variates but not other techniques like control variates or importance sampling
4. **No Path-Dependent Features**: Cannot handle path-dependent options like Asian options or barrier options
5. **No Dividend Support**: Current implementation does not account for dividend payments

### When to Use Alternative Methods

For certain option pricing scenarios, consider alternatives:

1. **Analytical Solutions**: 
   - Black-Scholes for standard European options (faster and more accurate)
   - Closed-form extensions for simple dividend models or barrier options

2. **Lattice Methods**:
   - Binomial/trinomial trees for American options with early exercise
   - Better for visualizing the evolution of option prices over time

3. **Finite Difference Methods**:
   - For solving complex PDEs associated with exotic options
   - Often more efficient than Monte Carlo for low-dimensional problems

4. **Fourier Transform Methods**:
   - For options with known characteristic functions
   - Often more efficient for certain exotic options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Sandy H. S. Herho <sandy.herho@email.ucr.edu>
- Siti N. Kaban
- Cahya Nugraha

## Citation

If you use this package in your study, please cite it as:

```latex
@article{Herho2025OptionMC,
  title = {{OptionMC}: A {Python} Package for {Monte Carlo} Pricing of {European} Options},
  author = {Herho, Sandy H. S. and Kaban, Siti N. and Nugraha, Cahya},
  journal = {International Journal of Data Science},
  volume = {6},
  number = {2},
  pages = {70--84},
  year = {2025},
  note={\url{https://doi.org/10.18517/ijods.6.2.70-84.2025}}
}
```
