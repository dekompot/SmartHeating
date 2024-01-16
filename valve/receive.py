#!/usr/bin/env python3
"""
ACTUATOR - receives communication from the server.
The valve functions as a gate, regulating the flow of heat to a specific part of the building.
"""
import paho.mqtt.client as mqtt
from config import BROKER, AREA_ID


class Valve:
    def __init__(self, id):
        self.id = id
        self.desired_temperature = None
        self.is_open = False
        self.client = mqtt.Client()

    def listen(self):
        self.client.on_connect = self.configure
        self.client.on_message = self.process_message
        self.client.connect(BROKER)
        self.client.loop_forever()

    def process_message(self, client, userdata, message):
        topic, value = decode_message(message)
        if topic == 'desired_temperature':
            self.desired_temperature = value
        elif topic == 'temperature':
            self.proceed_current_temperature(value)

    def proceed_current_temperature(self, temperature):
        if temperature >= self.desired_temperature and self.is_open:
            self.close()
        elif not self.is_open:
            self.open()

    def close(self):
        self.is_open = False
        self.client.publish(f"valves", f'close {self.id}')

    def open(self):
        self.is_open = True
        self.client.publish(f"valves", f'open {self.id}')


def decode_message(message):
    return read_topic(message), read_value(message)


def read_topic(message):
    return message.topic.split('/')[0]


def read_value(message):
    return str(message.payload.decode("utf-8"))


def configure(client, userdata, flags, rc):
    client.subscribe(f"temperature/{AREA_ID}")
    client.subscribe(f"desired_temperature/{AREA_ID}")


if __name__ == "__main__":
    valve = Valve(AREA_ID)
    valve.listen()
