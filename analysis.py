"""
Statistical analysis module for the Conversion A/B Testing Simulator.
Contains pure functions for hypothesis testing, confidence intervals, and metrics calculation.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Dict, Any, Tuple


def calculate_group_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates total visitors and conversions by group."""
    summary = (
        df.groupby("group")
        .agg({"visitors": "sum", "conversions": "sum"})
        .reset_index()
    )
    summary["conversion_rate"] = summary["conversions"] / summary["visitors"]
    return summary


def calculate_lift(control_rate: float, variant_rate: float) -> float:
    """Calculates relative conversion lift percentage of Variant over Control."""
    if control_rate == 0:
        return 0.0
    return ((variant_rate - control_rate) / control_rate) * 100


def perform_two_proportion_z_test(
    control_visitors: int,
    control_conversions: int,
    variant_visitors: int,
    variant_conversions: int,
) -> Tuple[float, float]:
    """
    Performs a standard two-proportion Z-test.
    Returns: (z_statistic, p_value)
    """
    x1 = control_conversions
    n1 = control_visitors
    x2 = variant_conversions
    n2 = variant_visitors

    p1 = x1 / n1
    p2 = x2 / n2

    # Pooled proportion under null hypothesis H0: p1 = p2
    p_pool = (x1 + x2) / (n1 + n2)

    if p_pool == 0 or p_pool == 1:
        return 0.0, 1.0

    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0

    z_stat = (p2 - p1) / se
    # Two-tailed p-value
    p_val = 2 * (1 - norm.cdf(abs(z_stat)))

    return float(z_stat), float(p_val)


def calculate_confidence_interval(
    control_visitors: int,
    control_conversions: int,
    variant_visitors: int,
    variant_conversions: int,
    alpha: float = 0.05,
) -> Tuple[float, float]:
    """Calculates a (1 - alpha) confidence interval for the difference in proportions (p_variant - p_control)."""
    p1 = control_conversions / control_visitors
    p2 = variant_conversions / variant_visitors

    se_diff = np.sqrt(
        (p1 * (1 - p1) / control_visitors) + (p2 * (1 - p2) / variant_visitors)
    )
    z_crit = norm.ppf(1 - alpha / 2)

    diff = p2 - p1
    margin_of_error = z_crit * se_diff

    return float(diff - margin_of_error), float(diff + margin_of_error)


def summarize_experiment(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
    """Performs full statistical summarization of the A/B test dataset."""
    totals = calculate_group_totals(df)

    control_row = totals[totals["group"] == "Control"].iloc[0]
    variant_row = totals[totals["group"] == "Variant"].iloc[0]

    n_control, x_control, r_control = (
        int(control_row["visitors"]),
        int(control_row["conversions"]),
        float(control_row["conversion_rate"]),
    )
    n_variant, x_variant, r_variant = (
        int(variant_row["visitors"]),
        int(variant_row["conversions"]),
        float(variant_row["conversion_rate"]),
    )

    abs_diff_pp = (r_variant - r_control) * 100
    rel_lift = calculate_lift(r_control, r_variant)

    z_stat, p_val = perform_two_proportion_z_test(
        n_control, x_control, n_variant, x_variant
    )
    ci_lower, ci_upper = calculate_confidence_interval(
        n_control, x_control, n_variant, x_variant, alpha=alpha
    )

    is_significant = p_val < alpha

    return {
        "control_visitors": n_control,
        "control_conversions": x_control,
        "control_rate": r_control,
        "variant_visitors": n_variant,
        "variant_conversions": x_variant,
        "variant_rate": r_variant,
        "absolute_difference_pp": abs_diff_pp,
        "relative_lift": rel_lift,
        "z_statistic": z_stat,
        "p_value": p_val,
        "alpha": alpha,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "is_significant": is_significant,
    }