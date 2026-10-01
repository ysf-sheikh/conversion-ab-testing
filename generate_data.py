"""
Data generation module for the Conversion A/B Testing Simulator.
Simulates 14 days of website traffic and conversions for Control and Variant groups.
"""

import os
import numpy as np
import pandas as pd
from config import (
    RANDOM_SEED,
    DEFAULT_DAYS,
    DEFAULT_CONTROL_RATE,
    DEFAULT_VARIANT_RATE,
    DEFAULT_MIN_VISITORS,
    DEFAULT_MAX_VISITORS,
)


def generate_ab_test_data(
    days: int = DEFAULT_DAYS,
    control_base_rate: float = DEFAULT_CONTROL_RATE,
    variant_base_rate: float = DEFAULT_VARIANT_RATE,
    min_visitors: int = DEFAULT_MIN_VISITORS,
    max_visitors: int = DEFAULT_MAX_VISITORS,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Generates synthetic daily A/B testing data for Control and Variant groups."""
    np.random.seed(seed)
    start_date = pd.to_datetime("2026-01-01")
    dates = [start_date + pd.Timedelta(days=i) for i in range(days)]

    records = []
    for date in dates:
        # Simulate daily visitors with some natural day-of-week / random variation
        n_control = np.random.randint(min_visitors, max_visitors + 1)
        n_variant = np.random.randint(min_visitors, max_visitors + 1)

        # Introduce mild daily noise to conversion probabilities
        p_control_daily = np.clip(
            np.random.normal(control_base_rate, 0.005), 0.01, 0.99
        )
        p_variant_daily = np.clip(
            np.random.normal(variant_base_rate, 0.005), 0.01, 0.99
        )

        # Binomial sampling for conversion counts
        conv_control = np.random.binomial(n_control, p_control_daily)
        conv_variant = np.random.binomial(n_variant, p_variant_daily)

        records.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "group": "Control",
                "visitors": int(n_control),
                "conversions": int(conv_control),
                "conversion_rate": round(conv_control / n_control, 5),
            }
        )
        records.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "group": "Variant",
                "visitors": int(n_variant),
                "conversions": int(conv_variant),
                "conversion_rate": round(conv_variant / n_variant, 5),
            }
        )

    df = pd.DataFrame(records)
    validate_dataset(df, expected_days=days)
    return df


def validate_dataset(df: pd.DataFrame, expected_days: int = DEFAULT_DAYS) -> None:
    """Performs rigorous data validation checks on the generated DataFrame."""
    if df.empty:
        raise ValueError("Dataset is empty.")

    required_columns = {
        "date",
        "group",
        "visitors",
        "conversions",
        "conversion_rate",
    }
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Expected: {required_columns}")

    if (df["visitors"] <= 0).any():
        raise ValueError("Found non-positive visitor counts.")

    if (df["conversions"] < 0).any() or (df["conversions"] > df["visitors"]).any():
        raise ValueError("Invalid conversion counts detected (conversions > visitors or < 0).")

    if not ((df["conversion_rate"] >= 0) & (df["conversion_rate"] <= 1)).all():
        raise ValueError("Conversion rates out of bounds [0, 1].")

    groups = df["group"].unique()
    if set(groups) != {"Control", "Variant"} or len(groups) != 2:
        raise ValueError(f"Expected exactly 'Control' and 'Variant' groups. Found: {groups}")

    if df["date"].nunique() != expected_days:
        raise ValueError(f"Expected {expected_days} unique dates, found {df['date'].nunique()}.")

    if df.duplicated(subset=["date", "group"]).any():
        raise ValueError("Duplicate date/group combinations found.")


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df_data = generate_ab_test_data()
    output_path = os.path.join("data", "ab_test_data.csv")
    df_data.to_csv(output_path, index=False)
    print(f"Successfully generated dataset with {len(df_data)} rows and saved to {output_path}")