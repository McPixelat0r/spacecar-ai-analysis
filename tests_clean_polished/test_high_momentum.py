"""
Test: High Momentum Behavior

This test checks how the physics-based trajectory model behaves when the car has
significant initial angular velocity and no external threats, focusing on momentum carry-over.
"""

from models_clean_polished.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics


def run_test() -> None:
    """
    Run the high momentum behavior test.
    """
    model = TrajectoryPredictionModelPhysics()
    car_state = {'heading': 270.0, 'angular_velocity': 15.0}

    perception_stats = {
        'Threats_Left_Sector': 0,
        'Threats_Right_Sector': 0,
        'FOV_Front_Cone_Threat_Count': 0
    }

    for i in range(4):
        print(f"\nStep {i + 1} (High momentum behavior):")
        print(model.predict(car_state, perception_stats, verbose=True))


if __name__ == "__main__":
    run_test()
