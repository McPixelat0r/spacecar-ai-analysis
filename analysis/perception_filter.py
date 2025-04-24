import numpy as np
import pandas as pd


class PerceptionFilter:
    def __init__(self, fov_deg=120, view_radius=50):
        self.fov = fov_deg
        self.radius = view_radius

    def _angle_between(self, dx, dy, car_angle_deg):
        angle_to_object = np.degrees(np.arctan2(dy, dx))
        angle_diff = (angle_to_object - car_angle_deg + 360) % 360
        return angle_diff if angle_diff <= 180 else 360 - angle_diff

    def filter(self, asteroid_df, car_position, car_angle_deg):
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
            # Simple area-based density (2D cone area approximation)
            area = (self.fov / 360) * np.pi * self.radius ** 2
            derived_stats["FOV_Density"] = len(df_filtered) / area
        else:
            df_filtered = pd.DataFrame(columns=asteroid_df.columns)

        return df_filtered, derived_stats


if __name__ == '__main__':
    # Sample asteroid dataset
    asteroids = pd.DataFrame({
        "x": [10, 30, -15, 40, 5],
        "y": [5, 25, 10, -10, 0],
        "diameter": [0.5, 3, 2, 1.5, 0.8],
        "velocity": [1, 5, 3, 4, 2]
    })

    # Car state
    car_pos = (0, 0)
    car_angle = 0  # Facing right (along +x)

    # Filter
    pf = PerceptionFilter(fov_deg=120, view_radius=50)
    filtered_df, stats = pf.filter(asteroids, car_pos, car_angle)

    print("Filtered Asteroids:")
    print(filtered_df)
    print("\nDerived Stats:")
    print(stats)
