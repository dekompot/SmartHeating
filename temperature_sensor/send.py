#!/usr/bin/env python3
"""
SENDER - sends communication to the server
Periodically measures and sends info about current temperature.
"""
import paho.mqtt.client as mqtt
from config import AREA_ID, BROKER

def send_message(broker, sensor_id, value):
    client.connect(broker)
    client.publish(f"temperature/{sensor_id}", value)
    client.disconnect()


def measure():
    return 50


if __name__ == "__main__":
    client = mqtt.Client()
    temperature = measure()
    send_message(BROKER, AREA_ID, temperature)
