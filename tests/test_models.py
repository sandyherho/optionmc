import unittest
import numpy as np
from optionmc.models import OptionPricing

class TestOptionPricing(unittest.TestCase):
    def setUp(self):
        # Set fixed seed for reproducibility
        np.random.seed(42)
        
        # Create a standard option pricing instance for testing
        self.pricer = OptionPricing(
            S0=100.0,    # Initial stock price
            E=100.0,     # Strike price
            T=1.0,       # Time to maturity (1 year)
            rf=0.05,     # Risk-free rate (5%)
            sigma=0.2,   # Volatility (20%)
            iterations=10000  # Lower iterations for faster tests
        )
    
    def test_bs_analytical_price(self):
        """Test that Black-Scholes formula gives expected results"""
        call_price, put_price = self.pricer.bs_analytical_price()
        
        # Expected values calculated using known BS formula
        expected_call = 10.45
        expected_put = 5.57
        
        # Assert with tolerance
        self.assertAlmostEqual(call_price, expected_call, delta=0.1)
        self.assertAlmostEqual(put_price, expected_put, delta=0.1)
    
    def test_call_option_simulation(self):
        """Test that Monte Carlo call price is close to analytical solution"""
        # Get the Monte Carlo price
        mc_price = self.pricer.call_option_simulation()
        
        # Get the analytical price
        bs_price, _ = self.pricer.bs_analytical_price()
        
        # Assert that Monte Carlo price is within 5% of BS price
        # (using a higher tolerance due to random simulation)
        percent_diff = abs(mc_price - bs_price) / bs_price
        self.assertLess(percent_diff, 0.05)
    
    def test_put_option_simulation(self):
        """Test that Monte Carlo put price is close to analytical solution"""
        # Get the Monte Carlo price
        mc_price = self.pricer.put_option_simulation()
        
        # Get the analytical price
        _, bs_price = self.pricer.bs_analytical_price()
        
        # Assert that Monte Carlo price is within 5% of BS price
        percent_diff = abs(mc_price - bs_price) / bs_price
        self.assertLess(percent_diff, 0.05)
    
    def test_antithetic_call_simulation(self):
        """Test that antithetic variates method works"""
        # Get prices with standard and antithetic methods
        standard_price = self.pricer.call_option_simulation()
        antithetic_price = self.pricer.antithetic_call_simulation()
        
        # Get the analytical price
        bs_price, _ = self.pricer.bs_analytical_price()
        
        # Both should be close to BS price
        std_percent_diff = abs(standard_price - bs_price) / bs_price
        anti_percent_diff = abs(antithetic_price - bs_price) / bs_price
        
        self.assertLess(std_percent_diff, 0.05)
        self.assertLess(anti_percent_diff, 0.05)
    
    def test_confidence_intervals(self):
        """Test that confidence intervals contain the analytical price"""
        # Get a price estimate
        price = self.pricer.call_option_simulation()
        
        # Get confidence intervals
        lower, upper = self.pricer.confidence_intervals(price)
        
        # Get analytical price
        bs_price, _ = self.pricer.bs_analytical_price()
        
        # Assert that analytical price is within confidence interval
        # (may occasionally fail due to randomness)
        self.assertLessEqual(lower, bs_price)
        self.assertGreaterEqual(upper, bs_price)

if __name__ == '__main__':
    unittest.main()
