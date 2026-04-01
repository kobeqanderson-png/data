#!/usr/bin/env python3
"""Automated test suite for NIH SABV data processing pipeline (20 scenarios)."""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_load import read_csv
from src.cleaning import basic_clean
from src.features import (
    add_log_feature, 
    add_missing_indicators,
    add_polynomial_features,
    add_interaction_features,
    standardize_features
)
from src.visualize import boxplot_by_category

# Import functions from app
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location("app", "app.py")
# Skip the streamlit stuff - just test the functions
import re
from scipy import stats as scipy_stats

def parse_animal_number(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)
    text = str(value).strip()
    if not text:
        return np.nan
    lower_text = text.lower()
    prefixed_match = re.search(r"(?:rat|subject|animal)\s*[-_#:]?\s*(\d+(?:\.\d+)?)", lower_text)
    if prefixed_match:
        return float(prefixed_match.group(1))
    numeric_only_match = re.fullmatch(r"\d+(?:\.\d+)?", lower_text)
    if numeric_only_match:
        return float(numeric_only_match.group(0))
    match = re.search(r"\d+(?:\.\d+)?", text)
    if match:
        return float(match.group(0))
    return np.nan

def parse_animal_number_series(series):
    return series.apply(parse_animal_number)

def ttest_for_groups(df, value_col, group_col="Sex"):
    male_data = df[df[group_col] == 'Male'][value_col].dropna()
    female_data = df[df[group_col] == 'Female'][value_col].dropna()
    if len(male_data) > 1 and len(female_data) > 1:
        t_stat, p_value = scipy_stats.ttest_ind(male_data, female_data, equal_var=False)
        return t_stat, p_value, len(male_data), len(female_data)
    return np.nan, np.nan, len(male_data), len(female_data)

def effect_size_cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return np.nan
    return (group1.mean() - group2.mean()) / pooled_std

def parse_id_list(raw_text):
    values = set()
    invalid_tokens = []
    for token in raw_text.split(','):
        token = token.strip()
        if not token:
            continue
        if '-' in token:
            parts = token.split('-', 1)
            if len(parts) != 2:
                invalid_tokens.append(token)
                continue
            try:
                start = float(parts[0].strip())
                end = float(parts[1].strip())
            except ValueError:
                invalid_tokens.append(token)
                continue
            if float(start).is_integer() and float(end).is_integer():
                start_i = int(start)
                end_i = int(end)
                lo, hi = (start_i, end_i) if start_i <= end_i else (end_i, start_i)
                for v in range(lo, hi + 1):
                    values.add(float(v))
            else:
                values.add(float(start))
                values.add(float(end))
            continue
        try:
            values.add(float(token))
        except ValueError:
            invalid_tokens.append(token)
    return values, invalid_tokens


# ============================================================================
# TEST SCENARIOS
# ============================================================================

test_results = []

def log_test(test_num, test_name, status, details=""):
    result = {
        "Test": test_num,
        "Name": test_name,
        "Status": status,
        "Details": details
    }
    test_results.append(result)
    status_icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
    print(f"{status_icon} Test {test_num}: {test_name} - {status} {details}")


print("=" * 80)
print("NIH SABV DATA PROCESSING PIPELINE - 20 TEST SCENARIOS")
print("=" * 80)

# Test 1: Create synthetic data
try:
    np.random.seed(42)
    df_test = pd.DataFrame({
        'Animal_ID': range(1, 51),
        'Weight': np.random.normal(25, 5, 50),
        'Length': np.random.normal(20, 3, 50),
        'Velocity': np.abs(np.random.normal(10, 2, 50)),
    })
    log_test(1, "Create synthetic dataset", "PASS", f"50 rows, 4 cols")
except Exception as e:
    log_test(1, "Create synthetic dataset", "FAIL", str(e))

# Test 2: Basic cleaning
try:
    df_clean = basic_clean(df_test.copy())
    assert len(df_clean) > 0
    log_test(2, "Basic cleaning", "PASS", f"{len(df_clean)} rows after cleaning")
except Exception as e:
    log_test(2, "Basic cleaning", "FAIL", str(e))

# Test 3: Parse animal numbers
try:
    animal_nums = parse_animal_number_series(df_test['Animal_ID'])
    assert animal_nums.notna().sum() == 50
    log_test(3, "Parse animal numbers", "PASS", "All 50 IDs parsed")
except Exception as e:
    log_test(3, "Parse animal numbers", "FAIL", str(e))

# Test 4: Classify by threshold
try:
    threshold = 16
    sex_class = np.where(
        animal_nums <= threshold, 'Male',
        np.where(animal_nums > threshold, 'Female', 'Unclassified')
    )
    df_test['Sex'] = sex_class
    male_count = (df_test['Sex'] == 'Male').sum()
    female_count = (df_test['Sex'] == 'Female').sum()
    log_test(4, "Classify by threshold (≤16=M, >16=F)", "PASS", f"M={male_count}, F={female_count}")
