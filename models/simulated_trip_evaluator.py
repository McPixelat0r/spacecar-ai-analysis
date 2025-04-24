
class SimulatedTripEvaluator:
    def __init__(self):
        self.weights = {
            "danger": 0.4,
            "fuel": 0.2,
            "cost": 0.2,
            "turn": 0.2
        }
        self.norm = {
            "fuel": 10.0,
            "cost": 50.0,
            "turn": 90.0
        }

    def evaluate(self, danger_score, fuel_used, total_cost, turn_angle=None):
        # Normalize inputs
        fuel_norm = min(fuel_used / self.norm["fuel"], 1.0)
        cost_norm = min(total_cost / self.norm["cost"], 1.0)
        turn_norm = min((turn_angle or 0) / self.norm["turn"], 1.0)

        # Weighted penalty score
        penalty = (
            self.weights["danger"] * danger_score +
            self.weights["fuel"] * fuel_norm +
            self.weights["cost"] * cost_norm +
            self.weights["turn"] * turn_norm
        )

        trip_score = round(1.0 - penalty, 3)

        # Interpret score
        if trip_score >= 0.8:
            evaluation = "Excellent"
            comment = "Efficient and low-risk path"
        elif trip_score >= 0.6:
            evaluation = "Good"
            comment = "Safe with minor inefficiencies"
        elif trip_score >= 0.4:
            evaluation = "Risky"
            comment = "Moderate danger or cost detected"
        else:
            evaluation = "Poor"
            comment = "Unsafe or inefficient trip path"

        return {
            "TripScore": trip_score,
            "Evaluation": evaluation,
            "Comments": comment
        }
