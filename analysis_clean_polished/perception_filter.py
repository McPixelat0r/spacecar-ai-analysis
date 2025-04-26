"""
Perception Filter Module

This module provides a class for filtering objects (e.g., asteroids) within a space car's
field of view (FOV) and view radius. It also derives basic spatial statistics.
"""

import numpy as np
import pandas as pd
from typing import Tuple


class PerceptionFilter:
    """
    A filter for detecting objects within a car's field of view and range.

    Attributes:
        fov (float): Field of view in degrees.
        radius (float): Maximum viewable radius.
    """

    def __init__(self, fov_deg: float = 120.0, view_radius: float = 50.0) -> None:
        """
        Initialize the PerceptionFilter.

        Args:
            fov_deg (float, optional): Field of view in degrees. Defaults to 120.
            view_radius (float, optional): View radius in arbitrary distance units. Defaults to 50.
        """
        self.fov = fov_deg
        self.radius = view_radius

    def _angle_between(self, dx: float, dy: float, car_angle_deg: float) -> float:
        """
        Calculate the smallest angle difference between the car and an object.

        Args:
            dx (float): Delta x (object - car).
            dy (float): Delta y (object - car).
            car_angle_deg (float): Car's current facing direction in degrees.

        Returns:
            float: Absolute angle difference in degrees.
        """
        angle_to_object = np.degrees(np.arctan2(dy, dx))
        angle_diff = (angle_to_object - car_angle_deg + 360) % 360
        return angle_diff if angle_diff <= 180 else 360 - angle_diff

    def filter(self, asteroid_df: pd.DataFrame, car_position: Tuple[float, float], car_angle_deg: float) -> Tuple[
        pd.DataFrame, dict]:
        """
        Filter asteroids within FOV and range and compute derived stats.

        Args:
            asteroid_df (pd.DataFrame): DataFrame with asteroid data (must contain 'x' and 'y' columns).
            car_position (Tuple[float, float]): (x, y) coordinates of the car.
            car_angle_deg (float): Car's facing angle in degrees.

        Returns:
            Tuple[pd.DataFrame, dict]: Filtered asteroids and derived stats dictionary.
        """
        if not isinstance(asteroid_df, pd.DataFrame):
            raise TypeError("asteroid_df must be a pandas DataFrame.")

        filtered_rows = []
        derived_stats = {
            "FOV_Threat_Count": 0,
            "Min_Distance_In_FOV": np.inf,
            "Avg_Distance_In_FOV": None,
            "FOV_Density": 0
        }

        car_x, car_y = car_position
        distances = []

        for _, asteroid in asteroid_df.iterrows():
            dx = asteroid["x"] - car_x
            dy = asteroid["y"] - car_y
            distance = np.hypot(dx, dy)
            angle = self._angle_between(dx, dy, car_angle_deg)

            if distance <= self.radius and angle <= self.fov / 2:
                filtered_rows.append(asteroid)
                distances.append(distance)

        if filtered_rows:
            df_filtered = pd.DataFrame(filtered_rows)
            derived_stats["FOV_Threat_Count"] = len(df_filtered)
            derived_stats["Min_Distance_In_FOV"] = min(distances)
            derived_stats["Avg_Distance_In_FOV"] = np.mean(distances)
            # Estimate FOV area as a sector of a circle
            area = (self.fov / 360) * np.pi * self.radius ** 2
            derived_stats["FOV_Density"] = len(df_filtered) / area
        else:
            df_filtered = pd.DataFrame(columns=asteroid_df.columns)

        return df_filtered, derived_stats


if __name__ == "__main__":
    # Example usage / Test block
    asteroids = pd.DataFrame({
        "x": [10, 30, -15, 40, 5],
        "y": [5, 25, 10, -10, 0],
        "diameter": [0.5, 3.0, 2.0, 1.5, 0.8],
        "velocity": [1.0, 5.0, 3.0, 4.0, 2.0]
    })

    car_pos = (0, 0)
    car_angle = 0  # Facing right (0 degrees)

    pf = PerceptionFilter(fov_deg=120, view_radius=50)
    filtered_df, stats = pf.filter(asteroids, car_pos, car_angle)

    print("Filtered Asteroids:")
    print(filtered_df)
    print("\nDerived Stats:")
    print(stats)
