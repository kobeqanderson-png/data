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

