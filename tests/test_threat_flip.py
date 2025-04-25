from models.trajectory_prediction_model_physics import TrajectoryPredictionModelPhysics
def run_test():
    model = TrajectoryPredictionModelPhysics()
    car_state = {'heading': 45.0, 'angular_velocity': 0.0}
    threats = [
        {'Threats_Left_Sector': 0, 'Threats_Right_Sector': 4, 'FOV_Front_Cone_Threat_Count': 2},
        {'Threats_Left_Sector': 4, 'Threats_Right_Sector': 0, 'FOV_Front_Cone_Threat_Count': 3}
    ]
    for i, stats in enumerate(threats * 2):
        print(f"\nStep {i+1}:")
        print(model.predict(car_state, stats, verbose=True))
if __name__ == '__main__':
    run_test()
