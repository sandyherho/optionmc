import argparse
import numpy as np
import time
import os
import warnings
from .models import OptionPricing
from .visualization import OptionVisualizer
from .utils import save_results, calculate_performance_metrics

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fontTools")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

def price_options(args):
    """Calculate and visualize option prices"""
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set random seed if provided
    if args.seed is not None:
        np.random.seed(args.seed)
    
    try:
        # Initialize pricer
        pricer = OptionPricing(
            S0=args.s0, 
            E=args.strike, 
            T=args.time, 
            rf=args.rate, 
            sigma=args.volatility, 
            iterations=args.iterations
        )
        
        # Calculate option prices
        start_time = time.time()
        
        if args.method == 'standard':
            call_price, (stock_prices, call_payoffs) = pricer.call_option_simulation(return_paths=True)
            put_price, (_, put_payoffs) = pricer.put_option_simulation(return_paths=True)
            method_name = "Standard Monte Carlo"
        else:
            call_price = pricer.antithetic_call_simulation()
            put_price = pricer.antithetic_put_simulation()
            # Get paths for visualization (with fewer iterations)
            vis_pricer = OptionPricing(
                S0=args.s0, E=args.strike, T=args.time, 
                rf=args.rate, sigma=args.volatility, iterations=10000
            )
            _, (stock_prices, call_payoffs) = vis_pricer.call_option_simulation(return_paths=True)
            _, (_, put_payoffs) = vis_pricer.put_option_simulation(return_paths=True)
            method_name = "Antithetic Variates Monte Carlo"
        
        computation_time = time.time() - start_time
        
        # Get analytical solution
        bs_call, bs_put = pricer.bs_analytical_price()
        
        # Calculate performance metrics
        call_metrics = calculate_performance_metrics(call_price, bs_call, computation_time)
        put_metrics = calculate_performance_metrics(put_price, bs_put, computation_time)
        
        # Create visualizer
        visualizer = OptionVisualizer(output_dir=args.output_dir)
        
        try:
            # Create iteration lists for convergence plots
            iter_list = np.logspace(2, np.log10(args.iterations), 10).astype(int)
            
            # Lists for call option data
            call_prices = []
            call_ci_lower = []
            call_ci_upper = []
            
            # Lists for put option data
            put_prices = []
            put_ci_lower = []
            put_ci_upper = []
            
            # Calculate prices at different iteration counts
            for n in iter_list:
                temp_pricer = OptionPricing(
                    S0=args.s0, E=args.strike, T=args.time, 
                    rf=args.rate, sigma=args.volatility, iterations=n
                )
                
                # Call option prices
                if args.method == 'standard':
                    call_price = temp_pricer.call_option_simulation()
                    put_price = temp_pricer.put_option_simulation()
                else:
                    call_price = temp_pricer.antithetic_call_simulation()
                    put_price = temp_pricer.antithetic_put_simulation()
                
                # Get confidence intervals for call
                call_low, call_high = temp_pricer.confidence_intervals(call_price)
                call_prices.append(call_price)
                call_ci_lower.append(call_low)
                call_ci_upper.append(call_high)
                
                # Get confidence intervals for put (using same method but with put price)
                put_low, put_high = temp_pricer.confidence_intervals(put_price)
                put_prices.append(put_price)
                put_ci_lower.append(put_low)
                put_ci_upper.append(put_high)
            
            # Create call option convergence plot
            visualizer.plot_convergence(
                iter_list, call_prices, ci_lower=call_ci_lower, ci_upper=call_ci_upper, 
                analytical=bs_call,
                title=f'Call Option Price Convergence (K=${args.strike}, T={args.time}yr, σ={args.volatility})',
                filename='call_convergence'
            )
            
            # Create put option convergence plot
            visualizer.plot_convergence(
                iter_list, put_prices, ci_lower=put_ci_lower, ci_upper=put_ci_upper, 
                analytical=bs_put,
                title=f'Put Option Price Convergence (K=${args.strike}, T={args.time}yr, σ={args.volatility})',
                filename='put_convergence'
            )
            
            # Plot price distributions
            visualizer.plot_price_distribution(
                stock_prices, call_payoffs,
                title=f'Stock Price and Call Option Payoff Distributions (S0=${args.s0}, K=${args.strike})',
                filename='call_distributions'
            )
            
            visualizer.plot_price_distribution(
                stock_prices, put_payoffs,
                title=f'Stock Price and Put Option Payoff Distributions (S0=${args.s0}, K=${args.strike})',
                filename='put_distributions'
            )
            
            # Plot volatility sensitivity for call options
            vol_range = np.linspace(max(0.05, args.volatility/2), min(0.8, args.volatility*2), 10)
            call_vol_prices = []
            put_vol_prices = []
            call_vol_analytical = []
            put_vol_analytical = []
            
            for vol in vol_range:
                temp_pricer = OptionPricing(
                    S0=args.s0, E=args.strike, T=args.time, 
                    rf=args.rate, sigma=vol, iterations=args.iterations//10
                )
                
                # Get Monte Carlo prices
                if args.method == 'standard':
                    call_price = temp_pricer.call_option_simulation()
                    put_price = temp_pricer.put_option_simulation()
                else:
                    call_price = temp_pricer.antithetic_call_simulation()
                    put_price = temp_pricer.antithetic_put_simulation()
                    
                call_vol_prices.append(call_price)
                put_vol_prices.append(put_price)
                
                # Get analytical prices
                bs_call, bs_put = temp_pricer.bs_analytical_price()
                call_vol_analytical.append(bs_call)
                put_vol_analytical.append(bs_put)
            
            # Create volatility sensitivity plots
            visualizer.plot_parameter_sensitivity(
                vol_range, call_vol_prices, 'Volatility',
                analytical_prices=call_vol_analytical,
                title='Call Option Price Sensitivity to Volatility',
                filename='call_volatility_sensitivity'
            )
            
            visualizer.plot_parameter_sensitivity(
                vol_range, put_vol_prices, 'Volatility',
                analytical_prices=put_vol_analytical,
                title='Put Option Price Sensitivity to Volatility',
                filename='put_volatility_sensitivity'
            )
            
        except Exception as viz_error:
            print(f"Warning: Visualization error (but calculation succeeded): {viz_error}")
        
        # Save results
        results = {
            "parameters": {
                "initial_price": args.s0,
                "strike_price": args.strike,
                "time_to_maturity": args.time,
                "risk_free_rate": args.rate,
                "volatility": args.volatility,
                "iterations": args.iterations,
                "method": method_name
            },
            "results": {
                "call_price": call_price,
                "put_price": put_price,
                "analytical_call": bs_call,
                "analytical_put": bs_put,
                "call_error": call_metrics['absolute_error'],
                "put_error": put_metrics['absolute_error'],
                "call_relative_error": call_metrics['relative_error'],
                "put_relative_error": put_metrics['relative_error'],
                "computation_time": computation_time
            }
        }
        
        save_results(results, 'results.json', args.output_dir)
        
        # Print results
        print(f"Method: {method_name}")
        print(f"Call Option Price: ${call_price:.4f} (Analytical: ${bs_call:.4f})")
        print(f"Put Option Price: ${put_price:.4f} (Analytical: ${bs_put:.4f})")
        print(f"Relative Error (Call): {call_metrics['relative_error']:.4%}")
        print(f"Relative Error (Put): {put_metrics['relative_error']:.4%}")
        print(f"Computation Time: {computation_time:.2f} seconds")
        print(f"Results and visualizations saved to {args.output_dir}/")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description='Monte Carlo Option Pricing Tool')
    subparsers = parser.add_subparsers(dest='command')
    
    # Price command
    price_parser = subparsers.add_parser('price', help='Calculate option prices')
    price_parser.add_argument('--s0', type=float, default=100.0, help='Initial stock price')
    price_parser.add_argument('--strike', type=float, default=100.0, help='Strike price')
    price_parser.add_argument('--time', type=float, default=1.0, help='Time to maturity in years')
    price_parser.add_argument('--rate', type=float, default=0.05, help='Risk-free interest rate')
    price_parser.add_argument('--volatility', type=float, default=0.2, help='Volatility')
    price_parser.add_argument('--iterations', type=int, default=100000, help='Number of simulations')
    price_parser.add_argument('--method', choices=['standard', 'antithetic'], default='standard', help='Monte Carlo method')
    price_parser.add_argument('--seed', type=int, default=None, help='Random seed')
    price_parser.add_argument('--output-dir', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    if args.command == 'price':
        return price_options(args)
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
