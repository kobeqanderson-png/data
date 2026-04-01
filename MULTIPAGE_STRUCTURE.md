# Multi-Page App Structure

## Overview

Your Streamlit application has been reorganized into a modern multi-page structure using Streamlit's `/pages` directory feature. This provides better code organization, improved maintainability, and cleaner separation of concerns.

## Project Structure

```
/workspaces/data/
├── app.py                          # Home page / entry point
├── pages/                          # Multi-page directory
│   ├── 1_Upload_Data.py           # Upload and explore data
│   ├── 2_Process_Data.py          # Data cleaning & classification
│   ├── 3_Sex_Analysis.py          # Statistical analysis
│   ├── 4_Visualizations.py        # General data visualizations
│   ├── 5_Regression.py            # Linear regression modeling
│   └── 6_Download.py              # Export processed data
├── src/                           # Shared utility modules
│   ├── data_load.py              # CSV/Excel loading
│   ├── cleaning.py               # Data cleaning functions
│   ├── features.py               # Feature engineering
│   ├── visualize.py              # Visualization utilities
│   └── branding.py               # Optional branding/watermarking
└── requirements.txt              # Python dependencies
```

## Page Navigation

Each page is independently executable but shares data through Streamlit's `session_state`:

### 1. **Home Page** (`app.py`)
- Landing page with pipeline overview
- Global settings sidebar (threshold, cleaning options, branding)
- Session state indicators

### 2. **Upload Data** (`pages/1_Upload_Data.py`)
- Upload CSV or Excel files
- Preview raw data
- View statistics and column information
- Identify missing values

### 3. **Process Data** (`pages/2_Process_Data.py`)
- Apply data cleaning
- Classify samples by sex (3 methods available)
- Add log-transformed features
- Review processing summary

### 4. **Sex Analysis** (`pages/3_Sex_Analysis.py`)
- Statistical comparisons (Welch's t-test)
- Sex distribution overview
- Box plots, violin plots, distributions
- Effect size analysis (Cohen's d)
- Multi-variable comparisons

### 5. **Visualizations** (`pages/4_Visualizations.py`)
- Histograms and box plots
- Correlation heatmaps
- Density distributions
- Bivariate scatter plots
- Combined mean + individual points

### 6. **Regression** (`pages/5_Regression.py`)
- Configure and train linear models
- Polynomial feature support
- Model performance metrics
- Coefficient analysis
- Residual diagnostics

### 7. **Download** (`pages/6_Download.py`)
- Export as CSV
- Export as Excel (with summary statistics)
- Professional formatting with color-coding

## Running the App

```bash
# Start the app from the project root
streamlit run app.py

# Or with port specification
streamlit run app.py --server.port 8501
```

## Key Features of Multi-Page Structure

✅ **Code Organization** - Each page focuses on a specific task
✅ **Session State** - Data persists across page navigation
✅ **Shared Settings** - Global configuration in sidebar
✅ **Modular Design** - Easy to maintain and extend
✅ **Navigation** - Automatic page menu in top left
✅ **Performance** - Pages load on demand

## Session State Variables

Data is shared across pages using `st.session_state`:

- `df_raw` - Raw uploaded dataframe
- `df_processed` - Processed dataframe after cleaning & classification
- `sex_threshold` - Default animal ID threshold
- `sex_col_used` - Column used for sex classification
- `branding_enabled` - Whether to include watermarks
- `uploaded_filename` - Name of uploaded file

## Adding New Pages

To add new functionality:

1. Create a new file in `/pages/` with numeric prefix (e.g., `7_NewFeature.py`)
2. Use the same imports and session state management
3. Import shared utilities from `src/` modules
4. Streamlit automatically discovers and lists new pages

Example:
```python
# pages/7_NewFeature.py
import streamlit as st
if st.session_state.df_processed is None:
    st.warning("Process data first")
    st.stop()
# ... rest of page logic
```

## Comparison: Old vs New

| Aspect | Old (Monolithic) | New (Multi-Page) |
|--------|-----------------|------------------|
| **File Size** | 1400+ lines | ~250 lines per page |
| **Navigation** | Scroll top-to-bottom | Click page tabs |
| **Organization** | Linear flow | Logical sections |
| **Maintenance** | Difficult | Easy |
| **Reusability** | Limited | High (shared utilities) |

## Migration Notes

- All original functionality is preserved
- Data flow follows the same 7-step pipeline
- Styling and theme remain unchanged
- Helper functions moved to utilities (parsing, stats, etc.)
- Session state replaces in-memory dataframe passing

## Troubleshooting

**Pages not showing up:**
- Ensure files are in `/pages/` directory
- Check filenames start with numbers (e.g., `1_`, `2_`)
- Restart Streamlit

**Data lost between pages:**
- Check `session_state` is initialized in each page
- Don't reassign `df_raw`/`df_processed` - modify copies

**Import errors:**
- Verify paths use `from src.module import function`
- Check `sys.path` includes project root

---

**Version:** 2.0 (Multi-Page)  
**Last Updated:** April 1, 2026
