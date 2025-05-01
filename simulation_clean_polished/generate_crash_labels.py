"""
Generate Crash Labels

This script loads the cleaned feature data and simulates forward movement
to determine whether a crash would occur. The resulting binary label
('CrashOccurred') is saved with each row.
"""

import pandas as pd
from simulated_environment import SimulatedCrashEnvironment
import random

# Load the cleaned dataset
input_path = "../data/cleaned_features.csv"
output_path = "../data/cleaned_features_with_crash.csv"

df = pd.read_csv(input_path).fillna(0)
crash_labels = []

# Generate crash labels row by row
for i, row in df.iterrows():
    env = SimulatedCrashEnvironment(perception_radius=20)

    # You can later map real heading/position if available; for now we randomize
    env.place_car()
    env.generate_obstacles(count=10)

    crash = env.check_for_crash()
    crash_labels.append(crash)

    if i % 100 == 0:
        print(f"Processed {i} rows...")

# Add crash label and save
df["CrashOccurred"] = crash_labels
df.to_csv(output_path, index=False)
print(f"✅ Saved labeled dataset to {output_path}")
