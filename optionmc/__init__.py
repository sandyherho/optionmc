"""
OptionMC: Monte Carlo Option Pricing

A simple yet rigorous Monte Carlo simulation package for European option pricing
with beautiful visualization capabilities.
"""

__version__ = '0.1.3.4'

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fontTools")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

from .models import OptionPricing
from .visualization import OptionVisualizer