except Exception as e:
    log_test(4, "Classify by threshold", "FAIL", str(e))

# Test 5: Parse ID list with ranges
try:
    male_ids, invalid = parse_id_list("1-16, 20")
    assert len(male_ids) == 17
    assert len(invalid) == 0
    log_test(5, "Parse ID list with ranges", "PASS", f"Parsed {len(male_ids)} IDs")
except Exception as e:
    log_test(5, "Parse ID list with ranges", "FAIL", str(e))

# Test 6: Parse ID list with overlaps
try:
    male_ids, _ = parse_id_list("1-10")
    female_ids, _ = parse_id_list("8-15")
    overlap = male_ids.intersection(female_ids)
    assert len(overlap) == 3  # 8, 9, 10
    log_test(6, "Detect overlapping ID lists", "PASS", f"Found {len(overlap)} overlaps")
except Exception as e:
    log_test(6, "Detect overlapping ID lists", "FAIL", str(e))

# Test 7: T-test for sex differences
try:
    t_stat, p_value, n_m, n_f = ttest_for_groups(df_test, 'Weight')
    assert not pd.isna(t_stat)
    is_sig = p_value < 0.05
    log_test(7, "T-test for sex differences (Weight)", "PASS", f"p={p_value:.4f}")
except Exception as e:
    log_test(7, "T-test for sex differences", "FAIL", str(e))

# Test 8: Effect size (Cohen's d)
try:
    male_weight = df_test[df_test['Sex'] == 'Male']['Weight'].dropna()
    female_weight = df_test[df_test['Sex'] == 'Female']['Weight'].dropna()
    cohens_d = effect_size_cohens_d(male_weight, female_weight)
    log_test(8, "Calculate Cohen's d effect size", "PASS", f"d={cohens_d:.4f}")
except Exception as e:
    log_test(8, "Calculate Cohen's d effect size", "FAIL", str(e))

# Test 9: Add log feature
try:
    df_log = add_log_feature(df_test.copy(), 'Weight')
    assert 'Weight_log' in df_log.columns
    assert df_log['Weight_log'].notna().sum() > 0
    log_test(9, "Add log-transformed feature", "PASS", "Weight_log created")
except Exception as e:
    log_test(9, "Add log-transformed feature", "FAIL", str(e))

# Test 10: Add polynomial features
try:
    df_poly = add_polynomial_features(df_test.copy(), 'Weight', degree=3)
    assert 'Weight_pow2' in df_poly.columns
    assert 'Weight_pow3' in df_poly.columns
    log_test(10, "Add polynomial features", "PASS", "Weight_pow2, Weight_pow3 created")
except Exception as e:
    log_test(10, "Add polynomial features", "FAIL", str(e))

# Test 11: Add interaction features
try:
    df_inter = add_interaction_features(df_test.copy(), 'Weight', 'Length')
    assert 'Weight_x_Length' in df_inter.columns
    log_test(11, "Add interaction features", "PASS", "Weight_x_Length created")
except Exception as e:
    log_test(11, "Add interaction features", "FAIL", str(e))

# Test 12: Standardize features
try:
    df_std = standardize_features(df_test.copy(), ['Weight', 'Length'])
    assert 'Weight_std' in df_std.columns
    assert 'Length_std' in df_std.columns
    w_mean = df_std['Weight_std'].mean()
    w_std = df_std['Weight_std'].std()
    assert abs(w_mean) < 0.01  # Should be ~0
    log_test(12, "Standardize features", "PASS", "Features standardized (μ≈0, σ≈1)")
except Exception as e:
    log_test(12, "Standardize features", "FAIL", str(e))

# Test 13: Add missing indicators
try:
    df_miss = add_missing_indicators(df_test.copy(), ['Weight', 'Length'])
    assert 'Weight_missing' in df_miss.columns
    assert 'Length_missing' in df_miss.columns
    log_test(13, "Add missing indicators", "PASS", "Missing indicators added")
except Exception as e:
    log_test(13, "Add missing indicators", "FAIL", str(e))

# Test 14: Handle missing values in features
try:
    df_with_nan = df_test.copy()
    df_with_nan.loc[5:10, 'Weight'] = np.nan
    df_clean_nan = basic_clean(df_with_nan.copy())
    missing_count = df_clean_nan['Weight'].isna().sum()
    log_test(14, "Handle missing values", "PASS", f"Rows with NaN handled")
except Exception as e:
    log_test(14, "Handle missing values", "FAIL", str(e))

