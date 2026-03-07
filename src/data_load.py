"""Data loading helpers

Functions:
- read_csv(path) -> pd.DataFrame



These are thin wrappers around pandas to centralize read logic and default parameters.
"""

import pandas as pd


def read_csv(path: str, **kwargs) -> pd.DataFrame:
    """Read CSV with sensible defaults.

    Args:
        path: path to CSV file
        **kwargs: forwarded to pd.read_csv
    Returns:
        DataFrame
    """
    defaults = dict(encoding='utf-8', low_memory=False)
    defaults.update(kwargs)
    return pd.read_csv(path, **defaults)


def read_excel(path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Read Excel file (openpyxl recommended).

    Args:
        path: path to Excel file
        sheet_name: sheet name or index (default 0 = first sheet)
    """
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)

