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
            turn_angle: Optional[float] = None
    ) -> Dict[str, object]:
        """
        Compute a trip score based on weighted penalties for different trip aspects.

        Args:
            danger_score (float): Normalized danger score (0 to 1).
            fuel_used (float): Fuel usage in units.
            total_cost (float): Total trip cost.
            turn_angle (Optional[float], optional): Turn angle in degrees, defaults to 0° if not provided.

        Returns:
            Dict[str, object]: Dictionary containing 'TripScore', 'Evaluation', and 'Comments'.

        Raises:
            TypeError: If any required argument is not a float or int.
        """
        if not all(isinstance(x, (int, float)) for x in [danger_score, fuel_used, total_cost]):
            raise TypeError("danger_score, fuel_used, and total_cost must be int or float types.")
        if turn_angle is not None and not isinstance(turn_angle, (int, float)):
            raise TypeError("turn_angle must be int, float, or None.")

        # Normalize the numerical inputs
        fuel_norm = min(fuel_used / self.norm["fuel"], 1.0)
        cost_norm = min(total_cost / self.norm["cost"], 1.0)
        turn_norm = min((turn_angle or 0.0) / self.norm["turn"], 1.0)

        # Compute weighted penalty score
        penalty = (
                self.weights["danger"] * danger_score +
                self.weights["fuel"] * fuel_norm +
                self.weights["cost"] * cost_norm +
                self.weights["turn"] * turn_norm
        )

        trip_score = round(1.0 - penalty, 3)

        # Interpret the trip score qualitatively
        if trip_score >= 0.8:
            evaluation = "Excellent"
            comment = "Efficient and low-risk path."
        elif trip_score >= 0.6:
            evaluation = "Good"
            comment = "Safe with minor inefficiencies."
        elif trip_score >= 0.4:
            evaluation = "Risky"
            comment = "Moderate danger or cost detected."
        else:
            evaluation = "Poor"
            comment = "Unsafe or inefficient trip path."

        return {
            "TripScore": trip_score,
            "Evaluation": evaluation,
            "Comments": comment
        }
