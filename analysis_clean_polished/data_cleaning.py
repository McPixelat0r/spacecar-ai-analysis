"""
Data Cleaning Module

This module handles the preprocessing of raw feature data, including removal of duplicates,
handling missing values, and exporting a cleaned dataset ready for simulations.
"""

import os
import pandas as pd
import numpy as np


def clean_raw_data(input_path: str = "../data/raw_features.csv",
                   output_path: str = "../data/cleaned_features.csv") -> None:
    """
    Clean a raw feature CSV file and save the cleaned version.

    Args:
        input_path (str, optional): Path to the raw CSV file. Defaults to '../data/raw_features.csv'.
        output_path (str, optional): Path to save the cleaned CSV file. Defaults to '../data/cleaned_features.csv'.

    Raises:
        FileNotFoundError: If the input CSV file does not exist.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' not found. Please check the path.")

    df = pd.read_csv(input_path)
    print(f"📥 Loaded raw data: {len(df)} rows")

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Drop rows where crucial columns are missing
    required_cols = ["car_model", "moment_of_inertia", "starting_fuel_kWh"]
    existing_required = [col for col in required_cols if col in df.columns]
    df.dropna(subset=existing_required, inplace=True)
    print(f"🧹 After dropping rows missing {existing_required}: {len(df)} rows")

    # Fill missing numeric values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill missing text/categorical fields with 'Unknown'
    non_numeric_cols = df.select_dtypes(include=["object"]).columns.tolist()
    df[non_numeric_cols] = df[non_numeric_cols].fillna("Unknown")

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")
