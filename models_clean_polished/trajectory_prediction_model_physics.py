"""
Trajectory Prediction Model (Physics-Based)

This model simulates the change in a space car's heading based on torque application,
moment of inertia, and threat sector perception. It predicts angular acceleration,
updated angular velocity, and the resulting new heading.
"""

import math
from typing import Dict, Any


class TrajectoryPredictionModelPhysics:
    """
    Physics-based trajectory prediction model using torque and rotational inertia.

    Attributes:
        moment_of_inertia (float): Resistance to rotational acceleration.
        max_torque (float): Maximum torque the car can apply to adjust its heading.
    """

    def __init__(self, moment_of_inertia: float = 500.0, max_torque: float = 100.0) -> None:
        """
        Initialize the model with the car's rotational properties.

        Args:
            moment_of_inertia (float, optional): Rotational inertia of the car. Defaults to 500.0.
            max_torque (float, optional): Maximum torque output. Defaults to 100.0.
        """
        self.moment_of_inertia = moment_of_inertia
        self.max_torque = max_torque

    def predict(
            self,
            car_state: Dict[str, Any],
            perception_stats: Dict[str, Any],
            delta_time: float = 1.0,
            verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Predict the updated heading and angular velocity of the space car.

        Args:
            car_state (Dict[str, Any]): Must include 'heading' (degrees) and 'angular_velocity' (degrees/sec).
            perception_stats (Dict[str, Any]): Must include 'Threats_Left_Sector', 'Threats_Right_Sector', and 'FOV_Front_Cone_Threat_Count'.
            delta_time (float, optional): Simulation time step. Defaults to 1.0 second.
            verbose (bool, optional): If True, includes detailed calculation steps in the output.

        Returns:
            Dict[str, Any]: Contains 'CurrentHeading', 'PredictedHeading', 'AngularVelocity', 'AppliedTorque', and optionally debug info.

        Raises:
            KeyError: If required keys are missing in car_state or perception_stats.
            TypeError: If inputs are not dictionaries.
        """
        if not isinstance(car_state, dict):
            raise TypeError(f"Expected car_state to be a dict, got {type(car_state).__name__}.")
        if not isinstance(perception_stats, dict):
            raise TypeError(f"Expected perception_stats to be a dict, got {type(perception_stats).__name__}.")

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

        # Step 1: Decide torque direction
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

        # Step 2: Update angular velocity
        angular_acceleration = torque / self.moment_of_inertia
        angular_velocity += angular_acceleration * delta_time

        # Step 3: Update heading
        new_heading = (heading + angular_velocity * delta_time) % 360

        # Step 4: Save back to car_state
        car_state["angular_velocity"] = angular_velocity
        car_state["heading"] = new_heading

        result = {
            "CurrentHeading": heading,
            "PredictedHeading": new_heading,
            "AngularVelocity": angular_velocity,
            "AppliedTorque": torque
        }

        if verbose:
            result["DebugInfo"] = {
                "TorqueDirection": direction,
                "AngularAcceleration": angular_acceleration,
                "DeltaTime": delta_time
            }

        return result
