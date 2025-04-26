"""
Danger Rating Model with Angle Weighting

This model evaluates the perceived danger to the space car based on threat count, distance,
field-of-view (FOV) density, front-cone threats, and the angular density of threats.
It applies zone-based multipliers and angle proximity bonuses to assess the final danger score.
"""

from typing import Dict, Any, Union


class DangerRatingModel:
    """
    Model for calculating a normalized danger score based on environmental perception statistics.

    Attributes:
        weights (Dict[str, float]): Importance weights for different perception features.
        zone_multipliers (Dict[str, float]): Multipliers based on environmental zone risk.
        max_angle_bonus (float): Maximum score boost for threats aligned directly ahead (0° offset).
    """

    def __init__(self) -> None:
        """
        Initialize the DangerRatingModel with default weighting parameters.
        """
        self.weights: Dict[str, float] = {
            "threat_count": 0.35,
            "min_distance": 0.2,
            "fov_density": 0.1,
            "front_cone_threats": 0.2,
            "angle_density": 0.15
        }

        self.zone_multipliers: Dict[str, float] = {
            "green": 1.0,
            "yellow": 1.25,
            "red": 1.5
        }

        self.max_angle_bonus: float = 0.2  # Max bonus for perfect center alignment (0° offset).

    def compute(self, perception_stats: Dict[str, Any]) -> Dict[str, Union[float, str]]:
        """
        Compute a danger score and label based on perception statistics.

        Args:
            perception_stats (Dict[str, Any]): Dictionary containing perception metrics.

        Returns:
            Dict[str, Union[float, str]]: A dictionary with 'DangerScore' and 'DangerLabel'.

        Raises:
            TypeError: If 'perception_stats' is not a dictionary.
        """
        if not isinstance(perception_stats, dict):
            raise TypeError(f"Expected perception_stats to be a dict, got {type(perception_stats).__name__}.")

        threat_count = perception_stats.get("FOV_Threat_Count", 0)
        min_distance = perception_stats.get("Min_Distance_In_FOV", 10.0)
        fov_density = perception_stats.get("FOV_Density", 0.0)
        front_cone_threats = perception_stats.get("FOV_Front_Cone_Threat_Count", 0)
        angle_density = perception_stats.get("Angle_Weighted_Density", 0.0)
        avg_offset = perception_stats.get("Average_Threat_Angle_Offset", 90.0)
        zone = perception_stats.get("Zone", "green").lower()

        # Compute raw weighted score
        score = (
                self.weights["threat_count"] * (threat_count / 10) +
                self.weights["min_distance"] * (1 / max(min_distance, 0.1)) +
                self.weights["fov_density"] * fov_density +
                self.weights["front_cone_threats"] * (front_cone_threats / 10) +
                self.weights["angle_density"] * angle_density
        )

        # Apply zone-based risk multiplier
        score *= self.zone_multipliers.get(zone, 1.0)

        # Apply angle-based threat proximity bonus
        angle_weight_multiplier = 1 + ((90 - min(avg_offset, 90)) / 90) * self.max_angle_bonus
        score *= angle_weight_multiplier

        # Clamp score between 0 and 1
        score = min(max(score, 0.0), 1.0)

        # Assign a danger label
        if score > 0.75:
            label = "High"
        elif score > 0.4:
            label = "Medium"
        else:
            label = "Low"

        return {
            "DangerScore": round(score, 3),
            "DangerLabel": label
        }
