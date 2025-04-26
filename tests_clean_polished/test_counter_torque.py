"""
Test: Counter Torque Maneuver

This test checks how the physics-based trajectory model applies torque when threats are biased
toward the left sector, expecting the car to turn right to counterbalance.
"""

from models_clean_polished.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics


def run_test() -> None:
    """
    Run the counter torque maneuver test.
    """
    model = TrajectoryPredictionModelPhysics()
    car_state = {'heading': 180.0, 'angular_velocity': 5.0}

    for i in range(3):
        stats = {
            'Threats_Left_Sector': 3,
            'Threats_Right_Sector': 1,
            'FOV_Front_Cone_Threat_Count': 3
        }

        print(f"\nStep {i + 1} (Counter torque maneuver):")
        print(model.predict(car_state, stats, verbose=True))


if __name__ == "__main__":
    run_test()
