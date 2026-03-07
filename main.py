from pathlib import Path
import pandas as pd

from src.data_load import read_excel, read_csv
from src.cleaning import basic_clean, save_clean
from src.features import add_log_feature


DATA_RAW = Path("data/raw")
DATA_PROCESSED = Path("data/processed")


def load_file(file_path: Path, sheet_name=0) -> pd.DataFrame:
    """Load a CSV or Excel file into a DataFrame.

    Args:
        file_path: Path to the file
        sheet_name: For Excel files, which sheet to load (default: first sheet)

    Returns:
        DataFrame with the file contents
    """
    suffix = file_path.suffix.lower()

    if suffix == '.csv':
        return read_csv(str(file_path))
    elif suffix in ['.xlsx', '.xls']:
        return read_excel(str(file_path), sheet_name=sheet_name)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use .csv, .xlsx, or .xls")


def process_file(input_path: Path, output_dir: Path, sheet_name=0) -> None:
    """Process a single data file: load, clean, add features, and save.

    Args:
        input_path: Path to the input file
        output_dir: Directory to save processed output
        sheet_name: For Excel files, which sheet to load
    """
    print(f"\n{'='*60}")
    print(f"Processing: {input_path.name}")
    print('='*60)

    # 1. Load the file
    df_raw = load_file(input_path, sheet_name=sheet_name)

    # 2. Inspect the data
    print("\n=== RAW DATA: HEAD ===")
    print(df_raw.head())
    print("\n=== RAW DATA: INFO ===")
    print(df_raw.info())
    print("\n=== RAW DATA: DESCRIBE (first 5 numeric cols) ===")
    num_cols = df_raw.select_dtypes(include=["number"]).columns[:5]
    if len(num_cols) > 0:
        print(df_raw[num_cols].describe())
    else:
        print("No numeric columns detected yet.")

    # 3. Run basic cleaning
    df_clean = basic_clean(df_raw)

    # 4. Add a log feature on the first numeric column, if available
    df_feat = df_clean
    if len(num_cols) > 0:
        first_num_col = num_cols[0]
        print(f"\nAdding log feature for numeric column: {first_num_col}")
        df_feat = add_log_feature(df_clean, col=first_num_col)

    # 5. Save cleaned data
    output_dir.mkdir(parents=True, exist_ok=True)
    output_name = input_path.stem + "_processed.csv"
    output_path = output_dir / output_name
    save_clean(df_feat, path_csv=str(output_path))

    # 6. Final summary
    print("\n=== CLEANED DATA SHAPE (rows, cols) ===")
    print(df_feat.shape)
    print("\n=== CLEANED DATA COLUMNS ===")
    print(df_feat.columns.tolist())
    print(f"\nSaved cleaned data to: {output_path}")


def main() -> None:
    """Process all Excel and CSV files in data/raw.

    Steps for each file:
    1) Load the file (CSV or Excel)
    2) Inspect structure and a few rows
    3) Run basic cleaning
    4) Add one demo log feature if a suitable numeric column exists
    5) Save cleaned data to data/processed
    """
    # Find all CSV and Excel files in data/raw
    csv_files = list(DATA_RAW.glob("*.csv"))
    excel_files = list(DATA_RAW.glob("*.xlsx")) + list(DATA_RAW.glob("*.xls"))
    all_files = csv_files + excel_files

    if not all_files:
        print(f"No CSV or Excel files found in {DATA_RAW}")
        print("Place your data files (.csv, .xlsx, .xls) in data/raw/ and run again.")
        return

    print(f"Found {len(all_files)} data file(s) to process:")
    for f in all_files:
        print(f"  - {f.name}")

    # Process each file
    for file_path in all_files:
        try:
            # For Excel files, try to load the first sheet by default
            # You can modify this to prompt for sheet selection or use a config
            process_file(file_path, DATA_PROCESSED, sheet_name=0)
        except Exception as e:
            print(f"\nError processing {file_path.name}: {e}")
            print("Skipping this file and continuing...")

    print(f"\n{'='*60}")
    print("All processing complete!")
    print(f"Output files saved to: {DATA_PROCESSED}")
    print('='*60)


if __name__ == "__main__":
    main()
