"""
Trajectory Prediction Model (Smarter Version)

This model predicts how the space car should adjust its heading based on threats detected ahead,
weighted angle densities, and prior momentum trends. It chooses a turn direction intelligently
and adapts the turn magnitude based on perceived density.
"""

import random
from typing import Dict, Any, Optional


class TrajectoryPredictionModelSmarter:
    """
    Smarter trajectory prediction model that adapts to threat distributions and momentum.

    Attributes:
        base_turn (float): Minimum base turn angle applied when threats are detected.
        turn_amplifier (float): Scaling factor for adjusting turn magnitude based on density.
        max_turn_angle (float): Maximum allowed turn angle to prevent oversteering.
    """

    def __init__(self, base_turn: float = 20.0, turn_amplifier: float = 40.0, max_turn_angle: float = 90.0) -> None:
        """
        Initialize the model with base, amplified, and maximum turning constraints.

        Args:
            base_turn (float, optional): Base turn angle. Defaults to 20.
            turn_amplifier (float, optional): Amplification factor for density. Defaults to 40.
            max_turn_angle (float, optional): Maximum cap for turn angle. Defaults to 90.
        """
        self.base_turn = base_turn
        self.turn_amplifier = turn_amplifier
        self.max_turn_angle = max_turn_angle

    def predict(
            self,
            car_state: Dict[str, Any],
            perception_stats: Dict[str, Any],
            previous_heading: Optional[float] = None,
            verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Predict the next heading adjustment based on perception and car momentum.

        Args:
            car_state (Dict[str, Any]): Must contain 'heading' (degrees).
            perception_stats (Dict[str, Any]): Must contain 'FOV_Front_Cone_Threat_Count', 'Angle_Weighted_Density',
                                               'Threats_Left_Sector', and 'Threats_Right_Sector'.
            previous_heading (Optional[float], optional): Heading from the previous timestep, used for momentum bias.
            verbose (bool, optional): If True, includes detailed reasoning.

        Returns:
            Dict[str, Any]: Contains 'CurrentHeading', 'PredictedHeading', 'TurnDirection', 'AdjustedForThreats',
                            and optionally verbose debug info.

        Raises:
            TypeError: If inputs are not dictionaries.
            KeyError: If required keys are missing.
        """
        if not isinstance(car_state, dict):
            raise TypeError(f"Expected car_state to be a dict, got {type(car_state).__name__}.")
        if not isinstance(perception_stats, dict):
            raise TypeError(f"Expected perception_stats to be a dict, got {type(perception_stats).__name__}.")

        heading = car_state.get("heading", 0.0)
        threats_ahead = perception_stats.get("FOV_Front_Cone_Threat_Count", 0)
        angle_density = perception_stats.get("Angle_Weighted_Density", 0.0)
        threats_left = perception_stats.get("Threats_Left_Sector", 0)
        threats_right = perception_stats.get("Threats_Right_Sector", 0)

        # Step 1: Analyze momentum
        momentum_bias = None
        if previous_heading is not None:
            delta_heading = (heading - previous_heading) % 360
            if delta_heading > 180:
                delta_heading -= 360
            if delta_heading > 10:
                momentum_bias = "right"
            elif delta_heading < -10:
                momentum_bias = "left"

        # Step 2: Check if threats are present
        if threats_ahead == 0:
            result = {
                "CurrentHeading": heading,
                "PredictedHeading": heading,
                "TurnDirection": "none",
                "AdjustedForThreats": False
            }
            if verbose:
                result.update({
                    "AngleDensity": angle_density,
                    "TurnAngle": 0,
                    "MomentumBias": momentum_bias,
                    "ThreatsLeft": threats_left,
                    "ThreatsRight": threats_right,
                    "Reason": "No threats detected"
                })
            return result

        # Step 3: Compute desired turn angle based on density
        delta = round(self.base_turn + (angle_density * self.turn_amplifier))
        delta = min(delta, self.max_turn_angle)

        # Step 4: Determine turn direction
        if threats_right > threats_left:
            direction = "left"
        elif threats_left > threats_right:
            direction = "right"
        elif momentum_bias is not None:
            direction = momentum_bias
        else:
            direction = random.choice(["left", "right"])

        # Step 5: Apply heading change
        new_heading = (heading - delta) % 360 if direction == "left" else (heading + delta) % 360

        result = {
            "CurrentHeading": heading,
            "PredictedHeading": new_heading,
            "TurnDirection": direction,
            "AdjustedForThreats": True
        }

        if verbose:
            result.update({
                "AngleDensity": angle_density,
                "TurnAngle": delta,
                "MomentumBias": momentum_bias,
                "ThreatsLeft": threats_left,
                "ThreatsRight": threats_right,
                "Reason": (
                    f"Threats ahead — adjusted based on density, sector bias, "
                    f"and momentum (bias={momentum_bias})"
                )
            })

        return result
