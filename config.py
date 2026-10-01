"""
Configuration module for the Conversion A/B Testing Simulator.
Defines global constants, random seeds, and default experiment settings.
"""

RANDOM_SEED = 42
DEFAULT_DAYS = 14
DEFAULT_CONTROL_RATE = 0.08  # 8% baseline conversion for Control
DEFAULT_VARIANT_RATE = 0.10  # 10% baseline conversion for Variant
DEFAULT_MIN_VISITORS = 800
DEFAULT_MAX_VISITORS = 1500
ALPHA = 0.05