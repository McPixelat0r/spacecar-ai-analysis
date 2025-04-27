"""
Raw Feature Generator (Full Version)

This module generates synthetic raw feature data for space cars, including physical properties,
perception statistics, navigation metadata, and cosmetic attributes for testing and simulation.
"""

import random
import pandas as pd
from faker import Faker
from datetime import date
from typing import List, Dict, Any


def add_sensor_noise(value: float, noise_percent: float = 0.03) -> float:
    """
    Adds small random noise to a numerical sensor reading.

    Args:
        value (float): Original sensor value.
        noise_percent (float): Maximum noise deviation as a fraction (default 3%).

    Returns:
        float: Noisy sensor value.
    """
    noise = random.uniform(-noise_percent, noise_percent) * value
    return round(value + noise, 3)


class RawFeatureGenerator:
    """
    A generator for creating complete randomized feature data entries for simulation purposes.

    Attributes:
        faker (Faker): Faker instance for generating random names and elements.
        car_models (Dict[str, Dict[str, Any]]): Car models mapped to type and chassis weight.
        engine_weight_range (Dict[str, tuple]): Engine weight ranges by car type.
        thruster_weight_range (Dict[str, tuple]): Thruster weight ranges by car type.
        fuel_types (Dict[str, Dict[str, float]]): Fuel types mapped to energy and mass density.
    """

    def __init__(self, seed: int = 42) -> None:
        """
        Initialize the RawFeatureGenerator with a fixed random seed.

        Args:
            seed (int, optional): Random seed for reproducibility. Defaults to 42.
        """
        self.faker = Faker()
        self.faker.seed_instance(seed)
        random.seed(seed)

        self.car_models = {
            "Stratos M2": {"car_type": "Sedan", "chassis_weight_kg": 950},
            "Vortex R7": {"car_type": "SUV", "chassis_weight_kg": 1250},
            "Nimbus X1": {"car_type": "Micro", "chassis_weight_kg": 700}
        }

        self.engine_weight_range = {
            "Sedan": (180, 260),
            "SUV": (250, 340),
            "Micro": (120, 180)
        }

        self.thruster_weight_range = {
            "Sedan": (100, 150),
            "SUV": (140, 200),
            "Micro": (80, 120)
        }

        self.fuel_types = {
            "IonGel": {"energy_density_MJ_per_kg": 5.2, "mass_density_kg_per_L": 1.1},
            "FusionCore": {"energy_density_MJ_per_kg": 8.4, "mass_density_kg_per_L": 1.6},
            "PlasmaCell": {"energy_density_MJ_per_kg": 6.7, "mass_density_kg_per_L": 1.3}
        }

    def generate_row(self) -> Dict[str, Any]:
        """
        Generate a single complete feature row.

        Returns:
            Dict[str, Any]: Generated feature dictionary.
        """
        car_model = random.choice(list(self.car_models.keys()))
        car_info = self.car_models[car_model]
        car_type = car_info["car_type"]
        chassis_weight = car_info["chassis_weight_kg"]

        moi_values = {
            "Micro": 0.8,
            "Coupe": 1.0,
            "Sedan": 1.2,
            "SUV": 1.5,
            "Transport": 2.0
        }
        moment_of_inertia = moi_values.get(car_type, 1.0)

        engine_weight = random.randint(*self.engine_weight_range[car_type])
        thruster_weight = random.randint(*self.thruster_weight_range[car_type])
        fuel_type = random.choice(list(self.fuel_types.keys()))
        fuel_data = self.fuel_types[fuel_type]
        fuel_weight = random.randint(100, 300)
        starting_fuel_kWh = round(random.uniform(100.0, 300.0), 1)

        total_thrust = round(random.uniform(40.0, 80.0), 1)
        thrust_rear = round(total_thrust * 0.6, 1)
        thrust_front = round(total_thrust * 0.3, 1)
        thrust_side = round(total_thrust * 0.1, 1)

        sci_fi_station_names = [
            "Lunaris Port", "Vega Spire", "Orryx Haven", "Cryon Reach",
            "Zenthar Relay", "Helion Hub", "Cerebra Ring", "Thalos Crossing"
        ]
        sci_fi_admins = [
            "Dr. Calix Renner", "Elia Vorn", "Marshal Keir", "Tamsin Ryx",
            "Axel Orov", "Captain Kael", "Zara Strix", "Commander Yulo"
        ]
        telemetry_templates = [
            "Power levels nominal. Adjusting trajectory.",
            "Fuel low. Navigating around debris.",
            "Re-routing due to unstable path.",
            "Clear path confirmed. Continuing cruise.",
            "Minor vibration detected. Monitoring systems."
        ]

        origin_station = random.choice(sci_fi_station_names)
        destination_station = random.choice([s for s in sci_fi_station_names if s != origin_station])

        assigned_by = random.choice(sci_fi_admins)
        last_telemetry_message = random.choice(telemetry_templates)
        test_date = date(4025, random.randint(1, 12), random.randint(1, 28))

        return {
            "car_type": car_type,
            "car_model": car_model,
            "engine_class": self.faker.random_element(elements=["Ion-A", "Fusion-B", "Plasma-A"]),
            "chassis_weight_kg": chassis_weight,
            "moment_of_inertia": moment_of_inertia,
            "engine_weight_kg": engine_weight,
            "thruster_weight_kg": thruster_weight,
            "fuel_weight_kg": fuel_weight,
            "starting_fuel_kWh": starting_fuel_kWh,
            "fuel_type": fuel_type,
            "energy_density_MJ_per_kg": fuel_data["energy_density_MJ_per_kg"],
            "mass_density_kg_per_L": fuel_data["mass_density_kg_per_L"],
            "total_thrust_kN": total_thrust,
            "thrust_rear_kN": thrust_rear,
            "thrust_front_kN": thrust_front,
            "thrust_side_kN": thrust_side,
            "FOV_Threat_Count": max(0, int(add_sensor_noise(random.randint(0, 8), noise_percent=0.05))),
            "Min_Distance_In_FOV": add_sensor_noise(round(random.uniform(1.0, 10.0), 2)),
            "FOV_Density": add_sensor_noise(round(random.uniform(0.1, 1.0), 2)),
            "FOV_Front_Cone_Threat_Count": max(0, int(add_sensor_noise(random.randint(0, 5), noise_percent=0.05))),
            "Angle_Weighted_Density": add_sensor_noise(round(random.uniform(0.0, 1.0), 2)),
            "Threats_Left_Sector": random.randint(0, 5),
            "Threats_Right_Sector": random.randint(0, 5),
            "Average_Threat_Angle_Offset": round(random.uniform(0.0, 90.0), 1),
            "heading_deg": random.randint(0, 359),
            "previous_heading_deg": random.randint(0, 359),
            "test_id": f"CASE-{self.faker.random_number(digits=4)}-{self.faker.random_uppercase_letter()}",
            "test_date": test_date.isoformat(),
            "assigned_by": assigned_by,
            "mission_type": "commute",
            "crew_status": "automated",
            "navigation_mode": "auto",
            "origin_station": origin_station,
            "destination_station": destination_station,
            "car_color": self.faker.color_name(),
            "last_telemetry_message": last_telemetry_message,
            "ship_serial_number": f"CXS-{random.randint(1000, 9999)}-{self.faker.random_uppercase_letter()}{self.faker.random_uppercase_letter()}"
        }

    def generate_batch(self, n: int = 1000) -> List[Dict[str, Any]]:
        """
        Generate a batch of feature rows.

        Args:
            n (int, optional): Number of rows to generate. Defaults to 1000.

        Returns:
            List[Dict[str, Any]]: List of feature dictionaries.
        """
        return [self.generate_row() for _ in range(n)]

    def export_to_csv(self, filename: str = "../data/raw_features.csv", n: int = 1000) -> None:
        """
        Generate and export a batch of feature rows to a CSV file.

        Args:
            filename (str, optional): Path to save the file. Defaults to '../data/raw_features.csv'.
            n (int, optional): Number of rows to generate. Defaults to 1000.
        """
        df = pd.DataFrame(self.generate_batch(n))
        df.to_csv(filename, index=False)
        print(f"✅ Successfully exported {n} raw records to '{filename}'")
