"""Small visualization helpers using seaborn/matplotlib."""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional


def boxplot_by_category(df: pd.DataFrame, cat_col: str, value_col: str, out_path: Optional[str] = None):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x=cat_col, y=value_col)
    plt.title(f"{value_col} distribution by {cat_col}")
    plt.tight_layout()
    if out_path:
        plt.savefig(out_path)
    else:
        plt.show()


def countplot(df: pd.DataFrame, col: str, out_path: Optional[str] = None):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,5))
    sns.countplot(data=df, x=col)
    plt.tight_layout()
    if out_path:
        plt.savefig(out_path)
    else:
        plt.show()

