#!/usr/bin/env python3
"""
ACTUATOR - receives communication from the server.
The valve functions as a gate, regulating the flow of heat to a specific part of the building.
"""
import paho.mqtt.client as mqtt
from config import BROKER, AREA_ID
from decode import decode_with_id


class Valve:
    def __init__(self, id):
        self.id = id
        self.desired_temperature = 25
        self.last_read_temperature = 0
        self.is_open = False
        self.client = mqtt.Client()

    def listen(self):
        self.client.on_connect = configure
        self.client.on_message = self.process_message
        self.client.connect(BROKER)
        self.client.loop_forever()

    def process_message(self, client, userdata, message):
        topic, sensor_area_id, value = decode_with_id(message)
        print(topic, sensor_area_id, value)
        if sensor_area_id == AREA_ID:
            if topic == 'desired_temperature':
                self.process_desired_temperature(value)
            elif topic == 'temperature' and sensor_area_id:
                self.process_current_temperature(value)

    def process_current_temperature(self, temperature):
        self.last_read_temperature = temperature
        if temperature >= self.desired_temperature and self.is_open:
            self.close()
        elif not self.is_open:
            self.open()

    def process_desired_temperature(self, value):
        self.desired_temperature = value
        self.process_current_temperature(self.last_read_temperature)

    def close(self):
        print('close')
        self.is_open = False
        self.client.publish(f"valve", f'{self.id}:close')

    def open(self):
        print('open')
        self.is_open = True
        self.client.publish(f"valve", f'{self.id}:open')


def configure(client, userdata, flags, rc):
    client.subscribe(f"temperature")
    client.subscribe(f"desired_temperature")


if __name__ == "__main__":
    valve = Valve(AREA_ID)
    valve.listen()
