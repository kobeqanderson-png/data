"""Data loading helpers

Functions:
- read_csv(path) -> pd.DataFrame



These are thin wrappers around pandas to centralize read logic and default parameters.
"""

import pandas as pd


import pandas as pd

def read_csv(file):
    try:
        # First, try standard UTF-8
        return pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        # If that fails, try 'latin1' (ISO-8859-1), which handles special symbols
        return pd.read_csv(file, encoding='latin1')


def read_excel(path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Read Excel file (openpyxl recommended).

    Args:
        path: path to Excel file
        sheet_name: sheet name or index (default 0 = first sheet)
    """
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)

