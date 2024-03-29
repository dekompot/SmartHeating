"""
ACTUATOR - receives communication from the server.
The heating unit processes messages from server to heat up temperature.
This programm may communicate with an interface of working heating unit.
"""
import time
import paho.mqtt.client as mqtt
from config import BROKER, SLEEP
from display import HeatingDisplay


class HeatingUnit:

    def __init__(self):
        self.client = mqtt.Client()
        self.state = "stop"

    def connect_to_broker(self):
        self.client.connect(BROKER)
        self.client.subscribe(f"heating")
        self.client.on_message = self.process_message

    def listen(self):
        self.connect_to_broker()
        self.client.loop_start()

    def process_message(self, client, userdata, message):
        self.state = message.payload.decode("utf-8")
        self.state_change()

    def state_change(self):
        print(self.state)


if __name__ == "__main__":

    heating_unit = HeatingUnit()
    heating_unit.listen()

    heating_display = HeatingDisplay()

    while True:
        heating_display.on_state_change(heating_unit.state)
        if heating_unit.state == "start":
            heating_display.display_heating()
            time.sleep(SLEEP)
