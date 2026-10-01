"""
Unit tests for statistical analysis module.
"""

import pandas as pd
from analysis import (
    calculate_lift,
    perform_two_proportion_z_test,
    summarize_experiment,
)


def test_calculate_lift():
    assert calculate_lift(0.08, 0.10) == 25.0
    assert calculate_lift(0.10, 0.10) == 0.0


def test_z_test_identical_groups():
    # Large identical sample sizes should yield p-value = 1.0 and z = 0.0
    z, p = perform_two_proportion_z_test(
        control_visitors=10000,
        control_conversions=800,
        variant_visitors=10000,
        variant_conversions=800,
    )
    assert z == 0.0
    assert p == 1.0


def test_z_test_significant_difference():
    # Clearly distinct proportions should yield statistical significance
    z, p = perform_two_proportion_z_test(
        control_visitors=5000,
        control_conversions=400,  # 8%
        variant_visitors=5000,
        variant_conversions=600,  # 12%
    )
    assert z > 0
    assert p < 0.05