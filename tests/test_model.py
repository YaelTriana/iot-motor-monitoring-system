import random

import pytest

from motormon.collector import WARNING_G
from motormon.model import MotorModel
from motormon.simulator import build_motors, make_payload


def test_healthy_motor_stays_below_warning():
    motor = MotorModel("M1", fault_probability=0.0, rng=random.Random(1))
    readings = [motor.step() for _ in range(1000)]
    assert max(readings) < WARNING_G
    assert min(readings) >= 0


def test_fault_makes_vibration_grow():
    motor = MotorModel("M1", fault_probability=1.0, rng=random.Random(1))
    early = [motor.step() for _ in range(10)]
    late = [motor.step() for _ in range(10)]
    assert motor.faulty
    assert sum(late) / 10 > sum(early) / 10


def test_repair_resets_wear():
    motor = MotorModel("M1", fault_probability=1.0, rng=random.Random(1))
    for _ in range(50):
        motor.step()
    motor.repair()
    assert motor.wear == 0 and not motor.faulty


def test_same_seed_same_readings():
    a = build_motors(3, 0.01, seed=7)
    b = build_motors(3, 0.01, seed=7)
    assert [[m.step() for _ in range(20)] for m in a] == [[m.step() for _ in range(20)] for m in b]


def test_build_motors_rejects_zero():
    with pytest.raises(ValueError):
        build_motors(0, 0.0, seed=1)


def test_payload_round_trip_is_valid_for_collector():
    from motormon.collector import parse_payload

    motor = build_motors(1, 0.0, seed=1)[0]
    assert parse_payload(make_payload(motor, 0.81, 1700000000).encode()) == ("M1", 0.81, 1700000000)
