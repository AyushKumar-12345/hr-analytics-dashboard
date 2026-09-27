#!/usr/bin/env python3
"""
HR Workforce Analytics - Data ETL & Feature Engineering Pipeline
================================================================
Processes the IBM HR Employee Attrition dataset into a clean,
analytics-ready model:
  - Eliminates redundant single-value & noise metrics
  - Creates vectorized demographic and compensation cohorts
  - Generates binary attrition metrics for DAX & BI engines
  - Outputs: HR_Data_cleaned.csv
"""

import sys
import time
import logging
from pathlib import Path
import pandas as pd
import numpy as np

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("HRETL")


def load_raw_dataset(base_dir: Path) -> pd.DataFrame:
    """Load the raw HR attrition dataset safely from the local directory."""
    candidate_filenames = [
        "WA_Fn-UseC_-HR-Employee-Attrition.csv",
        "HR_Employee_Attrition.csv",
        "hr_data.csv"
    ]
    
    source_file = None
    for name in candidate_filenames:
        target = base_dir / name
        if target.exists():
            source_file = target
            break

    if not source_file:
        logger.error("Raw HR dataset not found in directory: %s", base_dir.resolve())
        logger.info("Checked filenames: %s", ", ".join(candidate_filenames))
        sys.exit(1)

    logger.info("Ingesting raw dataset: %s", source_file.name)
    df = pd.read_csv(source_file)
    logger.info("Dataset loaded successfully. Initial records: %d | Features: %d", df.shape[0], df.shape[1])
    return df


def drop_uninformative_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove constant, redundant, and identifier columns with zero analytical variance."""
    df = df.copy()
    columns_to_drop = [
        "EmployeeCount",   # Zero variance (Always 1)
        "Over18",          # Zero variance (Always 'Y')
        "StandardHours",   # Zero variance (Always 80)
        "EmployeeNumber",  # Arbitrary surrogate key
        "DailyRate",       # Redundant compensation metric
        "HourlyRate",      # Redundant compensation metric
        "MonthlyRate"      # Redundant compensation metric
    ]
    
    present_cols = [c for c in columns_to_drop if c in df.columns]
    df.drop(columns=present_cols, inplace=True)
    logger.info("Removed %d non-informative / redundant columns.", len(present_cols))
    return df


def engineer_hr_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer demographic brackets, salary bands, and numerical attrition flags."""
    df = df.copy()

    # 1. Binary Attrition Flag (Essential for DAX & Plotly mean rate calculations)
    if "Attrition" in df.columns:
        df["Attrition_Num"] = (df["Attrition"].str.strip().str.lower() == "yes").astype(int)
        logger.info("Created binary flag 'Attrition_Num' (1 = Yes, 0 = No).")

    # 2. Vectorized Age Brackets
    age_bins = [0, 20, 30, 40, 50, 120]
    age_labels = ["18-20", "21-30", "31-40", "41-50", "51-60+"]
    df["Age Bracket"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=True)
    logger.info("Engineered categorical 'Age Bracket' distribution.")

    # 3. Vectorized Salary Bands
    salary_bins = [0, 5000, 10000, np.inf]
    salary_labels = ["Low", "Medium", "High"]
    df["Salary Band"] = pd.cut(df["MonthlyIncome"], bins=salary_bins, labels=salary_labels, right=True)
    logger.info("Engineered categorical 'Salary Band' distribution.")

    # 4. Clean and normalize string categorical values
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    return df


def export_cleaned_data(df: pd.DataFrame, output_path: Path) -> Path:
    """Export the fully modeled dataset to CSV."""
    df.to_csv(output_path, index=False, encoding="utf-8")
    logger.info("Cleaned dataset successfully exported: '%s' (%d rows, %d columns)", 
                output_path.name, df.shape[0], df.shape[1])
    return output_path


def main():
    start_time = time.time()
    base_dir = Path(__file__).resolve().parent

    logger.info("=" * 60)
    logger.info("STARTING HR ANALYTICS DATA PIPELINE")
    logger.info("=" * 60)

    # Pipeline execution flow
    df_raw = load_raw_dataset(base_dir)
    df_pruned = drop_uninformative_columns(df_raw)
    df_transformed = engineer_hr_features(df_pruned)
    
    output_csv = base_dir / "HR_Data_cleaned.csv"
    export_cleaned_data(df_transformed, output_csv)

    elapsed_time = time.time() - start_time
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY IN %.2f SECONDS", elapsed_time)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
