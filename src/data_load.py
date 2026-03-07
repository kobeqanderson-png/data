"""Data loading helpers

Functions:
- read_csv(path) -> pd.DataFrame



These are thin wrappers around pandas to centralize read logic and default parameters.
"""

import pandas as pd


import pandas as pd

import pandas as pd
import io

def read_csv(file):
    # Try the most common encodings used in research data
    encodings = ['utf-8', 'latin1', 'cp1252']
    
    for enc in encodings:
        try:
            # We seek to 0 to ensure we read from the start of the file
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except (UnicodeDecodeError, Exception):
            continue
            
    raise ValueError("Could not decode CSV file. Please try saving it as an Excel file (.xlsx) instead.")

def read_excel(file):
    return pd.read_excel(file)

def read_excel(path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Read Excel file (openpyxl recommended).

    Args:
        path: path to Excel file
        sheet_name: sheet name or index (default 0 = first sheet)
    """
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)

