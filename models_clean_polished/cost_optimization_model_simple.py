"""
Cost Optimization Model (Simple Version)

This model calculates the total cost of a simulated trip based on the amount of fuel used.
"""

from typing import Dict


class CostOptimizationModelSimple:
    """
    A simple model for optimizing cost based on fuel usage.

    Attributes:
        fuel_unit_cost (float): Cost per unit of fuel.
    """

    def __init__(self) -> None:
        """
        Initialize the CostOptimizationModelSimple with default fuel cost settings.
        """
        self.fuel_unit_cost: float = 5.0  # Cost per unit of fuel (in credits or currency units).

    def optimize(self, fuel_used: float) -> Dict[str, float]:
        """
        Calculate the cost metrics based on fuel consumption.

        Args:
            fuel_used (float): The amount of fuel used (must be non-negative).

        Returns:
            Dict[str, float]: A dictionary containing 'fuel_cost' and 'total_cost'.
        
        Raises:
            ValueError: If 'fuel_used' is negative.
        """
        if not isinstance(fuel_used, (int, float)):
            raise TypeError(f"Expected fuel_used to be int or float, got {type(fuel_used).__name__}.")
        if fuel_used < 0:
            raise ValueError("Fuel used cannot be negative.")

        fuel_cost = round(fuel_used * self.fuel_unit_cost, 2)
        total_cost = fuel_cost  # In this simple model, total cost equals fuel cost.

        return {
            "fuel_cost": fuel_cost,
            "total_cost": total_cost
        }
