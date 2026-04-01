"""Quick smoke test to verify environment and run a tiny pipeline."""

import pandas as pd
import seaborn as sns
import numpy as np

try:
    from src.cleaning import basic_clean
    from src.features import add_log_feature
except ModuleNotFoundError:
    # Support direct script execution: python src/quick_test.py
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from src.cleaning import basic_clean
    from src.features import add_log_feature


def main():
    print("pandas", pd.__version__)
    print("seaborn", sns.__version__)

    # create small sample
    df = pd.DataFrame({
        'id': [1,2,2,3],
        'date': ['2020-01-01','2020-01-02', None, 'not a date'],
        'value': [10, 20, None, 40],
        'category': ['a','b','b','a']
    })

    print("\nOriginal:\n", df)
    dfc = basic_clean(df, date_cols=['date'], id_cols=['id'])
    dfc = add_log_feature(dfc, 'value')
    print("\nCleaned:\n", dfc)

if __name__ == '__main__':
    main()

