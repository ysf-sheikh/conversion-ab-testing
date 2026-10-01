"""
Unit tests for data generation and validation.
"""

import pytest
import pandas as pd
from generate_data import generate_ab_test_data, validate_dataset


def test_generate_ab_test_data_shape():
    df = generate_ab_test_data(days=14)
    # 14 days * 2 groups = 28 rows
    assert len(df) == 28
    assert "date" in df.columns
    assert "group" in df.columns
    assert "visitors" in df.columns
    assert "conversions" in df.columns
    assert "conversion_rate" in df.columns


def test_data_validation_rules():
    df = generate_ab_test_data(days=14)
    # Should pass without error
    validate_dataset(df, expected_days=14)

    # Test failure on visitors <= 0
    df_invalid = df.copy()
    df_invalid.loc[0, "visitors"] = 0
    with pytest.raises(ValueError):
        validate_dataset(df_invalid)

    # Test failure on conversions > visitors
    df_invalid2 = df.copy()
    df_invalid2.loc[0, "conversions"] = df_invalid2.loc[0, "visitors"] + 5
    with pytest.raises(ValueError):
        validate_dataset(df_invalid2)