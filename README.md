# Industrial IoT Motor Monitoring Simulator

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

Sensor Simulator → MQTT Broker → Prometheus → Grafana

The simulator generates vibration metrics for multiple motors and exposes them for monitoring systems.

## Features

- Simulation of multiple industrial motors
- Real-time telemetry
- MQTT data publishing
- Prometheus metrics exporter
- Monitoring ready for Grafana dashboards
- Scriptable and extensible architecture

## Example Metric

```
vibracion_motor{motor_id="M1"} 0.87
```

Each motor produces a time series that can be monitored and analyzed.

## Screenshots

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

## Use Case

Industrial environments monitor vibration to detect anomalies and prevent equipment failure.  
This project simulates that telemetry pipeline using modern observability tools.

## Author

Yael Triana
Computer Systems Engineering
