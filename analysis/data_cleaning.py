import pandas as pd
import numpy as np

def clean_raw_data(input_path="../data/raw_features.csv", output_path="../data/cleaned_features.csv"):
    df = pd.read_csv(input_path)
    print(f"📥 Loaded raw data: {len(df)} rows")

    # Remove duplicates if any
    df.drop_duplicates(inplace=True)

    # Drop rows where crucial data is missing, but only if those columns exist
    required_cols = ["car_model", "moment_of_inertia", "starting_fuel_kWh"]
    existing_required = [col for col in required_cols if col in df.columns]
    df = df.dropna(subset=existing_required)
    print(f"🧹 After dropping rows missing {existing_required}: {len(df)} rows")

    # Fill numeric columns with median (if missing)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill non-numeric categorical/text fields with placeholder
    non_numeric_cols = df.select_dtypes(include=["object"]).columns.tolist()
    df[non_numeric_cols] = df[non_numeric_cols].fillna("Unknown")

    # # Just ensure test_date exists and print sample
    # if "test_date" in df.columns:
    #     print("📎 Leaving test_date as string. Sample values:")
    #     print(df['test_date'].dropna().astype(str).head().apply(lambda x: f"[{x}]"))

    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")
