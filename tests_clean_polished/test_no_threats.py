"""
Test: No Threats Scenario

This test checks how the physics-based trajectory model behaves when no threats are detected
in any sector, ensuring minimal or no adjustment to the trajectory.
"""

from models_clean_polished.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics


def run_test() -> None:
    """
    Run the no threats scenario test.
    """
    model = TrajectoryPredictionModelPhysics()
    car_state = {'heading': 90.0, 'angular_velocity': 2.0}

    perception_stats = {
        'Threats_Left_Sector': 0,
        'Threats_Right_Sector': 0,
        'FOV_Front_Cone_Threat_Count': 0
    }

    for i in range(3):
        print(f"\nStep {i + 1} (No threats scenario):")
        print(model.predict(car_state, perception_stats, verbose=True))


if __name__ == "__main__":
    run_test()
