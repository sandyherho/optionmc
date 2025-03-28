import numpy as np
import json
import os

def save_results(results, filename, directory='.'):
    """
    Save simulation results to JSON file
    
    Parameters:
        results (dict): Dictionary of results
        filename (str): Output filename
        directory (str): Output directory
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Save to JSON
    with open(os.path.join(directory, filename), 'w') as f:
        json.dump(results, f, indent=2)

def load_results(filename, directory='.'):
    """
    Load simulation results from JSON file
    
    Parameters:
        filename (str): Input filename
        directory (str): Input directory
        
    Returns:
        dict: Dictionary of results
    """
    with open(os.path.join(directory, filename), 'r') as f:
        return json.load(f)

def calculate_performance_metrics(mc_price, analytical_price, computation_time):
    """
    Calculate performance metrics for the simulation
    
    Parameters:
        mc_price (float): Monte Carlo price estimate
        analytical_price (float): Analytical price
        computation_time (float): Computation time in seconds
        
    Returns:
        dict: Dictionary of performance metrics
    """
    return {
        'absolute_error': abs(mc_price - analytical_price),
        'relative_error': abs(mc_price - analytical_price) / analytical_price,
        'computation_time': computation_time
    }

def generate_parameter_series(param_name, min_val, max_val, num_points):
    """
    Generate a series of parameter values for sensitivity analysis
    
    Parameters:
        param_name (str): Parameter name
        min_val (float): Minimum value
        max_val (float): Maximum value
        num_points (int): Number of points
        
    Returns:
        dict: Dictionary with parameter name and values
    """
    if param_name.lower() in ['volatility', 'sigma']:
        # Use logarithmic scale for volatility
        values = np.exp(np.linspace(np.log(min_val), np.log(max_val), num_points))
    else:
        # Use linear scale for other parameters
        values = np.linspace(min_val, max_val, num_points)
    
    return {
        'name': param_name,
        'values': values
    }
