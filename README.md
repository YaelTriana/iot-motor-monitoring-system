# Industrial IoT Motor Monitoring Simulator
Python • IoT • MQTT • Prometheus • Monitoring • Observability
Simulation of industrial motor vibration sensors with real-time monitoring using Prometheus and MQTT.

This project demonstrates how IoT telemetry can be collected, exported as metrics and visualized in monitoring systems.

## Technologies

Python  
MQTT  
Prometheus  
Grafana (visualization testing)
Docker  
Linux  

## Architecture

Sensor Simulator (Python)
        │
        ▼
MQTT Broker
        │
        ▼
Prometheus Metrics
        │
        ▼
Grafana Visualization

The simulator generates vibration metrics for multiple motors and exposes them for monitoring systems.

## Features

- Multi-motor vibration simulation
- Real-time telemetry streaming
- MQTT message publishing
- Prometheus metrics exporter
- Monitoring pipeline compatible with Grafana
- Easily extensible simulation architecture

## Example Metric

```
vibracion_motor{motor_id="M1"} 0.87
```

Each motor produces a time series that can be monitored and analyzed.

## Data Flow

1. Python simulator generates vibration values.
2. Data is published to MQTT topics.
3. Prometheus scrapes the metrics endpoint.
4. Metrics can be visualized in Grafana dashboards.

## Monitoring Output

### Prometheus Metrics
<img width="1874" height="1039" alt="image" src="https://github.com/user-attachments/assets/e249d75b-a62d-4cee-941c-811a77156ca6" />


## Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Run simulator

```
python simulator/motor_simulator.py
```

Prometheus endpoint:

```
http://localhost:8000
```

## Why this project

Industrial systems rely on continuous monitoring to detect anomalies before failures occur.  
This project demonstrates how a lightweight IoT monitoring pipeline can be built using open-source observability tools.

## Possible Extensions

- Real sensor integration
- Cloud deployment
- Alert rules for vibration anomalies
- Data persistence for analysis

## Author

Yael Triana
Computer Systems Engineering
