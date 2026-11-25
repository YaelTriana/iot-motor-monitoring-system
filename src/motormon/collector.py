"""MQTT -> Prometheus collector.

Subscribes to every motor's vibration topic, validates each message, keeps a
rolling RMS per motor and exposes everything as Prometheus metrics.
"""

from __future__ import annotations

import json
import logging
import math
import os
import time
from collections import deque

from prometheus_client import CollectorRegistry, Counter, Gauge, start_http_server

log = logging.getLogger("motormon.collector")

# Design assumptions for this simulation, not values from a standard.
WARNING_G = 1.2
CRITICAL_G = 1.8

STATUS_OK, STATUS_WARNING, STATUS_CRITICAL = 0, 1, 2


def classify(rms: float) -> int:
    if rms >= CRITICAL_G:
        return STATUS_CRITICAL
    if rms >= WARNING_G:
        return STATUS_WARNING
    return STATUS_OK


class RollingRMS:
    def __init__(self, size: int = 10) -> None:
        if size < 1:
            raise ValueError("size must be >= 1")
        self._values: deque[float] = deque(maxlen=size)

    def add(self, value: float) -> float:
        self._values.append(value)
        return math.sqrt(sum(v * v for v in self._values) / len(self._values))


def parse_payload(raw: bytes) -> tuple[str, float, int]:
    """Return (motor_id, vibration_g, timestamp) or raise ValueError."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"not JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("payload must be a JSON object")
    motor_id = data.get("motor_id")
    value = data.get("vibration_g")
    ts = data.get("timestamp")
    if not isinstance(motor_id, str) or not motor_id:
        raise ValueError("missing motor_id")
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError("vibration_g must be a non-negative number")
    if isinstance(ts, bool) or not isinstance(ts, int):
        raise ValueError("timestamp must be an integer")
    return motor_id, float(value), ts


class Collector:
    def __init__(self, registry: CollectorRegistry | None = None, window: int = 10) -> None:
        self.registry = registry or CollectorRegistry()
        self.window = window
        self._rms: dict[str, RollingRMS] = {}
        labels = ["motor_id"]
        self.vibration = Gauge("motor_vibration_g", "Last vibration reading (g)", labels, registry=self.registry)
        self.rms = Gauge("motor_vibration_rms_g", "Rolling RMS vibration (g)", labels, registry=self.registry)
        self.status = Gauge("motor_status", "0=ok, 1=warning, 2=critical", labels, registry=self.registry)
        self.last_seen = Gauge(
            "motor_last_message_timestamp_seconds", "Timestamp of the last message", labels, registry=self.registry
        )
        self.messages = Counter("mqtt_messages_total", "Valid MQTT messages", registry=self.registry)
        self.invalid = Counter("mqtt_invalid_messages_total", "Rejected MQTT messages", registry=self.registry)

    def handle(self, raw: bytes) -> bool:
        try:
            motor_id, value, ts = parse_payload(raw)
        except ValueError as exc:
            self.invalid.inc()
            log.warning("invalid message: %s", exc)
            return False
        rms = self._rms.setdefault(motor_id, RollingRMS(self.window)).add(value)
        self.vibration.labels(motor_id).set(value)
        self.rms.labels(motor_id).set(rms)
        self.status.labels(motor_id).set(classify(rms))
        self.last_seen.labels(motor_id).set(ts)
        self.messages.inc()
        return True


def main() -> None:  # pragma: no cover - needs a live broker
    import paho.mqtt.client as mqtt

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    host = os.getenv("MQTT_HOST", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))
    topic = os.getenv("MQTT_TOPIC", "motors/+/vibration")
    metrics_port = int(os.getenv("METRICS_PORT", "8000"))

    collector = Collector()
    start_http_server(metrics_port, registry=collector.registry)
    log.info("metrics on :%d", metrics_port)

    def on_connect(client, _userdata, _flags, reason_code, _props):
        log.info("connected to %s:%d (%s), subscribing to %s", host, port, reason_code, topic)
        client.subscribe(topic)

    def on_message(_client, _userdata, msg):
        collector.handle(msg.payload)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="motormon-collector")
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(host, port, keepalive=30)
            break
        except OSError as exc:
            log.warning("broker not ready (%s), retrying in 2s", exc)
            time.sleep(2)
    client.loop_forever(retry_first_connection=True)


if __name__ == "__main__":  # pragma: no cover
    main()
