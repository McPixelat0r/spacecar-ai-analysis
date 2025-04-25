import random
from faker import Faker
from models.cost_optimization_model_simple import CostOptimizationModelSimple
from models.trajectory_prediction_model_smarter import TrajectoryPredictionModelSmarter
from models.simulated_trip_evaluator import SimulatedTripEvaluator
from models.danger_rating_model_with_angle_weighting import DangerRatingModel

class BatchSimulator:
    def __init__(self, n_samples=1000, seed=42):
        self.n_samples = n_samples
        self.results = []

        import pandas as pd
        self.df = pd.read_csv('./data/cleaned_features.csv').fillna(0)

        random.seed(seed)
        self.faker = Faker()
        self.faker.seed_instance(seed)

        self.danger_model = DangerRatingModel()
        self.fuel_model = FuelUsageModelEnhanced()
        self.cost_model = CostOptimizationModelSimple()
        self.trajectory_model = TrajectoryPredictionModelSmarter()
        self.trip_evaluator = SimulatedTripEvaluator()

    def run_simulation(self):
        for i in range(min(self.n_samples, len(self.df))):
            row = self.df.iloc[i].to_dict()
            car = row
            perception = row

            heading = row.get("heading_deg", 0)
            previous_heading = row.get("previous_heading_deg", heading)

            danger = self.danger_model.compute(perception)
            trajectory = self.trajectory_model.predict(
                {"heading": heading},
                perception,
                previous_heading=previous_heading,
                verbose=True
            )
            fuel_used = self.fuel_model.estimate(car, danger["DangerScore"], turn_angle=trajectory["TurnAngle"])
            cost = self.cost_model.optimize(fuel_used)
            trip = self.trip_evaluator.evaluate(
                danger_score=danger["DangerScore"],
                fuel_used=fuel_used,
                total_cost=cost["total_cost"],
                turn_angle=trajectory["TurnAngle"]
            )

            result = {
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

            self.results.append(result)
