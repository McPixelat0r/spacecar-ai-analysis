import math


class FuelUsageModelEnhanced:
    def __init__(self):
        self.base_fuel_rate = 0.04  # base multiplier

        # Engine-specific fuel efficiency multipliers (lower = more efficient)
        self.engine_efficiency = {
            "Ion-A": 0.7,
            "Ion-B": 0.75,
            "Fusion-B": 1.0,
            "Fusion-C": 1.1,
            "Plasma-A": 1.3
        }

    def thrust_efficiency_curve(self, thrust):
        """
        Models efficiency drop-off for very low or high thrust.
        Optimal efficiency is centered around 50–70 kN.
        """
        if thrust <= 0:
            return 2.0  # severe penalty
        return 1 + 0.0015 * (thrust - 60) ** 2

    def power_penalty(self, power_capacity):
        """
        Adds a penalty when power capacity is nearing maximum load.
        This could be dynamic if actual power draw is modeled.
        """
        if power_capacity >= 300:
            return 1.1  # mild inefficiency penalty
        return 1.0

    def danger_multiplier(self, danger_score):
        if danger_score > 0.75:
            return 1.5
        elif danger_score > 0.4:
            return 1.2
        return 1.0

    def estimate(self, car_specs, danger_score):
        weight = car_specs.get("space_weight_kg", 2000)
        thrust = car_specs.get("thrust_kN", 60.0)
        power = car_specs.get("power_capacity_kWh", 200)
        engine_class = car_specs.get("engine_class", "Fusion-B")

        thrust_efficiency = self.thrust_efficiency_curve(thrust)
        engine_factor = self.engine_efficiency.get(engine_class, 1.0)
        power_factor = self.power_penalty(power)
        risk_factor = self.danger_multiplier(danger_score)

        fuel_usage = (
                self.base_fuel_rate
                * (weight / thrust)
                * thrust_efficiency
                * engine_factor
                * power_factor
                * risk_factor
        )

        return round(fuel_usage, 3)
