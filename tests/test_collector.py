import json
import math

import pytest

from motormon.collector import (
    CRITICAL_G,
    STATUS_CRITICAL,
    STATUS_OK,
    STATUS_WARNING,
    WARNING_G,
    Collector,
    RollingRMS,
    classify,
    parse_payload,
)


def msg(motor="M1", value=0.5, ts=1700000000):
    return json.dumps({"motor_id": motor, "vibration_g": value, "timestamp": ts}).encode()


@pytest.mark.parametrize(
    ("rms", "expected"),
    [(0.0, STATUS_OK), (WARNING_G - 0.01, STATUS_OK), (WARNING_G, STATUS_WARNING), (CRITICAL_G, STATUS_CRITICAL)],
)
def test_classify(rms, expected):
    assert classify(rms) == expected


def test_rolling_rms_uses_only_the_window():
    rms = RollingRMS(size=2)
    rms.add(10.0)
    rms.add(3.0)
    assert rms.add(4.0) == pytest.approx(math.sqrt((9 + 16) / 2))


def test_rolling_rms_rejects_empty_window():
    with pytest.raises(ValueError):
        RollingRMS(size=0)


@pytest.mark.parametrize(
    "raw",
    [
        b"not json",
        b"[1, 2]",
        json.dumps({"vibration_g": 1, "timestamp": 1}).encode(),
        json.dumps({"motor_id": "M1", "vibration_g": -1, "timestamp": 1}).encode(),
        json.dumps({"motor_id": "M1", "vibration_g": True, "timestamp": 1}).encode(),
        json.dumps({"motor_id": "M1", "vibration_g": 1, "timestamp": "now"}).encode(),
    ],
)
def test_parse_payload_rejects_bad_messages(raw):
    with pytest.raises(ValueError):
        parse_payload(raw)


def sample(collector, name, motor=None):
    labels = {"motor_id": motor} if motor else {}
    return collector.registry.get_sample_value(name, labels)


def test_collector_updates_metrics():
    c = Collector()
    assert c.handle(msg(value=0.5))
    assert sample(c, "motor_vibration_g", "M1") == 0.5
    assert sample(c, "motor_status", "M1") == STATUS_OK
    assert sample(c, "motor_last_message_timestamp_seconds", "M1") == 1700000000
    assert sample(c, "mqtt_messages_total") == 1


def test_collector_raises_status_on_sustained_vibration():
    c = Collector(window=3)
    for _ in range(3):
        c.handle(msg(value=2.0))
    assert sample(c, "motor_status", "M1") == STATUS_CRITICAL


def test_collector_counts_invalid_messages_and_keeps_going():
    c = Collector()
    assert not c.handle(b"garbage")
    assert c.handle(msg())
    assert sample(c, "mqtt_invalid_messages_total") == 1
    assert sample(c, "mqtt_messages_total") == 1


def test_collector_tracks_motors_independently():
    c = Collector(window=1)
    c.handle(msg("M1", 0.4))
    c.handle(msg("M2", 1.5))
    assert sample(c, "motor_status", "M1") == STATUS_OK
    assert sample(c, "motor_status", "M2") == STATUS_WARNING
