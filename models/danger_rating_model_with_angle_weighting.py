
class DangerRatingModel:
    def __init__(self):
        self.weights = {
            "threat_count": 0.35,
            "min_distance": 0.2,
            "fov_density": 0.1,
            "front_cone_threats": 0.2,
            "angle_density": 0.15
        }

        self.zone_multipliers = {
            "green": 1.0,
            "yellow": 1.25,
            "red": 1.5
        }

        self.max_angle_bonus = 0.2  # max score boost for threats at 0°

    def compute(self, perception_stats):
        threat_count = perception_stats.get("FOV_Threat_Count", 0)
        min_distance = perception_stats.get("Min_Distance_In_FOV", 10.0)
        fov_density = perception_stats.get("FOV_Density", 0.0)
        front_cone_threats = perception_stats.get("FOV_Front_Cone_Threat_Count", 0)
        angle_density = perception_stats.get("Angle_Weighted_Density", 0.0)
        avg_offset = perception_stats.get("Average_Threat_Angle_Offset", 90.0)
        zone = perception_stats.get("Zone", "green").lower()

        # Compute raw score
        score = (
            self.weights["threat_count"] * (threat_count / 10) +
            self.weights["min_distance"] * (1 / max(min_distance, 0.1)) +
            self.weights["fov_density"] * fov_density +
            self.weights["front_cone_threats"] * (front_cone_threats / 10) +
            self.weights["angle_density"] * angle_density
        )

        # Zone multiplier
        score *= self.zone_multipliers.get(zone, 1.0)

        # Apply angle-based multiplier (closer to center = higher danger)
        angle_weight_multiplier = 1 + ((90 - min(avg_offset, 90)) / 90) * self.max_angle_bonus
        score *= angle_weight_multiplier

        # Clamp to [0, 1]
        score = min(max(score, 0.0), 1.0)

        # Label danger level
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
