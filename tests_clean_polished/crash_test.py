from models_clean_polished.simulated_trip_evaluator import SimulatedTripEvaluator
import random

if __name__ == "__main__":
    evaluator = SimulatedTripEvaluator()

    for i in range(15):
        danger_score = random.uniform(0.0, 1.0)
        fuel_used = random.uniform(2.0, 10.0)
        total_cost = random.uniform(10.0, 50.0)
        turn_angle = random.uniform(0.0, 90.0)
        min_distance = random.uniform(0.1, 5.0)  # Some will crash (<= 1.0)

        perception = {
            "FOV_Threat_Count": random.randint(0, 10),
            "Min_Distance_In_FOV": min_distance
        }

        print(f"\n🌌 Simulating trip {i+1}: DangerScore={danger_score:.2f}, MinDistance={min_distance:.2f}")
        result = evaluator.evaluate(
            danger_score=danger_score,
            fuel_used=fuel_used,
            total_cost=total_cost,
            turn_angle=turn_angle,
            perception_stats=perception
        )
        print(result)
