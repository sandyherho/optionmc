import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

class OptionVisualizer:
    """Generate publication-quality visualizations for option pricing"""
    
    def __init__(self, output_dir="figures", publication_mode=True):
        """Initialize visualizer with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set matplotlib style for publication quality
        if publication_mode:
            plt.style.use('bmh')
            plt.rcParams.update({
                'font.size': 12,
                'axes.labelsize': 14,
                'axes.titlesize': 16,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 12,
                'figure.figsize': (10, 6),
                'savefig.dpi': 300,
                'savefig.bbox': 'tight'
            })
    
    def _dollar_formatter(self, x, pos):
        """Format y-axis ticks with dollar signs"""
        return f'${x:.2f}'
    
    def plot_convergence(self, iterations, prices, ci_lower=None, ci_upper=None,
                         analytical=None, title=None, filename=None):
        """
        Plot Monte Carlo convergence with iterations
        
        Parameters:
            iterations: List of iteration counts
            prices: List of price estimates
            ci_lower, ci_upper: Confidence interval bounds (optional)
            analytical: Analytical solution (optional)
            title: Plot title
            filename: Filename to save plot (without extension)
        
        Returns:
            matplotlib figure
        """
        fig, ax = plt.subplots()
        
        # Create dollar formatter for y-axis
        dollar_format = FuncFormatter(self._dollar_formatter)
        ax.yaxis.set_major_formatter(dollar_format)
        
        # Plot MC estimates
        ax.plot(iterations, prices, 'o-', label='Monte Carlo Estimate', color='#1f77b4')
        
        # Plot confidence intervals if provided
        if ci_lower is not None and ci_upper is not None:
            ax.fill_between(iterations, ci_lower, ci_upper, alpha=0.2, 
                           color='#1f77b4', label='95% Confidence Interval')
        
        # Plot analytical solution if provided
        if analytical is not None:
            ax.axhline(y=analytical, color='#d62728', linestyle='--', 
                      label=f'Analytical Solution (${analytical:.2f})')
        
        # Add labels and title
        ax.set_xlabel('Number of Iterations')
        ax.set_ylabel('Option Price [$]')
        ax.set_title(title or 'Monte Carlo Convergence')
        ax.set_xscale('log')  # Log scale for iterations
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Save figure if filename provided
        if filename:
            fig.savefig(os.path.join(self.output_dir, f"{filename}.png"))
            fig.savefig(os.path.join(self.output_dir, f"{filename}.pdf"))
            
            # Save data for reproducibility
            data = pd.DataFrame({
                'iterations': iterations,
                'prices': prices,
                'ci_lower': ci_lower if ci_lower is not None else np.nan,
                'ci_upper': ci_upper if ci_upper is not None else np.nan,
                'analytical': [analytical] * len(iterations) if analytical is not None else np.nan
            })
            data.to_csv(os.path.join(self.output_dir, f"{filename}.csv"), index=False)
        
        return fig
    
    def plot_price_distribution(self, stock_prices, payoffs, title=None, filename=None):
        """
        Plot distribution of final stock prices and option payoffs
        
        Parameters:
            stock_prices: Array of final stock prices
            payoffs: Array of option payoffs
            title: Plot title
            filename: Filename to save plot (without extension)
            
        Returns:
            matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Create dollar formatter for axes
        dollar_format = FuncFormatter(self._dollar_formatter)
        ax1.xaxis.set_major_formatter(dollar_format)
        ax2.xaxis.set_major_formatter(dollar_format)
        
        # Plot stock price distribution
        sns.histplot(stock_prices.flatten(), kde=True, ax=ax1, color='#1f77b4')
        ax1.set_xlabel('Final Stock Price [$]')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Final Stock Prices')
        
        # Plot payoff distribution
        sns.histplot(payoffs.flatten(), kde=True, ax=ax2, color='#2ca02c')
        ax2.set_xlabel('Option Payoff [$]')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Option Payoffs')
        
        # Add overall title if provided
        if title:
            fig.suptitle(title, fontsize=16, y=1.05)
        
        plt.tight_layout()
        
        # Save figure if filename provided
        if filename:
            fig.savefig(os.path.join(self.output_dir, f"{filename}.png"))
            fig.savefig(os.path.join(self.output_dir, f"{filename}.pdf"))
            
            # Save data
            price_data = pd.DataFrame({'stock_prices': stock_prices.flatten()})
            payoff_data = pd.DataFrame({'payoffs': payoffs.flatten()})
            price_data.to_csv(os.path.join(self.output_dir, f"{filename}_prices.csv"), index=False)
            payoff_data.to_csv(os.path.join(self.output_dir, f"{filename}_payoffs.csv"), index=False)
        
        return fig
    
    def plot_parameter_sensitivity(self, parameter_values, prices, parameter_name, 
                                  analytical_prices=None, title=None, filename=None):
        """
        Plot option price sensitivity to a parameter
        
        Parameters:
            parameter_values: Array of parameter values
            prices: Corresponding option prices
            parameter_name: Name of parameter for labeling
            analytical_prices: Analytical prices (optional)
            title: Plot title
            filename: Filename to save plot (without extension)
            
        Returns:
            matplotlib figure
        """
        fig, ax = plt.subplots()
        
        # Create dollar formatter for y-axis
        dollar_format = FuncFormatter(self._dollar_formatter)
        ax.yaxis.set_major_formatter(dollar_format)
        
        # Plot MC estimates
        ax.plot(parameter_values, prices, 'o-', label='Monte Carlo', color='#1f77b4')
        
        # Plot analytical solution if provided
        if analytical_prices is not None:
            ax.plot(parameter_values, analytical_prices, 's--', 
                   label='Analytical', color='#d62728')
        
        # Add labels and title
        ax.set_xlabel(parameter_name)
        ax.set_ylabel('Option Price [$]')
        ax.set_title(title or f'Option Price Sensitivity to {parameter_name}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Save figure if filename provided
        if filename:
            fig.savefig(os.path.join(self.output_dir, f"{filename}.png"))
            fig.savefig(os.path.join(self.output_dir, f"{filename}.pdf"))
            
            # Save data
            data = pd.DataFrame({
                parameter_name: parameter_values,
                'mc_prices': prices,
                'analytical_prices': analytical_prices if analytical_prices is not None else np.nan
            })
            data.to_csv(os.path.join(self.output_dir, f"{filename}.csv"), index=False)
        
        return fig
