# Data Analysis (Sex-Specific)

Scaffold for data cleaning and analysis (pandas-based).

If you prefer conda, create a conda environment and run `pip install -r requirements.txt` in that environment.

## Quick Start (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the smoke test
python -m src.quick_test

# Run the Streamlit app
streamlit run app.py
```

## Structure

- run_analysis.ps1 - Quick runner for Windows PowerShell
- requirements.txt
- src/ - Reusable Python modules (data loading, cleaning, features, visualization)
- data/processed/ - Cleaned outputs
- data/raw/ - Place raw input files here (small examples are fine)



