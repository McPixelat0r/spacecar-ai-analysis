import random
from faker import Faker


class CarpernicusNarrativeGen:
    def __init__(self, seed=None):
        self.fake = Faker()
        if seed is not None:
            random.seed(seed)
            Faker.seed(seed)

        self.prefixes = ["Nova", "Void", "Quantum", "Helix", "Luma", "Strato", "Aether", "Vortex"]
        self.tags = ["VX-9", "Delta-7", "XR", "Type-3", "Phantom", "Glide", "KX", "Orion"]

        self.telemetry_messages = [
            "auto-thrust calibration loop complete",
            "drift correction sequence initiated",
            "gyro lock unstable – heading recalibration needed",
            "core power routing nominal – minimal variance"
        ]

        self.failure_flags = [
            "trajectory instability",
            "sensor misalignment",
            "fuel pressure anomaly",
            "course deviation spike"
        ]

    def generate_narrative(self):
        unit_model = f"{random.choice(self.prefixes)} {random.choice(self.tags)}"

        return {
            "unit_model": unit_model,
            "sensor_suite": f"OrbitAI S{random.uniform(3.0, 5.0):.1f}",
            "last_telemetry": random.choice(self.telemetry_messages),
            "failure_flag": random.choice(self.failure_flags)
        }

    def generate_batch(self, n=10):
        return [self.generate_narrative() for _ in range(n)]
