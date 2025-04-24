import pandas as pd

from models.danger_rating_model_with_angle_weighting import DangerRatingModel
from models.fuel_usage_model import FuelUsageModelEnhanced
from models.cost_optimization_model_simple import CostOptimizationModelSimple
from models.trajectory_prediction_model_smarter import TrajectoryPredictionModelSmarter
from models.simulated_trip_evaluator import SimulatedTripEvaluator


def run_simulation_from_cleaned_data(filename="cleaned_features.csv", limit=10):
    df = pd.read_csv(filename)
    results = []

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
                "space_weight_kg": row["chassis_weight_kg"] + row["engine_weight_kg"] + row["thruster_weight_kg"] + row[
                    "fuel_weight_kg"],
                "thrust_kN": row["total_thrust_kN"],
                "power_capacity_kWh": row["starting_fuel_kWh"]
            }

            danger = danger_model.compute(perception_stats)
            fuel_used = fuel_model.estimate(car_data, danger["DangerScore"])
            cost = cost_model.optimize(fuel_used)
            trajectory = trajectory_model.predict(
                {"heading": row["heading_deg"]},
                perception_stats,
                previous_heading=row["previous_heading_deg"]
            )

            turn_angle = (trajectory["PredictedHeading"] - trajectory["CurrentHeading"]) % 360

            # print(trajectory)
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

        except Exception as e:
            print(f"⚠️ Error processing row: {e}")

    return results


if __name__ == "__main__":
    results = run_simulation_from_cleaned_data()
    for i, r in enumerate(results, 1):
        print(f"--- Simulation {i} ---")
        for k, v in r.items():
            print(f"{k}: {v}")
        print()
