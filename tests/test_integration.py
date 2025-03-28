import unittest
import os
import tempfile
import shutil
import subprocess
import json
import sys

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for output
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_cli_basic(self):
        """Test basic CLI functionality"""
        # Run the CLI command using the module directly
        cmd = [
            sys.executable, '-m', 'optionmc.cli', 'price',
            '--s0', '100', 
            '--strike', '100', 
            '--volatility', '0.2', 
            '--iterations', '10000',
            '--output-dir', self.test_dir
        ]
        
        # Print the command for debugging
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print output for debugging
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
        # Check that the command ran successfully
        self.assertEqual(result.returncode, 0)
        
        # Check that output files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'results.json')))
        
        # Load and check results
        with open(os.path.join(self.test_dir, 'results.json'), 'r') as f:
            results = json.load(f)
        
        # Check that results contain expected fields
        self.assertIn('parameters', results)
        self.assertIn('results', results)
        self.assertIn('call_price', results['results'])
        self.assertIn('put_price', results['results'])

    def test_cli_antithetic(self):
        """Test CLI with antithetic variates"""
        # Run the CLI command with antithetic method
        cmd = [
            sys.executable, '-m', 'optionmc.cli', 'price',
            '--s0', '100', 
            '--strike', '100', 
            '--volatility', '0.2', 
            '--iterations', '10000',
            '--method', 'antithetic',
            '--output-dir', self.test_dir
        ]
        
        # Print the command for debugging
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print output for debugging
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
        # Check that the command ran successfully
        self.assertEqual(result.returncode, 0)
        
        # Load and check results
        with open(os.path.join(self.test_dir, 'results.json'), 'r') as f:
            results = json.load(f)
        
        # Check that method is correctly recorded
        self.assertIn('Antithetic', results['parameters']['method'])

if __name__ == '__main__':
    unittest.main()
