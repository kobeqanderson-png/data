"""Quick smoke test to verify environment and run a tiny pipeline."""

import pandas as pd
import seaborn as sns
import numpy as np
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

