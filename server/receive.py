#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""
"""may present current temperature?"""
"""from db???"""

from process import process_message
import paho.mqtt.client as mqtt
from config import BROKER

def send_to_process(client, userdata, message):
    process_message(message)


def configure(client, userdata, flags, rc):
    client.subscribe(f"temperature")
    client.subscribe(f"valve")


def run():
    client = mqtt.Client()
    client.on_connect = configure
    client.on_message = send_to_process
    client.connect(BROKER)
    client.loop_forever()


if __name__ == "__main__":
    run()
