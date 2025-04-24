
import random

class TrajectoryPredictionModelSmarter:
    def __init__(self, base_turn=20, turn_amplifier=40, max_turn_angle=90):
        self.base_turn = base_turn
        self.turn_amplifier = turn_amplifier
        self.max_turn_angle = max_turn_angle

    def predict(self, car_state, perception_stats, previous_heading=None, verbose=False):
        heading = car_state.get("heading", 0)
        threats_ahead = perception_stats.get("FOV_Front_Cone_Threat_Count", 0)
        angle_density = perception_stats.get("Angle_Weighted_Density", 0.0)
        threats_left = perception_stats.get("Threats_Left_Sector", 0)
        threats_right = perception_stats.get("Threats_Right_Sector", 0)

        # Determine momentum direction
        momentum_bias = None
        if previous_heading is not None:
            delta_heading = (heading - previous_heading) % 360
            if delta_heading > 180:
                delta_heading -= 360
            if delta_heading > 10:
                momentum_bias = "right"
            elif delta_heading < -10:
                momentum_bias = "left"

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

        # Compute turn angle with clamping
        delta = round(self.base_turn + (angle_density * self.turn_amplifier))
        delta = min(delta, self.max_turn_angle)

        # Choose turn direction using threat analysis and momentum fallback
        if threats_right > threats_left:
            direction = "left"
        elif threats_left > threats_right:
            direction = "right"
        elif momentum_bias is not None:
            direction = momentum_bias
        else:
            direction = random.choice(["left", "right"])

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
