"""
ACTUATOR - receives communication from the server.
The heating unit processes messages from server to heat up temperature.
This programm may communicate with an interface of working heating unit.
"""
#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""
"""may present current temperature?"""
"""from db???"""

import paho.mqtt.client as mqtt
from config import BROKER

def heat():
    print("ogrzewaj!")


def configure(client, userdata, flags, rc):
    client.subscribe(f"heating")


def run():
    client = mqtt.Client()
    client.on_connect = configure
    client.on_message = heat
    client.connect(BROKER)
    client.loop_forever()


if __name__ == "__main__":
    run()
