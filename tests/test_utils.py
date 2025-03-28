import unittest
import os
import json
import numpy as np
from optionmc.utils import save_results, load_results, calculate_performance_metrics

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Create a test directory
        self.test_dir = 'test_utils_output'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test data
        self.test_results = {
            "parameters": {
                "initial_price": 100.0,
                "strike_price": 100.0,
                "time_to_maturity": 1.0,
                "risk_free_rate": 0.05,
                "volatility": 0.2,
                "iterations": 10000
            },
            "results": {
                "call_price": 10.5,
                "put_price": 5.6,
                "analytical_call": 10.45,
                "analytical_put": 5.57
            }
        }
    
    def tearDown(self):
        # Clean up test files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_save_load_results(self):
        """Test saving and loading results"""
        # Save results
        save_results(self.test_results, 'test_results.json', self.test_dir)
        
        # Check that file exists
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'test_results.json')))
        
        # Load results
        loaded_results = load_results('test_results.json', self.test_dir)
        
        # Check that loaded results match original
        self.assertEqual(loaded_results, self.test_results)
    
    def test_calculate_performance_metrics(self):
        """Test calculation of performance metrics"""
        mc_price = 10.5
        analytical_price = 10.45
        computation_time = 1.2
        
        metrics = calculate_performance_metrics(mc_price, analytical_price, computation_time)
        
        # Check metrics
        self.assertAlmostEqual(metrics['absolute_error'], 0.05)
        self.assertAlmostEqual(metrics['relative_error'], 0.05 / 10.45)
        self.assertEqual(metrics['computation_time'], 1.2)

if __name__ == '__main__':
    unittest.main()
