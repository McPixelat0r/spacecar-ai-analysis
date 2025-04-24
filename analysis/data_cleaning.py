import pandas as pd
import numpy as np


def clean_raw_data(input_path="raw_features.csv", output_path="cleaned_features.csv"):
    # Load raw data
    df = pd.read_csv(input_path)

    # -------------------------------
    # 1. Handle missing or invalid values
    # -------------------------------
    df.replace("", np.nan, inplace=True)

    df['Min_Distance_In_FOV'] = df['Min_Distance_In_FOV'].clip(lower=0.1)
    df['Average_Threat_Angle_Offset'] = df['Average_Threat_Angle_Offset'].clip(0, 180)
    df['starting_fuel_kWh'] = df['starting_fuel_kWh'].fillna(df['starting_fuel_kWh'].median())

    float_columns = df.select_dtypes(include="float").columns
    for col in float_columns:
        df[col] = df[col].fillna(df[col].mean())

    # -------------------------------
    # 2. Standardize text fields
    # -------------------------------
    df['engine_class'] = df['engine_class'].str.strip().str.upper()
    df['car_type'] = df['car_type'].str.strip().str.title()
    df['mission_type'] = df['mission_type'].fillna("Commute")
    df['crew_status'] = "automated"
    df['navigation_mode'] = "auto"

    # -------------------------------
    # 3. Date formatting and ID consistency
    # -------------------------------
    df['test_date'] = pd.to_datetime(df['test_date'], errors='coerce')
    df['ship_serial_number'] = df['ship_serial_number'].str.upper().fillna("UNKNOWN")

    # -------------------------------
    # 4. Save cleaned output
    # -------------------------------
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")
    return df


if __name__ == "__main__":
    clean_raw_data()
