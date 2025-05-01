# batch_simulator.py
"""
Batch Simulator

This module simulates multiple runs of the space car models using cleaned feature data.
It evaluates danger, predicts trajectory, estimates fuel use and cost, and scores each trip.
"""

import random
import pandas as pd
from faker import Faker
from typing import List, Dict, Any

from models_clean_polished.cost_optimization_model_simple import CostOptimizationModelSimple
from models_clean_polished.trajectory_prediction_model_smarter import TrajectoryPredictionModelSmarter
from models_clean_polished.simulated_trip_evaluator import SimulatedTripEvaluator
from models_clean_polished.danger_rating_model_with_angle_weighting import DangerRatingModel
from models_clean_polished.fuel_usage_model import FuelUsageModelEnhanced
from simulation_clean_polished.load_crash_model import predict_crash

class BatchSimulator:
    """
    Simulator that runs a batch of synthetic trips through the danger, trajectory, fuel, cost, and trip evaluation models.

    Attributes:
        n_samples (int): Number of simulation runs to perform.
        results (List[Dict[str, Any]]): List of simulation results.
    """

    def __init__(self, n_samples: int = 1000, seed: int = 42) -> None:
        """
        Initialize the BatchSimulator.

        Args:
            n_samples (int, optional): Number of samples to simulate. Defaults to 1000.
            seed (int, optional): Random seed for reproducibility. Defaults to 42.

        Raises:
            FileNotFoundError: If 'cleaned_features.csv' cannot be found.
        """
        self.n_samples: int = n_samples
        self.results: List[Dict[str, Any]] = []

        try:
            self.df = pd.read_csv('./data/cleaned_features.csv').fillna(0)
        except FileNotFoundError as e:
            raise FileNotFoundError("Required file './data/cleaned_features.csv' not found.") from e

        random.seed(seed)
        self.faker = Faker()
        self.faker.seed_instance(seed)

        self.danger_model = DangerRatingModel()
        self.fuel_model = FuelUsageModelEnhanced()
        self.cost_model = CostOptimizationModelSimple()
        self.trajectory_model = TrajectoryPredictionModelSmarter()
        self.trip_evaluator = SimulatedTripEvaluator()

    def run_simulation(self) -> None:
        """
        Run the batch simulation across available cleaned feature rows.

        Each iteration simulates a trip through all models and stores the combined result.
        """
        for i in range(min(self.n_samples, len(self.df))):
            row = self.df.iloc[i].to_dict()
            car = row
            perception = row

            heading = row.get("heading_deg", 0.0)
            previous_heading = row.get("previous_heading_deg", heading)

            # Model outputs
            danger = self.danger_model.compute(perception)
            trajectory = self.trajectory_model.predict(
                {"heading": heading},
                perception,
                previous_heading=previous_heading,
                verbose=True
            )
            fuel_used = self.fuel_model.estimate(car, danger["DangerScore"],
                                                 turn_angle=trajectory.get("TurnAngle", 0.0))
            cost = self.cost_model.optimize(fuel_used)
            trip = self.trip_evaluator.evaluate(
                danger_score=danger["DangerScore"],
                fuel_used=fuel_used,
                total_cost=cost["total_cost"],
                turn_angle=trajectory.get("TurnAngle", 0.0)
            )

            enriched_row = {
                **car,
                "car_model": car.get("car_model", "Unknown"),
                "car_type": car.get("car_type", "Unknown"),
                "moment_of_inertia": car.get("moment_of_inertia", 1.0),
                "assigned_by": car.get("assigned_by", "Unknown"),
                "last_telemetry_message": car.get("last_telemetry_message", "N/A"),
                **danger,
                "FuelUsed": fuel_used,
                **cost,
                **trajectory,
                **trip
            }

            # Predict crash using trained HGB model
            crash_pred = predict_crash(pd.DataFrame([enriched_row]))[0]
            crash_prob = predict_crash(pd.DataFrame([enriched_row]), return_proba=True)[0]
            enriched_row["CrashPredicted"] = crash_pred
            enriched_row["CrashProbability"] = round(crash_prob, 3)

            self.results.append(enriched_row)

    def save_results(self, filename: str = "./data/simulation_results.csv") -> None:
        """
        Save simulation results to a CSV file.

        Args:
            filename (str): Output file path. Defaults to './data/simulation_results.csv'.
        """
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"✅ Results saved to {filename}")
