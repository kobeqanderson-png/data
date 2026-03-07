"""Basic cleaning pipeline functions.

Example usage:
    from src.cleaning import basic_clean
    df = pd.read_csv('data/raw/sample.csv')
    df_clean = basic_clean(df)
    df_clean.to_csv('data/processed/cleaned.csv', index=False)
"""

import pandas as pd
import numpy as np
from typing import List


def basic_clean(df: pd.DataFrame, date_cols: List[str] = None, id_cols: List[str] = None) -> pd.DataFrame:
    """Perform common cleaning steps:
    - strip column names
    - parse date columns
    - drop full duplicates
    - fill simple missing values for numeric cols with median

    Args:
        df: input DataFrame
        date_cols: list of columns to parse as dates
        id_cols: list of columns that must not be null (drop rows missing these)
    Returns:
        cleaned DataFrame
    """
    # column names
    df = df.copy()
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

    # parse dates
    if date_cols:
        for c in date_cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors='coerce')

    # drop rows missing required ids
    if id_cols:
        df = df.dropna(subset=[c for c in id_cols if c in df.columns])

    # drop exact duplicates
    df = df.drop_duplicates()

    # simple numeric imputation: fill NaN with median
    num_cols = df.select_dtypes(include=['number']).columns
    for c in num_cols:
        med = df[c].median()
        if pd.notna(med):
            df[c] = df[c].fillna(med)

    # trim string columns and fill NA with empty string
    obj_cols = df.select_dtypes(include=['object']).columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip().replace({'nan': ''})

    return df


def save_clean(df: pd.DataFrame, path_csv: str = None, path_parquet: str = None) -> None:
    """Save cleaned DataFrame to CSV and/or parquet as requested.

    Args:
        df: DataFrame to save
        path_csv: optional CSV path
        path_parquet: optional parquet path
    """
    if path_csv:
        df.to_csv(path_csv, index=False)
    if path_parquet:
        df.to_parquet(path_parquet, index=False)

