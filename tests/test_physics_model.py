import pprint
from models.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics


def run_test():
    model = TrajectoryPredictionModelPhysics(moment_of_inertia=500.0, max_torque=100.0)

    # Define initial car state
    car_state = {
        'heading': 0.0,
        'angular_velocity': 0.0
    }

    # Define sample threat scenario
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


if __name__ == '__main__':
    run_test()
