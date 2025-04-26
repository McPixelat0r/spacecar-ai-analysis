"""
Test: Physics-Based Model Basic Behavior

This test checks how the physics-based trajectory model handles a scenario with threats
primarily on the left, and simulates 5 consecutive time steps.
"""

import pprint
from models_clean_polished.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics


def run_test() -> None:
    """
    Run the basic physics model behavior test.
    """
    model = TrajectoryPredictionModelPhysics(moment_of_inertia=500.0, max_torque=100.0)

    car_state = {
        'heading': 0.0,
        'angular_velocity': 0.0
    }

    perception_stats = {
        'Threats_Left_Sector': 3,
        'Threats_Right_Sector': 1,
        'FOV_Front_Cone_Threat_Count': 5
    }

    print("\n=== Simulating 5 consecutive time steps ===")
    for step in range(5):
        result = model.predict(car_state, perception_stats, delta_time=1.0, verbose=True)
        print(f"\n--- Step {step + 1} ---")
        pprint.pprint(result)


if __name__ == "__main__":
    run_test()
