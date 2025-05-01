# load_crash_model.py
"""
Load the trained HGB crash classification model and apply it to a DataFrame
containing perception and navigation features.
"""

import joblib
import pandas as pd

# Load trained model from models_clean_polished
MODEL_PATH = "../models_clean_polished/hgb_model.pkl"

# Load once globally if this will be reused
hgb_model = joblib.load(MODEL_PATH)
print(f"✅ Loaded model from {MODEL_PATH}")

def predict_crash(df: pd.DataFrame) -> pd.Series:
    """
    Predict crash outcomes using the trained HGB model.

    Args:
        df (pd.DataFrame): DataFrame with the same features used during training.

    Returns:
        pd.Series: Binary predictions (0 = no crash, 1 = crash)
    """
    required_cols = [
        "FOV_Threat_Count",
        "Min_Distance_In_FOV",
        "FOV_Density",
        "FOV_Front_Cone_Threat_Count",
        "Angle_Weighted_Density",
        "Threats_Left_Sector",
        "Threats_Right_Sector",
        "Average_Threat_Angle_Offset",
        "heading_deg",
        "previous_heading_deg",
        "DangerScore"
    ]

    # Check for missing columns
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return pd.Series(hgb_model.predict(df[required_cols]), index=df.index, name="CrashPredicted")
