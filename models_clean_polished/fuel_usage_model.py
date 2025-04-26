"""
Fuel Usage Model (Enhanced)

This model estimates the space car's fuel usage based on its weight, thrust capacity, engine class efficiency,
power capacity, environmental danger score, and turning behavior (moment of inertia).
It incorporates multiple efficiency curves and penalties to reflect realistic energy demands.
"""

from typing import Dict, Any


class FuelUsageModelEnhanced:
    """
    Model for estimating the fuel consumption of a space car under various conditions.

    Attributes:
        base_fuel_rate (float): Base multiplier for fuel usage.
        engine_efficiency (Dict[str, float]): Engine-specific fuel efficiency multipliers.
    """

    def __init__(self) -> None:
        """
        Initialize the FuelUsageModelEnhanced with base rates and engine efficiency parameters.
        """
        self.base_fuel_rate: float = 0.04  # Base multiplier for all calculations

        self.engine_efficiency: Dict[str, float] = {
            "Ion-A": 0.7,
            "Ion-B": 0.75,
            "Fusion-B": 1.0,
            "Fusion-C": 1.1,
            "Plasma-A": 1.3
        }

    def thrust_efficiency_curve(self, thrust: float) -> float:
        """
        Model efficiency penalty based on thrust deviation from the optimal thrust range (60 kN).

        Args:
            thrust (float): Thrust value in kilonewtons.

        Returns:
            float: Thrust efficiency multiplier.
        """
        if thrust <= 0:
            return 2.0  # Severe inefficiency penalty for non-functional thrust
        return 1 + 0.0015 * (thrust - 60) ** 2

    def power_penalty(self, power_capacity: float) -> float:
        """
        Apply a mild penalty when power capacity approaches high values.

        Args:
            power_capacity (float): Power capacity in kilowatt-hours.

        Returns:
            float: Power inefficiency multiplier.
        """
        if power_capacity >= 300:
            return 1.1  # Mild inefficiency penalty
        return 1.0

    def danger_multiplier(self, danger_score: float) -> float:
        """
        Increase fuel usage based on the perceived environmental danger.

        Args:
            danger_score (float): Normalized danger score between 0.0 and 1.0.

        Returns:
            float: Risk multiplier for fuel usage.
        """
        if danger_score > 0.75:
            return 1.5
        elif danger_score > 0.4:
            return 1.2
        return 1.0

    def estimate(self, car_specs: Dict[str, Any], danger_score: float, turn_angle: float = 0.0) -> float:
        """
        Estimate the amount of fuel used based on car specifications and environmental conditions.

        Args:
            car_specs (Dict[str, Any]): Dictionary containing car parameters (weight, thrust, engine, etc.).
            danger_score (float): Computed environmental danger score.
            turn_angle (float, optional): Degree of turn maneuver. Defaults to 0.0.

        Returns:
            float: Estimated fuel usage, rounded to 3 decimals.

        Raises:
            TypeError: If car_specs is not a dictionary.
        """
        if not isinstance(car_specs, dict):
            raise TypeError(f"Expected car_specs to be a dict, got {type(car_specs).__name__}.")

        weight = car_specs.get("space_weight_kg", 2000)
        thrust = car_specs.get("thrust_kN", 60.0)
        power = car_specs.get("power_capacity_kWh", 200)
        engine_class = car_specs.get("engine_class", "Fusion-B")

        thrust_efficiency = self.thrust_efficiency_curve(thrust)
        engine_factor = self.engine_efficiency.get(engine_class, 1.0)
        power_factor = self.power_penalty(power)
        risk_factor = self.danger_multiplier(danger_score)

        # Base fuel consumption estimate
        fuel_usage = (
            self.base_fuel_rate
            * (weight / thrust)
            * thrust_efficiency
            * engine_factor
            * power_factor
            * risk_factor
        )

        # Additional fuel usage for turning based on moment of inertia
        moment_of_inertia = car_specs.get("moment_of_inertia", 1.0)
        if abs(turn_angle) > 0:
            fuel_usage *= 1 + 0.003 * abs(turn_angle) * moment_of_inertia

        return round(fuel_usage, 3)
