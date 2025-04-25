import math

class TrajectoryPredictionModelPhysics:
    def __init__(self, moment_of_inertia=500.0, max_torque=100.0):
        self.moment_of_inertia = moment_of_inertia  # Resistance to turning
        self.max_torque = max_torque                # Maximum turning force
        self.angular_velocity = 0.0                 # ω, in degrees/sec

    def predict(self, car_state, perception_stats, delta_time=1.0, verbose=False):
        heading = car_state.get("heading", 0.0)
        threats_left = perception_stats.get("Threats_Left_Sector", 0)
        threats_right = perception_stats.get("Threats_Right_Sector", 0)
        threats_ahead = perception_stats.get("FOV_Front_Cone_Threat_Count", 0)

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
            torque = self.max_torque if math.copysign(1, self.angular_velocity) <= 0 else -self.max_torque
            direction = "momentum-based"

        # Compute angular acceleration and update angular velocity
        angular_acceleration = torque / self.moment_of_inertia
        self.angular_velocity += angular_acceleration * delta_time

        # Update heading based on new angular velocity
        new_heading = (heading + self.angular_velocity * delta_time) % 360

        result = {
            "CurrentHeading": heading,
            "PredictedHeading": new_heading,
            "AngularVelocity": self.angular_velocity,
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
                    f"ω={self.angular_velocity:.2f}, α={angular_acceleration:.2f}"
                )
            })

        return result
