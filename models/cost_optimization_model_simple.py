
class CostOptimizationModelSimple:
    def __init__(self):
        self.fuel_unit_cost = 5.0  # per unit of fuel used

    def optimize(self, fuel_used):
        fuel_cost = fuel_used * self.fuel_unit_cost
        total_cost = round(fuel_cost, 2)
        return {
            "fuel_cost": round(fuel_cost, 2),
            "total_cost": total_cost
        }
