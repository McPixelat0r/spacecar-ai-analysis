import random
import math


class SimulatedCrashEnvironment:
    def __init__(self, grid_size=(100, 100), perception_radius=20):
        self.grid_width, self.grid_height = grid_size
        self.perception_radius = perception_radius

    def place_car(self):
        # Random starting position and heading
        self.car_x = random.uniform(10, self.grid_width - 10)
        self.car_y = random.uniform(10, self.grid_height - 10)
        self.heading_deg = random.uniform(0, 360)

    def generate_obstacles(self, count=10):
        # Place obstacles randomly within the perception radius
        self.obstacles = []
        for _ in range(count):
            angle = random.uniform(0, 360)
            distance = random.uniform(1, self.perception_radius)
            dx = distance * math.cos(math.radians(angle))
            dy = distance * math.sin(math.radians(angle))
            ox = self.car_x + dx
            oy = self.car_y + dy
            self.obstacles.append((ox, oy))

    def check_for_crash(self, forward_distance=5, collision_radius=2):
        # Project forward from car's heading
        fx = self.car_x + forward_distance * math.cos(math.radians(self.heading_deg))
        fy = self.car_y + forward_distance * math.sin(math.radians(self.heading_deg))
        for ox, oy in self.obstacles:
            dist = math.hypot(fx - ox, fy - oy)
            if dist < collision_radius:
                return 1  # Crash occurred
        return 0  # No crash
