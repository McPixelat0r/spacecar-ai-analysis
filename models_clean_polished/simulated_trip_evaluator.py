"""
Simulated Trip Evaluator

This model evaluates the overall quality of a simulated trip by balancing safety, fuel efficiency,
trip cost, and turn complexity. It outputs a normalized score and qualitative evaluation.
"""

from typing import Optional, Dict


class SimulatedTripEvaluator:
    """
    Model for evaluating the quality of a space car trip based on multiple factors.

    Attributes:
        weights (Dict[str, float]): Importance weights assigned to each trip factor.
        norm (Dict[str, float]): Normalization baselines for fuel, cost, and turn angle.
    """

    def __init__(self) -> None:
        """
        Initialize the SimulatedTripEvaluator with default weights and normalization factors.
        """
        self.weights: Dict[str, float] = {
            "danger": 0.4,
            "fuel": 0.2,
            "cost": 0.2,
            "turn": 0.2
        }
        self.norm: Dict[str, float] = {
            "fuel": 10.0,  # Maximum expected fuel usage for normalization
            "cost": 50.0,  # Maximum expected cost for normalization
            "turn": 90.0  # Maximum reasonable turn angle (degrees)
        }

    def evaluate(
            self,
            danger_score: float,
            fuel_used: float,
            total_cost: float,
            turn_angle: Optional[float] = None,
            perception_stats: Optional[Dict[str, object]] = None
    ) -> Dict[str, object]:
        """
        Compute a trip score based on weighted penalties for different trip aspects,
        with added detection of no-escape zones and crash events.

        Args:
            danger_score (float): Normalized danger score (0 to 1).
            fuel_used (float): Fuel usage in units.
            total_cost (float): Total trip cost.
            turn_angle (Optional[float], optional): Turn angle in degrees. Defaults to 0.
            perception_stats (Optional[Dict[str, object]], optional): Perception information for crash and no-escape detection.

        Returns:
            Dict[str, object]: Trip evaluation results, including crash flags if detected.

        Raises:
            TypeError: If any required argument is not a float or int.
        """
        if not all(isinstance(x, (int, float)) for x in [danger_score, fuel_used, total_cost]):
            raise TypeError("danger_score, fuel_used, and total_cost must be int or float types.")
        if turn_angle is not None and not isinstance(turn_angle, (int, float)):
            raise TypeError("turn_angle must be int, float, or None.")

        # Normalize numerical inputs
        fuel_norm = min(fuel_used / self.norm["fuel"], 1.0)
        cost_norm = min(total_cost / self.norm["cost"], 1.0)
        turn_norm = min((turn_angle or 0.0) / self.norm["turn"], 1.0)

        # Compute weighted penalty
        penalty = (
                self.weights["danger"] * danger_score +
                self.weights["fuel"] * fuel_norm +
                self.weights["cost"] * cost_norm +
                self.weights["turn"] * turn_norm
        )

        # Base trip score
        trip_score = round(1.0 - penalty, 3)

        # Initialize crash and no-escape flags
        no_escape_zone = False
        crash = False
        crash_severity = None

        if perception_stats:
            threat_raw = perception_stats.get("FOV_Threat_Count", 0)
            distance_raw = perception_stats.get("Min_Distance_In_FOV", 99)

            try:
                threat_count = int(threat_raw) if isinstance(threat_raw, (int, float, str)) else 0
                min_distance = float(distance_raw) if isinstance(distance_raw, (int, float, str)) else 99.0

                # Detect no-escape
                if threat_count >= 7 and min_distance <= 2.0:
                    no_escape_zone = True
                    trip_score = round(trip_score * 0.5, 3)

                # Detect crash based on dangerous proximity
                if min_distance <= 1.0:  # Critical threshold
                    crash = True
                    crash_severity = self.determine_crash_severity(danger_score, min_distance)
                    trip_score = 0.0  # Immediate failure if crashed

            except (ValueError, TypeError):
                no_escape_zone = False
                crash = False

        # Determine qualitative evaluation
        if crash:
            evaluation = "Critical Failure"
        elif trip_score >= 0.8:
            evaluation = "Excellent"
        elif trip_score >= 0.6:
            evaluation = "Good"
        elif trip_score >= 0.4:
            evaluation = "Risky"
        else:
            evaluation = "Poor"

        # Comments based on result
        if crash:
            comment = f"Mission failed: {crash_severity} crash detected."
        elif evaluation == "Risky":
            comment = "Moderate danger or cost detected."
        elif evaluation == "Poor":
            comment = "Unsafe or inefficient trip path."
            if no_escape_zone:
                comment = "Mission failed due to no-escape zone."
        elif evaluation == "Good":
            comment = "Safe with minor inefficiencies."
        else:
            comment = "Efficient and low-risk path."

        return {
            "TripScore": trip_score,
            "Evaluation": evaluation,
            "Comments": comment,
            "Crash": crash,
            "CrashSeverity": crash_severity,
            "NoEscapeZone": no_escape_zone
        }

    def determine_crash_severity(self, danger_score: float, min_distance: float) -> str:
        """
        Determine crash severity based on danger score and proximity.

        Args:
            danger_score (float): Environmental danger score.
            min_distance (float): Closest obstacle distance.

        Returns:
            str: Severity classification.
        """
        if danger_score >= 0.8 and min_distance <= 0.5:
            return "Deadly"
        elif danger_score >= 0.7 and min_distance <= 1.0:
            return "Total Loss"
        elif danger_score >= 0.5 and min_distance <= 1.5:
            return "Major Damage"
        elif danger_score >= 0.3 and min_distance <= 2.0:
            return "Medium Damage"
        else:
            return "Minor Damage"
