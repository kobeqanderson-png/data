"""Data loading helpers

Functions:
- read_csv(path) -> pd.DataFrame



These are thin wrappers around pandas to centralize read logic and default parameters.
"""

import io

import pandas as pd

def read_csv(file):
    # This list of encodings handles the 'utf-8' and 'latin1' errors
    encodings = ['utf-8', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            file.seek(0) # Reset file pointer to the beginning
            return pd.read_csv(file, encoding=enc, low_memory=False)
        except Exception:
            continue
    raise ValueError("Could not decode CSV. Try saving as an Excel file (.xlsx).")

def read_excel(file, sheet_name=0):
    return pd.read_excel(file, sheet_name=sheet_name)

def read_excel(path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Read Excel file (openpyxl recommended).

    Args:
        path: path to Excel file
        sheet_name: sheet name or index (default 0 = first sheet)
    """
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)

