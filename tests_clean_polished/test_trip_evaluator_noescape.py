from models_clean_polished.simulated_trip_evaluator import SimulatedTripEvaluator

if __name__ == "__main__":
    evaluator = SimulatedTripEvaluator()

    fake_danger_score = 0.5
    fake_fuel_used = 5.0
    fake_total_cost = 25.0
    fake_turn_angle = 30.0
    fake_perception = {
        "FOV_Threat_Count": 8,
        "Min_Distance_In_FOV": 1.5
    }

    result = evaluator.evaluate(
        danger_score=fake_danger_score,
        fuel_used=fake_fuel_used,
        total_cost=fake_total_cost,
        turn_angle=fake_turn_angle,
        perception_stats=fake_perception
    )

    print(result)
