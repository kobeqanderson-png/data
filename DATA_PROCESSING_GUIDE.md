# Data Processing Pipeline Guide

This document explains how to use the data processing pipeline for cleaning and preparing raw data files.

---

## Overview

The pipeline automatically:
1. Finds all CSV and Excel files in `data/raw/`
2. Loads each file into a pandas DataFrame
3. Applies basic cleaning (handles missing values, duplicates, whitespace)
4. Adds engineered features (e.g., log transformations)
5. Saves processed data to `data/processed/`

---

## Project Structure

```
competition/
├── main.py                  # Main script - processes all files in data/raw/
├── requirements.txt         # Python dependencies
├── data/
│   ├── raw/                 # Put your raw CSV/Excel files here
│   └── processed/           # Cleaned output files appear here
├── src/
│   ├── data_load.py         # Functions: read_csv(), read_excel()
│   ├── cleaning.py          # Functions: basic_clean(), save_clean()
│   ├── features.py          # Functions: add_log_feature()
│   └── visualize.py         # Functions: boxplot_by_category(), countplot()
└── notebooks/
    └── data_processing_pipeline.ipynb  # Interactive notebook version
```

---

## How to Run

### Step 1: Place Your Data Files

Put any CSV or Excel files you want to process into the `data/raw/` folder.

Supported formats:
- `.csv`
- `.xlsx`
- `.xls`

### Step 2: Run the Pipeline

Open PowerShell and run:

```powershell
cd C:\Users\kobeq\PycharmProjects\competition
.\.venv\Scripts\python.exe main.py
```

### Step 3: Find Your Output

Processed files will be saved to `data/processed/` with the naming pattern:
```
<original_filename>_processed.csv
```

For example:
- Input:  `data/raw/2025 County Health Rankings Data.xlsx`
- Output: `data/processed/2025 County Health Rankings Data_processed.csv`

---

## What the Pipeline Does

### 1. Loading Data

- **CSV files**: Loaded with UTF-8 encoding
- **Excel files**: Loads the first sheet by default (sheet index 0)

To load a specific Excel sheet, modify `main.py`:
```python
df_raw = load_file(input_file, sheet_name="Sheet Name Here")
```

### 2. Basic Cleaning (`basic_clean()`)

The cleaning function performs:
- Strips whitespace from column names
- Parses date columns (if specified)
- Drops rows missing ID columns (if specified)
- Removes duplicate rows
- Fills missing numeric values with the median
- Cleans string columns (strips whitespace, handles 'nan' strings)

### 3. Feature Engineering (`add_log_feature()`)

- Adds a log-transformed version of the first numeric column
- New column is named `<original_column>_log`
- Uses `log1p` (log(1 + x)) to handle zeros safely

### 4. Saving Output (`save_clean()`)

- Saves to CSV format by default
- Can also save to Parquet format for faster loading of large files

---

## Module Reference

### src/data_load.py

| Function | Description |
|----------|-------------|
| `read_csv(path)` | Load a CSV file into a DataFrame |
| `read_excel(path, sheet_name=0)` | Load an Excel file (first sheet by default) |

### src/cleaning.py

| Function | Description |
|----------|-------------|
| `basic_clean(df, date_cols=None, id_cols=None)` | Apply standard cleaning to a DataFrame |
| `save_clean(df, path_csv=None, path_parquet=None)` | Save DataFrame to CSV and/or Parquet |

### src/features.py

| Function | Description |
|----------|-------------|
| `add_log_feature(df, col, new_col=None)` | Add log-transformed column |
| `add_missing_indicators(df, cols)` | Add boolean columns indicating missing values |

### src/visualize.py

| Function | Description |
|----------|-------------|
| `boxplot_by_category(df, cat_col, value_col, out_path=None)` | Create a boxplot grouped by category |
| `countplot(df, col, out_path=None)` | Create a frequency bar chart |

---

## Examples

### Process All Files (Default)

```powershell
.\.venv\Scripts\python.exe main.py
```

### Load a Specific Excel Sheet

Edit `main.py` and change:
```python
process_file(file_path, DATA_PROCESSED, sheet_name=0)
```
To:
```python
process_file(file_path, DATA_PROCESSED, sheet_name="Your Sheet Name")
```

### Use in Python Script

```python
from pathlib import Path
from src.data_load import read_csv, read_excel
from src.cleaning import basic_clean, save_clean
from src.features import add_log_feature

# Load data
df = read_excel("data/raw/myfile.xlsx", sheet_name=0)

# Clean
df = basic_clean(df)

# Add features
df = add_log_feature(df, col="some_numeric_column")

# Save
save_clean(df, path_csv="data/processed/myfile_processed.csv")
```

### Use in Jupyter Notebook

```python
import sys
from pathlib import Path

# Add project root to path
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

from src.data_load import read_excel
from src.cleaning import basic_clean

# Load and clean
df = read_excel("../data/raw/myfile.xlsx")
df = basic_clean(df)
df.head()
```

---

## Troubleshooting

### "pip is not recognized"

Use the venv's Python directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### "running scripts is disabled on this system"

PowerShell execution policy is blocking scripts. Either:

1. Run Python directly (no activation needed):
   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```

2. Or change the policy:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### "No module named 'src'"

Make sure you're running from the project root directory:
```powershell
cd C:\Users\kobeq\PycharmProjects\competition
.\.venv\Scripts\python.exe main.py
```

### "'dict' object has no attribute 'head'"

This happens when an Excel file has multiple sheets and `sheet_name=None` is used.
The fix (already applied) is to use `sheet_name=0` to load the first sheet.

### Excel file loads metadata instead of data

Some Excel files (like County Health Rankings) have multiple sheets where the first
sheet contains documentation. Specify the correct sheet:

```python
df = read_excel("file.xlsx", sheet_name="Select Measure Data")
```

---

## Dependencies

Listed in `requirements.txt`:

- pandas >= 2.0
- numpy
- seaborn
- matplotlib
- scikit-learn
- jupyterlab
- openpyxl (for Excel support)
- pyarrow (for Parquet support)
- scipy

Install with:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Run pipeline | `.\.venv\Scripts\python.exe main.py` |
| Run web app | `.\.venv\Scripts\streamlit.exe run app.py` |
| Install dependencies | `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| Start Jupyter Lab | `.\.venv\Scripts\jupyter-lab.exe` |
| Check installed packages | `.\.venv\Scripts\python.exe -m pip list` |

---

## Web App (Interactive Mode)

The project includes an interactive web app built with Streamlit.

### Features

- Upload CSV or Excel files via drag-and-drop
- Select which sheet to load from Excel files
- Preview raw data with statistics and missing value analysis
- One-click data processing
- Interactive visualizations (histograms, box plots, correlation heatmap)
- Download processed data as CSV or Excel

### Running the Web App

```powershell
cd C:\Users\kobeq\PycharmProjects\competition
.\.venv\Scripts\streamlit.exe run app.py
```

This will:
1. Start a local web server
2. Open your browser to `http://localhost:8501`
3. Display the interactive data processing interface

### Using the Web App

1. **Upload**: Drag and drop your CSV or Excel file
2. **Select Sheet**: For Excel files, choose which sheet to load
3. **Explore**: View data preview, statistics, and missing values
4. **Process**: Click "Run Processing Pipeline" to clean the data
5. **Visualize**: Explore charts and graphs of your data
6. **Download**: Save the processed data as CSV or Excel

