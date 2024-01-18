#!/usr/bin/env python3
"""
SENDER - sends communication to the server
Periodically measures and sends info about current temperature.
"""
import sys
import paho.mqtt.client as mqtt
from config import AREA_ID, BROKER

def send_message(broker, area_id, value):
    client.connect(broker)
    client.publish("temperature", area_id + ":" + value)
    client.disconnect()


def measure():
    return 50


if __name__ == "__main__":
    client = mqtt.Client()
    temperature = float(sys.argv[1]) if len(sys.argv) > 1 else  measure()
    send_message(BROKER, AREA_ID, temperature)
