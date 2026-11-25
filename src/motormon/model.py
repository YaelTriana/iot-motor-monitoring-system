"""Vibration model for a simulated industrial motor.

Values are RMS acceleration in g. A healthy motor oscillates around its
baseline; once a fault starts (bearing wear), vibration grows a little on
every tick until someone notices it in Grafana or an alert fires.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field


@dataclass
class MotorModel:
    motor_id: str
    baseline: float = 0.6
    noise: float = 0.05
    fault_probability: float = 0.002
    degradation_per_tick: float = 0.01
    rng: random.Random = field(default_factory=random.Random)
    wear: float = 0.0
    faulty: bool = False
    tick: int = 0

    def step(self) -> float:
        """Advance one tick and return the new vibration reading."""
        self.tick += 1
        if not self.faulty and self.rng.random() < self.fault_probability:
            self.faulty = True
        if self.faulty:
            self.wear += self.degradation_per_tick
        # Small periodic component, like the shaft's rotation harmonic.
        harmonic = 0.05 * math.sin(self.tick / 5)
        value = self.baseline + harmonic + self.wear + self.rng.gauss(0, self.noise)
        return round(max(value, 0.0), 3)

    def repair(self) -> None:
        self.faulty = False
        self.wear = 0.0
