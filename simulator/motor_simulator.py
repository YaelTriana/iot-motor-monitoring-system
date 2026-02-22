import time
import random
import json
import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Gauge

# --- Configuración MQTT ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "motores/vibracion"

# --- Preguntar cuántos motores simular ---
while True:
    try:
        cantidad = int(input("¿Cuántos motores quieres simular? "))
        if cantidad < 1:
            print("Por favor, ingresa un número mayor que cero.")
            continue
        break
    except ValueError:
        print("Entrada no válida. Ingresa un número entero.")

# --- Generar lista de motores dinámicamente ---
MOTORES = [f"M{i+1}" for i in range(cantidad)]

# --- Métrica Prometheus con etiqueta por motor ---
vibracion_metric = Gauge("vibracion_motor", "Nivel de vibración del motor", ["motor_id"])

# --- Inicializar MQTT ---
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# --- Servidor Prometheus ---
start_http_server(8000)

# --- Función para generar vibración aleatoria ---
def generar_vibracion():
    return round(random.uniform(0.2, 1.5), 2)

# --- Loop principal ---
try:
    while True:
        timestamp = int(time.time())

        for motor_id in MOTORES:
            vibracion = generar_vibracion()

            # Publicar en MQTT
            payload = {
                "motor_id": motor_id,
                "timestamp": timestamp,
                "vibracion": vibracion
            }
            mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))

            # Actualizar métrica Prometheus
            vibracion_metric.labels(motor_id=motor_id).set(vibracion)

            print(f"[{timestamp}] {motor_id} → {vibracion} g")

        time.sleep(1)

except KeyboardInterrupt:
    print("Simulación detenida.")
    mqtt_client.disconnect()
