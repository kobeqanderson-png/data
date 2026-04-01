"""Feature engineering helpers.

Provides small, reusable feature transformations for demonstration.
"""

import pandas as pd
import numpy as np
from typing import List


def add_log_feature(df: pd.DataFrame, col: str, new_col: str = None) -> pd.DataFrame:
    """Add a log1p transformed feature (handles zeros and negatives by applying on clipped values).

    Args:
        df: input DataFrame
        col: numeric column to transform
        new_col: name of the new column; if None uses `{col}_log`
    Returns:
        new DataFrame with feature added
    """
    df = df.copy()
    new_col = new_col or f"{col}_log"
    # clip to non-negative to avoid complex numbers; if negatives exist, shift by min value
    series = pd.to_numeric(df[col], errors='coerce').fillna(0)
    minv = series.min()
    if minv < 0:
        series = series + abs(minv)
    df[new_col] = np.log1p(series)
    return df


def add_missing_indicators(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        df[f"{c}_missing"] = df[c].isna().astype(int)
    return df


def add_polynomial_features(df: pd.DataFrame, col: str, degree: int = 2) -> pd.DataFrame:
    """Add polynomial features (e.g., square, cube) for a numeric column.

    Args:
        df: input DataFrame
        col: numeric column to transform
        degree: polynomial degree (2 for quadratic, 3 for cubic, etc.)
    Returns:
        new DataFrame with polynomial features added
    """
    df = df.copy()
    series = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for d in range(2, degree + 1):
        df[f"{col}_pow{d}"] = np.power(series, d)
    return df


def add_interaction_features(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """Add interaction term between two numeric columns.

    Args:
        df: input DataFrame
        col1: first numeric column
        col2: second numeric column
    Returns:
        new DataFrame with interaction feature added
    """
    df = df.copy()
    series1 = pd.to_numeric(df[col1], errors='coerce').fillna(0)
    series2 = pd.to_numeric(df[col2], errors='coerce').fillna(0)
    df[f"{col1}_x_{col2}"] = series1 * series2
    return df


def standardize_features(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Standardize numeric columns to mean=0, std=1.

    Args:
        df: input DataFrame
        cols: list of numeric columns to standardize
    Returns:
        new DataFrame with standardized features
    """
    df = df.copy()
    for col in cols:
        series = pd.to_numeric(df[col], errors='coerce')
        mean = series.mean()
        std = series.std()
        if std > 0:
            df[f"{col}_std"] = (series - mean) / std
        else:
            df[f"{col}_std"] = 0
    return df

