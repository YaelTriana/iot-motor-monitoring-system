# Industrial IoT Motor Monitoring System

Simulation of an industrial motor vibration monitoring system using IoT technologies.

The project simulates multiple sensors sending vibration data to an MQTT broker.  
Metrics are collected with Prometheus and visualized with Grafana dashboards.

## Technologies

- Python
- MQTT
- Docker
- Prometheus
- Grafana
- Linux

## Architecture

Sensor Simulator → MQTT → Prometheus → Grafana

## Features

- Simulation of multiple industrial sensors
- Real-time data streaming
- Monitoring with Prometheus
- Visualization dashboards in Grafana
- Alert simulation
- Containerized environment using Docker

## Project Structure

```
simulator        Sensor simulation
mqtt             MQTT communication
monitoring       Prometheus configuration
dashboard        Grafana dashboards
docker           Docker setup
```

## Screenshots

Add Grafana dashboards here.

## Use Case

Industrial environments require continuous monitoring of motor vibration to detect anomalies and prevent failures.  
This project demonstrates how IoT and observability tools can be combined to build such monitoring systems.

## Author

Yael Triana
