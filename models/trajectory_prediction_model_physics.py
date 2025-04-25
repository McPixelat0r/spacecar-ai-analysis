import math

class TrajectoryPredictionModelPhysics:
    def __init__(self, moment_of_inertia=500.0, max_torque=100.0):
        self.moment_of_inertia = moment_of_inertia  # Resistance to turning
        self.max_torque = max_torque                # Maximum turning force

    def predict(self, car_state, perception_stats, delta_time=1.0, verbose=False):
        """
        Predict the new heading based on current car state and perceived threats.

        Parameters:
            car_state (dict): Requires keys 'heading' (float, degrees) and 'angular_velocity' (float, degrees/sec).
            perception_stats (dict): Requires keys 'Threats_Left_Sector', 'Threats_Right_Sector', 'FOV_Front_Cone_Threat_Count'.
            delta_time (float, optional): Time step for the simulation. Default is 1.0 second.
            verbose (bool, optional): If True, returns detailed debug information.

        Returns:
            dict: Prediction results including new heading, updated angular velocity, applied torque, and debug info if verbose.
        """
        required_car_keys = ["heading", "angular_velocity"]
        required_perception_keys = ["Threats_Left_Sector", "Threats_Right_Sector", "FOV_Front_Cone_Threat_Count"]

        for key in required_car_keys:
            if key not in car_state:
                raise KeyError(f"Missing required key in car_state: '{key}'")

        for key in required_perception_keys:
            if key not in perception_stats:
                raise KeyError(f"Missing required key in perception_stats: '{key}'")

        heading = car_state["heading"]
        angular_velocity = car_state["angular_velocity"]

        threats_left = perception_stats["Threats_Left_Sector"]
        threats_right = perception_stats["Threats_Right_Sector"]
        threats_ahead = perception_stats["FOV_Front_Cone_Threat_Count"]

        # Determine torque direction based on threat sectors
        if threats_ahead == 0:
            torque = 0.0
            direction = "none"
        elif threats_right > threats_left:
            torque = self.max_torque
            direction = "left"
        elif threats_left > threats_right:
            torque = -self.max_torque
            direction = "right"
        else:
            torque = self.max_torque if math.copysign(1, angular_velocity) <= 0 else -self.max_torque
            direction = "momentum-based"

        # Compute angular acceleration and update angular velocity
        angular_acceleration = torque / self.moment_of_inertia
        angular_velocity += angular_acceleration * delta_time

        # Update heading based on new angular velocity
        new_heading = (heading + angular_velocity * delta_time) % 360

        # Save updated values back to car state
        car_state["angular_velocity"] = angular_velocity
        car_state["heading"] = new_heading

        result = {
            "CurrentHeading": heading,
            "PredictedHeading": new_heading,
            "AngularVelocity": angular_velocity,
            "AngularAcceleration": angular_acceleration,
            "TorqueApplied": torque,
            "TurnDirection": direction,
            "AdjustedForThreats": threats_ahead > 0
        }

        if verbose:
            result.update({
                "ThreatsLeft": threats_left,
                "ThreatsRight": threats_right,
                "ThreatsAhead": threats_ahead,
                "DeltaTime": delta_time,
                "Reason": (
                    f"Physics-based turn using torque={torque}, I={self.moment_of_inertia}, "
                    f"ω={angular_velocity:.2f}, α={angular_acceleration:.2f}"
                )
            })

        return result
