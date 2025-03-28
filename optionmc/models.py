import numpy as np
from scipy.stats import norm

class OptionPricing:
    """
    European option pricing using Monte Carlo simulation with:
    - Variance reduction techniques
    - Error analysis
    - Confidence intervals
    - Benchmarking against analytical solutions
    """
    
    def __init__(self, S0, E, T, rf, sigma, iterations):
        """Initialize the model with given parameters"""
        self.S0 = S0          # Initial stock price
        self.E = E            # Strike price
        self.T = T            # Time to maturity in years
        self.rf = rf          # Risk-free rate
        self.sigma = sigma    # Volatility
        self.iterations = iterations  # Number of simulations
        
    def call_option_simulation(self, return_paths=False):
        """
        Calculate European call option price using standard Monte Carlo
        
        Parameters:
            return_paths (bool): If True, return stock paths and payoffs
            
        Returns:
            float: Option price estimate
            (and optionally) tuple: Stock prices, payoffs
        """
        # Generate random normal variables
        rand = np.random.normal(0, 1, [1, self.iterations])
        
        # Calculate stock prices using GBM
        stock_price = self.S0 * np.exp(
            self.T * (self.rf - 0.5 * self.sigma**2) + 
            self.sigma * np.sqrt(self.T) * rand
        )
        
        # Calculate payoffs
        payoffs = np.maximum(stock_price - self.E, 0)
        
        # Calculate option price
        option_price = np.exp(-self.rf * self.T) * np.mean(payoffs)
        
        if return_paths:
            return option_price, (stock_price, payoffs)
        return option_price
    
    def put_option_simulation(self, return_paths=False):
        """
        Calculate European put option price using standard Monte Carlo
        
        Parameters:
            return_paths (bool): If True, return stock paths and payoffs
            
        Returns:
            float: Option price estimate
            (and optionally) tuple: Stock prices, payoffs
        """
        # Generate random normal variables
        rand = np.random.normal(0, 1, [1, self.iterations])
        
        # Calculate stock prices using GBM
        stock_price = self.S0 * np.exp(
            self.T * (self.rf - 0.5 * self.sigma**2) + 
            self.sigma * np.sqrt(self.T) * rand
        )
        
        # Calculate payoffs
        payoffs = np.maximum(self.E - stock_price, 0)
        
        # Calculate option price
        option_price = np.exp(-self.rf * self.T) * np.mean(payoffs)
        
        if return_paths:
            return option_price, (stock_price, payoffs)
        return option_price
    
    def antithetic_call_simulation(self):
        """
        Calculate call option price using antithetic variates for variance reduction
        
        Returns:
            float: Option price estimate
        """
        # Generate one set of random normals
        rand = np.random.normal(0, 1, [1, self.iterations // 2])
        
        # Create antithetic variates
        rand_antithetic = -rand
        
        # Combine for efficiency
        combined_rand = np.concatenate((rand, rand_antithetic), axis=1)
        
        # Calculate stock prices
        stock_price = self.S0 * np.exp(
            self.T * (self.rf - 0.5 * self.sigma**2) + 
            self.sigma * np.sqrt(self.T) * combined_rand
        )
        
        # Calculate payoffs
        payoffs = np.maximum(stock_price - self.E, 0)
        
        # Calculate option price
        option_price = np.exp(-self.rf * self.T) * np.mean(payoffs)
        
        return option_price
    
    def antithetic_put_simulation(self):
        """
        Calculate put option price using antithetic variates for variance reduction
        
        Returns:
            float: Option price estimate
        """
        # Generate one set of random normals
        rand = np.random.normal(0, 1, [1, self.iterations // 2])
        
        # Create antithetic variates
        rand_antithetic = -rand
        
        # Combine for efficiency
        combined_rand = np.concatenate((rand, rand_antithetic), axis=1)
        
        # Calculate stock prices
        stock_price = self.S0 * np.exp(
            self.T * (self.rf - 0.5 * self.sigma**2) + 
            self.sigma * np.sqrt(self.T) * combined_rand
        )
        
        # Calculate payoffs
        payoffs = np.maximum(self.E - stock_price, 0)
        
        # Calculate option price
        option_price = np.exp(-self.rf * self.T) * np.mean(payoffs)
        
        return option_price
    
    def bs_analytical_price(self):
        """
        Calculate Black-Scholes analytical price for European options
        
        Returns:
            tuple: (call_price, put_price)
        """
        d1 = (np.log(self.S0 / self.E) + (self.rf + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        
        call_price = self.S0 * norm.cdf(d1) - self.E * np.exp(-self.rf * self.T) * norm.cdf(d2)
        put_price = self.E * np.exp(-self.rf * self.T) * norm.cdf(-d2) - self.S0 * norm.cdf(-d1)
        
        return call_price, put_price
    
    def confidence_intervals(self, price, confidence=0.95):
        """
        Calculate confidence interval for option price estimate
        
        Parameters:
            price (float): Option price estimate
            confidence (float): Confidence level (default: 0.95 for 95%)
            
        Returns:
            tuple: (lower_bound, upper_bound)
        """
        # Run multiple small simulations to get price distribution
        n_samples = 30
        subsample_size = self.iterations // n_samples
        prices = []
        
        for _ in range(n_samples):
            temp_pricer = OptionPricing(
                S0=self.S0, E=self.E, T=self.T, 
                rf=self.rf, sigma=self.sigma, 
                iterations=subsample_size
            )
            prices.append(temp_pricer.call_option_simulation())
        
        # Calculate standard error
        std_err = np.std(prices, ddof=1) / np.sqrt(n_samples)
        
        # Calculate z-score for given confidence
        z = norm.ppf((1 + confidence) / 2)
        
        return price - z * std_err, price + z * std_err
