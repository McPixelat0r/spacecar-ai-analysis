"""
Cleaned Data Simulation Runner

This module runs simulations based on previously cleaned feature datasets.
It evaluates danger, predicts trajectory, estimates fuel and cost, and scores trips.
"""

import os
import pandas as pd
from typing import List, Dict, Any

from models_clean_polished.danger_rating_model_with_angle_weighting import DangerRatingModel
from models_clean_polished.fuel_usage_model import FuelUsageModelEnhanced
from models_clean_polished.cost_optimization_model_simple import CostOptimizationModelSimple
from models_clean_polished.trajectory_prediction_model_smarter import TrajectoryPredictionModelSmarter
from models_clean_polished.simulated_trip_evaluator import SimulatedTripEvaluator


def run_simulation_from_cleaned_data(filename: str = "cleaned_features.csv", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Run a limited number of simulations from a cleaned dataset.

    Args:
        filename (str, optional): Path to the cleaned CSV file. Defaults to 'cleaned_features.csv'.
        limit (int, optional): Number of rows to process. Defaults to 10.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing simulation results.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' not found. Please ensure it exists.")

    df = pd.read_csv(filename)
    results: List[Dict[str, Any]] = []

    danger_model = DangerRatingModel()
    fuel_model = FuelUsageModelEnhanced()
    cost_model = CostOptimizationModelSimple()
    trajectory_model = TrajectoryPredictionModelSmarter()
    evaluator = SimulatedTripEvaluator()

    for _, row in df.head(limit).iterrows():
        try:
            perception_stats = {
                "FOV_Threat_Count": row["FOV_Threat_Count"],
                "Min_Distance_In_FOV": row["Min_Distance_In_FOV"],
                "FOV_Density": row["FOV_Density"],
                "FOV_Front_Cone_Threat_Count": row["FOV_Front_Cone_Threat_Count"],
                "Angle_Weighted_Density": row["Angle_Weighted_Density"],
                "Threats_Left_Sector": row["Threats_Left_Sector"],
                "Threats_Right_Sector": row["Threats_Right_Sector"],
                "Average_Threat_Angle_Offset": row["Average_Threat_Angle_Offset"]
            }

            car_data = {
                "space_weight_kg": (
                        row["chassis_weight_kg"]
                        + row["engine_weight_kg"]
                        + row["thruster_weight_kg"]
                        + row["fuel_weight_kg"]
                ),
                "thrust_kN": row["total_thrust_kN"],
                "power_capacity_kWh": row["starting_fuel_kWh"]
            }

            danger = danger_model.compute(perception_stats)
            fuel_used = fuel_model.estimate(car_data, danger["DangerScore"])
            cost = cost_model.optimize(fuel_used)
            trajectory = trajectory_model.predict(
                {"heading": row["heading_deg"]},
                perception_stats,
                previous_heading=row.get("previous_heading_deg", row["heading_deg"])
            )

            turn_angle = (trajectory["PredictedHeading"] - trajectory["CurrentHeading"]) % 360

            evaluation = evaluator.evaluate(
                danger_score=danger["DangerScore"],
                fuel_used=fuel_used,
                total_cost=cost["total_cost"],
                turn_angle=turn_angle
            )

            result = {
                **danger,
                "FuelUsed": fuel_used,
                **cost,
                **trajectory,
                **evaluation
            }
            results.append(result)

        except KeyError as e:
            print(f"⚠️ Skipping row due to missing key: {e}")
        except Exception as e:
            print(f"⚠️ Skipping row due to unexpected error: {e}")

    return results


if __name__ == "__main__":
    simulation_results = run_simulation_from_cleaned_data()
    for i, result in enumerate(simulation_results):
        print(f"Result {i + 1}: {result}")
