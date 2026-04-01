"""
NIH SABV Compliant Data Processing Pipeline - Home Page

Multi-page app entry point. Navigate to different sections through the sidebar.
Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys

project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.animations import (
    inject_animation_css,
    animated_header,
    animated_metric,
    create_metric_grid,
    animated_progress_steps,
    animated_info_message,
)

st.set_page_config(
    page_title="NIH SABV Compliant Pipeline",
    page_icon=None,
    layout="wide"
)

# Inject animations globally
inject_animation_css()

# Apply custom theme (keep existing styles)
st.markdown(
    """
    <style>
    :root {
        --bg-main: #0d1117;
        --bg-panel: #161b22;
        --bg-soft: #21262d;
        --text-main: #d1d5db;
        --text-muted: #9aa4b2;
        --accent: #22c55e;
        --accent-soft: #15803d;
        --accent-deep: #166534;
        --border: #30363d;
    }

    html, body, [class*="css"] {
        font-family: "IBM Plex Mono", "JetBrains Mono", "Fira Code", monospace !important;
        background: radial-gradient(circle at top right, #1f2937 0%, var(--bg-main) 45%) !important;
        color: var(--text-main) !important;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1f2937 0%, var(--bg-main) 45%) !important;
        color: var(--text-main) !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%) !important;
        border-right: 1px solid var(--border);
    }

    .stMarkdown, .stText, .stCaption, label, p, h1, h2, h3, h4 {
        color: var(--text-main) !important;
    }

    h1, h2, h3 {
        letter-spacing: 0.02em;
        text-shadow: 0 0 0.5px rgba(34, 197, 94, 0.45);
    }

    a {
        color: var(--accent) !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: var(--accent-soft) !important;
        color: #e6fffa !important;
        border: 1px solid var(--accent) !important;
        border-radius: 8px;
        box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.25) inset;
        transition: all 0.3s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--accent) !important;
        color: #0d1117 !important;
        border-color: #86efac !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4) !important;
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus,
    .stButton > button:focus-visible,
    .stDownloadButton > button:focus-visible {
        outline: 2px solid #86efac !important;
        outline-offset: 2px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div,
    .stDateInput > div > div {
        background-color: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-main) !important;
        transition: all 0.3s ease;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stNumberInput > div > div:focus-within,
    .stTextArea > div > div:focus-within,
    .stDateInput > div > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.35) !important;
    }

    div[data-baseweb="slider"] [role="slider"] {
        background-color: var(--accent) !important;
    }

    div[data-baseweb="slider"] > div > div {
        background-color: rgba(34, 197, 94, 0.25) !important;
    }

    .stCheckbox input:checked + div,
    .stRadio input:checked + div {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: #dcfce7 !important;
        border-bottom: 2px solid var(--accent) !important;
    }

    .stDataFrame, [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    .stAlert {
        background: var(--bg-panel) !important;
        border: 1px solid var(--accent-deep) !important;
    }

    hr {
        border-color: var(--border) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for shared data across pages
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None

# Title and description
animated_header("NIH SABV Compliant Pipeline", "Advanced data analysis for sex-based research compliance")

st.markdown("""
### Pipeline Overview

This multi-page application provides a complete workflow for analyzing sex differences in research data.

""")

# Animated progress steps
animated_progress_steps(
    current_step=1,
    total_steps=7,
    steps=[
        "Upload Data",
        "Explore Raw Data",
        "Process & Classify",
        "Analyze Differences",
        "Create Visualizations",
        "Build Models",
        "Download Results"
    ]
)

st.markdown("""
### Key Features

- **Automatic Classification** - Animal ID-based sex classification with flexible modes
- **Data Quality** - Cleaning, missing value handling, duplicate detection
- **Statistical Analysis** - Welch's t-tests, effect sizes, multi-variable comparisons
- **Visualization Suite** - Box plots, violin plots, density distributions, correlations
- **Regression Modeling** - Linear models with polynomial features and diagnostics
- **Publication Ready** - Professional Excel exports with built-in summary statistics

### Quick Start Path

1. Use the sidebar menu to navigate sequentially
2. Each page builds on the previous one
3. Your data persists throughout the session
4. Jump to any page as needed

---
**Built with Streamlit** | Data Processing Pipeline v2.0 | Enhanced with Animations
""")

st.divider()

# Sidebar settings
with st.sidebar:
    st.header("Global Settings")
    
    st.subheader("Sex Classification")
    st.markdown("**Animal # ≤ threshold = Male, > threshold = Female**")
    st.session_state.sex_threshold = st.number_input(
        "Default Threshold (Animal #)", 
        value=16, 
        min_value=1, 
        step=1,
        help="Used as default in processing pages"
    )

    st.divider()

    st.subheader("Sheet Selection (Excel)")
    sheet_option = st.radio(
        "Excel Sheet Selection",
        ["First sheet (index 0)", "Specify sheet name"],
        index=0
    )
    if sheet_option == "Specify sheet name":
        st.session_state.sheet_name = st.text_input("Sheet name", value="Sheet1")
    else:
        st.session_state.sheet_name = 0

    st.divider()

    st.subheader("Cleaning Options")
    st.session_state.fill_missing = st.checkbox("Fill missing numeric values with median", value=True)
    st.session_state.remove_dupes = st.checkbox("Remove duplicate rows", value=True)
    st.session_state.strip_ws = st.checkbox("Strip whitespace from strings", value=True)

    st.divider()

    st.subheader("Feature Engineering")
    st.session_state.add_log = st.checkbox("Add log-transformed features", value=True)

    st.divider()

    st.subheader("Attribution (Optional)")
    st.session_state.branding_enabled = st.checkbox(
        "Include subtle attribution watermark",
        value=False,
        help="Off by default. Turn on for provenance marks in graphs and exports.",
    )

    st.divider()
    
    # Session state info with animation
    if st.session_state.df_raw is not None:
        st.markdown("""
        <div class="metric-card" style="
            padding: 12px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 6px;
            text-align: center;
        ">
            <span style="color: #22c55e; font-weight: 600;">Data Loaded</span><br>
            <span style="color: #9aa4b2; font-size: 12px;">{len(st.session_state.df_raw)} rows ready</span>
        </div>
        """.format(len=len), unsafe_allow_html=True)
    
    if st.session_state.df_processed is not None:
        st.markdown("""
        <div class="metric-card" style="
            padding: 12px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 6px;
            text-align: center;
            margin-top: 8px;
        ">
            <span style="color: #22c55e; font-weight: 600;">Processed</span><br>
            <span style="color: #9aa4b2; font-size: 12px;">{len(st.session_state.df_processed)} rows analyzed</span>
        </div>
        """.format(len=len), unsafe_allow_html=True)

st.divider()
st.caption("Navigate through pages using the sidebar menu • Your data persists across pages")








