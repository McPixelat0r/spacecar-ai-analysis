"""
Main Simulation Runner

This script coordinates the full simulation pipeline:
1. Generates raw feature data.
2. Cleans the raw data.
3. Runs simulations on the cleaned data.
4. Prints out the simulation results.
"""

from models_clean_polished.trajectory_prediction_model_physics import \
    TrajectoryPredictionModelPhysics  # (Referenced but unused here)
from generation_clean_polished.raw_feature_generator import RawFeatureGenerator
from analysis_clean_polished.data_cleaning import clean_raw_data
from simulation_clean_polished.cleaned_data_simulation_runner import run_simulation_from_cleaned_data


def main() -> None:
    """
    Main function to execute the full simulation pipeline.
    """
    # Step 1: Generate raw data
    print("🚀 Generating raw data...")
    raw_gen = RawFeatureGenerator(seed=42)
    raw_gen.export_to_csv("../data/raw_features.csv", n=1000)

    # Step 2: Clean raw data
    print("🧼 Cleaning raw data...")
    clean_raw_data("../data/raw_features.csv", "../data/cleaned_features.csv")

    # Step 3: Run simulation pipeline
    print("🧪 Running simulations on cleaned data...")
    results = run_simulation_from_cleaned_data("../data/cleaned_features.csv", limit=10)

    # Step 4: Print results
    for i, result in enumerate(results, 1):
        print(f"\n--- Simulation {i} Results ---")
        for key, value in result.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