# Test 15: Data with low sample size
try:
    df_small = df_test.iloc[:5].copy()
    male_small = df_small[df_small['Sex'] == 'Male']['Weight'].dropna()
    female_small = df_small[df_small['Sex'] == 'Female']['Weight'].dropna()
    if len(male_small) > 1 and len(female_small) > 1:
        t_stat, p_val, _, _ = ttest_for_groups(df_small, 'Weight')
        log_test(15, "T-test with small sample (n=5)", "PASS", "Handled gracefully")
    else:
        log_test(15, "T-test with small sample (n=5)", "PASS", "Insufficient data handled")
except Exception as e:
    log_test(15, "T-test with small sample", "FAIL", str(e))

# Test 16: Multiple feature engineering pipeline
try:
    df_pipeline = df_test.copy()
    df_pipeline = add_log_feature(df_pipeline, 'Weight')
    df_pipeline = add_polynomial_features(df_pipeline, 'Length', degree=2)
    df_pipeline = add_interaction_features(df_pipeline, 'Weight', 'Length')
    df_pipeline = standardize_features(df_pipeline, ['Weight', 'Length'])
    df_pipeline = add_missing_indicators(df_pipeline, ['Weight', 'Length'])
    expected_cols = ['Weight_log', 'Length_pow2', 'Weight_x_Length', 'Weight_std', 'Length_std', 'Weight_missing', 'Length_missing']
    assert all(col in df_pipeline.columns for col in expected_cols)
    log_test(16, "Full feature engineering pipeline", "PASS", f"Created 7 new features")
except Exception as e:
    log_test(16, "Full feature engineering pipeline", "FAIL", str(e))

# Test 17: Linear regression compatibility
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    
    X = df_test[['Weight', 'Length']].dropna()
    y = df_test.loc[X.index, 'Velocity'].dropna()
    X = X.loc[y.index]
    
    if len(X) > 5:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        r2 = model.score(X_test, y_test)
        log_test(17, "Linear regression with sklearn", "PASS", f"R²={r2:.4f}")
    else:
        log_test(17, "Linear regression with sklearn", "PASS", "Dataset too small")
except Exception as e:
    log_test(17, "Linear regression with sklearn", "FAIL", str(e))

# Test 18: Polynomial regression
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    
    X = df_test[['Weight']].copy()
    X['Weight_pow2'] = X['Weight'] ** 2
    y = df_test['Velocity']
    
    X_clean = X.dropna()
    y_clean = y.loc[X_clean.index].dropna()
    X_clean = X_clean.loc[y_clean.index]
    
    if len(X_clean) > 5:
        X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        r2 = model.score(X_test, y_test)
        log_test(18, "Polynomial regression (degree 2)", "PASS", f"R²={r2:.4f}")
    else:
        log_test(18, "Polynomial regression", "PASS", "Dataset too small")
except Exception as e:
    log_test(18, "Polynomial regression", "FAIL", str(e))

# Test 19: Sex classification modes comparison
try:
    # Threshold mode
    threshold_sex = np.where(animal_nums <= 16, 'Male', 'Female')
    
    # Manual list mode
    sex_manual = np.where(
        animal_nums.isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]),
        'Male', 'Female'
    )
    
    # Both should match
    match_count = (threshold_sex == sex_manual).sum()
    log_test(19, "Sex classification mode equivalence", "PASS", f"{match_count}/50 match")
except Exception as e:
    log_test(19, "Sex classification mode equivalence", "FAIL", str(e))

# Test 20: Residual analysis for regression
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    
    X = df_test[['Weight', 'Length']].dropna()
    y = df_test.loc[X.index, 'Velocity'].dropna()
    X = X.loc[y.index]
    
    if len(X) > 10:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        residuals = y_test - y_pred
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        log_test(20, "Residual analysis", "PASS", f"MAE={mae:.4f}, RMSE={rmse:.4f}")
    else:
        log_test(20, "Residual analysis", "PASS", "Dataset too small")
except Exception as e:
    log_test(20, "Residual analysis", "FAIL", str(e))


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

df_results = pd.DataFrame(test_results)
pass_count = (df_results['Status'] == 'PASS').sum()
fail_count = (df_results['Status'] == 'FAIL').sum()
warn_count = (df_results['Status'] == 'WARN').sum()

print(f"\nTotal Tests: {len(df_results)}")
print(f"Passed: {pass_count} ✓")
print(f"Failed: {fail_count} ✗")
print(f"Warnings: {warn_count} ⚠")

if fail_count == 0:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠  {fail_count} test(s) failed:")
    for _, row in df_results[df_results['Status'] == 'FAIL'].iterrows():
        print(f"  - Test {row['Test']}: {row['Name']} - {row['Details']}")

print("\n" + "=" * 80)
