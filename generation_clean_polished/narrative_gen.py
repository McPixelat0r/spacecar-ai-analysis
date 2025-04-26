# ===============================================
# DEPRECATED MODULE NOTICE
# -----------------------------------------------
# This module (CarpernicusNarrativeGen) was previously used
# to generate narrative-only datasets (assigned_by, car_color, etc).
#
# As of final project polishing, all narrative fields are now
# integrated directly into RawFeatureGenerator.
#
# This file is retained for historical reference but is no longer active.
# ===============================================




"""
Carpernicus Narrative Generator

Generates narrative-style synthetic data for space car missions, including test administrators,
mission types, telemetry messages, and ship serial numbers for world-building purposes.
"""

import random
import pandas as pd
from faker import Faker
from typing import Dict, Any, List


class CarpernicusNarrativeGen:
    """
    Generator for narrative flavor data (non-essential for simulation).

    Attributes:
        faker (Faker): Faker instance for generating random values.
    """

    def __init__(self, seed: int = 42) -> None:
        """
        Initialize the narrative generator with a fixed seed.

        Args:
            seed (int, optional): Random seed for reproducibility. Defaults to 42.
        """
        self.faker = Faker()
        self.faker.seed_instance(seed)
        random.seed(seed)

    def generate_record(self) -> Dict[str, Any]:
        """
        Generate a single narrative record.

        Returns:
            Dict[str, Any]: Narrative data dictionary.
        """
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

        return {
            "assigned_by": random.choice(sci_fi_admins),
            "origin_station": origin_station,
            "destination_station": destination_station,
            "mission_type": "commute",
            "crew_status": "automated",
            "navigation_mode": "auto",
            "car_color": self.faker.color_name(),
            "last_telemetry_message": random.choice(telemetry_templates),
            "ship_serial_number": f"CXS-{random.randint(1000, 9999)}-{self.faker.random_uppercase_letter()}{self.faker.random_uppercase_letter()}"
        }

    def export_to_csv(self, filename: str = "narrative_data.csv", n: int = 1000) -> None:
        """
        Generate n narrative records and export them to a CSV file.

        Args:
            filename (str, optional): Path to save the file. Defaults to 'narrative_data.csv'.
            n (int, optional): Number of records to generate. Defaults to 1000.
        """
        records = [self.generate_record() for _ in range(n)]
        df = pd.DataFrame(records)
        df.to_csv(filename, index=False)
        print(f"✅ Successfully exported {n} narrative records to '{filename}'")
