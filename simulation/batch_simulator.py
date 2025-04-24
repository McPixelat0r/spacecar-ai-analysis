
import random
from faker import Faker
from models.fuel_usage_model import FuelUsageModelEnhanced
from models.cost_optimization_model_simple import CostOptimizationModelSimple
from models.trajectory_prediction_model_smarter import TrajectoryPredictionModelSmarter
from models.simulated_trip_evaluator import SimulatedTripEvaluator
from models.danger_rating_model_with_angle_weighting import DangerRatingModel

class BatchSimulator:
    def __init__(self, n_samples=1000, seed=42):
        self.n_samples = n_samples
        self.results = []

        random.seed(seed)
        self.faker = Faker()
        self.faker.seed_instance(seed)

        self.danger_model = DangerRatingModel()
        self.fuel_model = FuelUsageModelEnhanced()
        self.cost_model = CostOptimizationModelSimple()
        self.trajectory_model = TrajectoryPredictionModelSmarter()
        self.trip_evaluator = SimulatedTripEvaluator()

    def random_car_specs(self):
        return {
            "space_weight_kg": self.faker.pyint(min_value=1400, max_value=2200),
            "thrust_kN": round(random.uniform(40, 80), 1),
            "power_capacity_kWh": round(random.uniform(140, 300), 1),
            "engine_class": self.faker.random_element(elements=["Ion-A", "Fusion-B", "Plasma-A"])
        }

    def random_perception_stats(self):
        return {
            "FOV_Threat_Count": self.faker.pyint(min_value=0, max_value=8),
            "Min_Distance_In_FOV": round(random.uniform(1.0, 10.0), 2),
            "FOV_Density": round(random.uniform(0.1, 1.0), 2),
            "FOV_Front_Cone_Threat_Count": self.faker.pyint(min_value=0, max_value=5),
            "Angle_Weighted_Density": round(random.uniform(0.0, 1.0), 2),
            "Threats_Left_Sector": self.faker.pyint(min_value=0, max_value=5),
            "Threats_Right_Sector": self.faker.pyint(min_value=0, max_value=5),
            "Zone": self.faker.random_element(elements=["green", "yellow", "red"]),
            "Average_Threat_Angle_Offset": round(random.uniform(0.0, 90.0), 1)
        }

    def run_simulation(self):
        for _ in range(self.n_samples):
            car = self.random_car_specs()
            perception = self.random_perception_stats()
            heading = self.faker.pyint(min_value=0, max_value=359)
            previous_heading = heading - self.faker.random_element(elements=[-30, -15, 0, 15, 30])

            danger = self.danger_model.compute(perception)
            fuel_used = self.fuel_model.estimate(car, danger["DangerScore"])
            cost = self.cost_model.optimize(fuel_used)
            trajectory = self.trajectory_model.predict(
                {"heading": heading},
                perception,
                previous_heading=previous_heading,
                verbose=True
            )
            trip = self.trip_evaluator.evaluate(
                danger_score=danger["DangerScore"],
                fuel_used=fuel_used,
                total_cost=cost["total_cost"],
                turn_angle=trajectory["TurnAngle"]
            )

            row = {
                **car,
                **perception,
                **danger,
                "FuelUsed": fuel_used,
                **cost,
                **trajectory,
                **trip
            }

            self.results.append(row)
