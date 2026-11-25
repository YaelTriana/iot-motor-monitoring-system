"""Publishes simulated vibration readings for N motors over MQTT.

Configuration comes from environment variables so it runs the same way in
Docker and on a laptop:

    MOTORS=3 MQTT_HOST=localhost INTERVAL=1 FAULT_PROBABILITY=0.002 SEED=42
"""

from __future__ import annotations

import json
import logging
import os
import random
import time

from motormon.model import MotorModel

log = logging.getLogger("motormon.simulator")


def build_motors(count: int, fault_probability: float, seed: int | None) -> list[MotorModel]:
    if count < 1:
        raise ValueError("MOTORS must be >= 1")
    rng = random.Random(seed)
    return [
        MotorModel(
            motor_id=f"M{i + 1}",
            baseline=round(rng.uniform(0.45, 0.75), 2),
            fault_probability=fault_probability,
            rng=random.Random(rng.random()),
        )
        for i in range(count)
    ]


def make_payload(motor: MotorModel, value: float, timestamp: int) -> str:
    return json.dumps({"motor_id": motor.motor_id, "timestamp": timestamp, "vibration_g": value})


def main() -> None:  # pragma: no cover - needs a live broker
    import paho.mqtt.client as mqtt

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    host = os.getenv("MQTT_HOST", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))
    interval = float(os.getenv("INTERVAL", "1"))
    seed = os.getenv("SEED")
    motors = build_motors(
        int(os.getenv("MOTORS", "3")),
        float(os.getenv("FAULT_PROBABILITY", "0.002")),
        int(seed) if seed else None,
    )

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="motormon-simulator")
    while True:
        try:
            client.connect(host, port, keepalive=30)
            break
        except OSError as exc:
            log.warning("broker not ready (%s), retrying in 2s", exc)
            time.sleep(2)
    client.loop_start()
    log.info("simulating %d motors -> %s:%d", len(motors), host, port)

    try:
        while True:
            now = int(time.time())
            for motor in motors:
                value = motor.step()
                client.publish(f"motors/{motor.motor_id}/vibration", make_payload(motor, value, now))
                log.debug("%s %.3f g", motor.motor_id, value)
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("stopped")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":  # pragma: no cover
    main()
