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


class HeatingUnit:

    def __init__(self, callback):
        self.callback = callback
        self.client = mqtt.Client()
        self.state = "stop"

    def connect_to_broker(self):
        self.client.connect(BROKER)
        self.client.subscribe(f"heating")
        self.client.on_message = self.process_message

    def listen(self):
        self.connect_to_broker()
        self.client.loop_forever()

    def process_message(self, client, userdata, message):
        self.state = message.payload.decode("utf-8")
        self.state_change()

    def state_change(self):
        self.callback(self.state)
        print(self.state)


def mock_callback(state):
    print(state)


if __name__ == "__main__":
    heating_unit = HeatingUnit(mock_callback)
    heating_unit.listen()
