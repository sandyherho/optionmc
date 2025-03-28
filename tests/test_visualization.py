import unittest
import os
import numpy as np
import matplotlib.pyplot as plt
from optionmc.visualization import OptionVisualizer

class TestOptionVisualizer(unittest.TestCase):
    def setUp(self):
        # Create a test directory for output
        self.test_dir = 'test_output'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a visualizer instance
        self.visualizer = OptionVisualizer(output_dir=self.test_dir)
    
    def tearDown(self):
        # Clean up test files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_plot_convergence(self):
        """Test that convergence plot is created correctly"""
        # Create test data
        iterations = np.logspace(2, 5, 10).astype(int)
        prices = np.linspace(10, 12, 10) + np.random.normal(0, 0.1, 10)
        ci_lower = prices - 0.5
        ci_upper = prices + 0.5
        analytical = 11.0
        
        # Create plot
        fig = self.visualizer.plot_convergence(
            iterations, prices, ci_lower, ci_upper, analytical,
            title="Test Convergence Plot", filename="test_convergence"
        )
        
        # Check that files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_convergence.png")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_convergence.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_convergence.csv")))
        
        # Check that figure was returned
        self.assertIsInstance(fig, plt.Figure)
    
    def test_plot_price_distribution(self):
        """Test that price distribution plot is created correctly"""
        # Create test data
        stock_prices = np.random.normal(100, 10, (1, 1000))
        payoffs = np.maximum(stock_prices - 100, 0)
        
        # Create plot
        fig = self.visualizer.plot_price_distribution(
            stock_prices, payoffs,
            title="Test Distribution Plot", filename="test_distribution"
        )
        
        # Check that files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_distribution.png")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_distribution.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_distribution_prices.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_distribution_payoffs.csv")))
        
        # Check that figure was returned
        self.assertIsInstance(fig, plt.Figure)
    
    def test_plot_parameter_sensitivity(self):
        """Test that parameter sensitivity plot is created correctly"""
        # Create test data
        parameter_values = np.linspace(0.1, 0.5, 10)
        prices = 10 + parameter_values * 20 + np.random.normal(0, 0.5, 10)
        analytical_prices = 10 + parameter_values * 20
        
        # Create plot
        fig = self.visualizer.plot_parameter_sensitivity(
            parameter_values, prices, "Volatility",
            analytical_prices=analytical_prices,
            title="Test Sensitivity Plot", filename="test_sensitivity"
        )
        
        # Check that files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_sensitivity.png")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_sensitivity.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_sensitivity.csv")))
        
        # Check that figure was returned
        self.assertIsInstance(fig, plt.Figure)

if __name__ == '__main__':
    unittest.main()
