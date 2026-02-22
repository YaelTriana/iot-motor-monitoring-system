
# Industrial IoT Motor Monitoring Simulator

Educational project demonstrating an IoT monitoring pipeline.

Python • IoT • MQTT • Prometheus • Monitoring • Observability

Simulation of industrial motor vibration sensors with a real-time telemetry and monitoring pipeline using MQTT and Prometheus.

The system simulates multiple motors publishing vibration data through MQTT while Prometheus collects and exposes metrics for monitoring.

---

# Technologies

Python  
MQTT  
Prometheus  
Grafana (visualization testing)  
Docker  
Linux  

---

# Architecture

```mermaid
flowchart LR

Simulator[Motor Simulator - Python]

MQTT[MQTT Broker]

Exporter[Metrics Endpoint]

Prometheus[Prometheus Server]

Grafana[Grafana Dashboards]

Simulator -->|publish vibration data| MQTT
Simulator -->|expose metrics| Exporter
Exporter --> Prometheus
Prometheus --> Grafana
````

---

# Features

* Multi-motor vibration simulation
* Real-time telemetry streaming
* MQTT message publishing
* Prometheus metrics exporter
* Monitoring pipeline compatible with Grafana
* Easily extensible simulation architecture

---

# Example Metric

```
# HELP vibracion_motor Motor vibration value
# TYPE vibracion_motor gauge
vibracion_motor{motor_id="M1"} 0.87
```

Each motor produces a time series that can be monitored and analyzed.

---

# Data Flow

1. Python simulator generates vibration values.
2. Data is published to MQTT topics.
3. Prometheus scrapes the metrics endpoint.
4. Metrics can be visualized in Grafana dashboards.

---

# Monitoring Output

### Prometheus Metrics

<img width="1874" height="1039" alt="image" src="https://github.com/user-attachments/assets/e249d75b-a62d-4cee-941c-811a77156ca6" />

---

# Project Structure

```
simulator/
   motor_simulator.py

metrics/
   exporter.py

docker/
   docker-compose.yml

prometheus.yml
requirements.txt
```

---

# Skills Demonstrated

IoT telemetry pipelines

Metrics collection and monitoring
MQTT messaging systems

Observability with Prometheus

Containerized development

---

# Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Run simulator

```
python simulator/motor_simulator.py
```

Prometheus endpoint

```
http://localhost:8000
```

---

# Why this project

Industrial systems rely on continuous monitoring to detect anomalies before failures occur.
This project demonstrates how a lightweight IoT monitoring pipeline can be built using open-source observability tools.

---

# Possible Extensions

* Real sensor integration
* Cloud deployment
* Alert rules for vibration anomalies
* Data persistence for analysis

---

# Author

Yael Triana

Computer Systems Engineering


