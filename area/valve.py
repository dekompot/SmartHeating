#!/usr/bin/env python3
"""
ACTUATOR - receives communication from the server.
The valve functions as a gate, regulating the flow of heat to a specific part of the building.
"""
import paho.mqtt.client as mqtt
from config import BROKER, AREA_ID
from decode import decode_with_id


class Valve:
    def __init__(self, area_id):
        self.area_id = area_id
        self.desired_temperature = None
        self.last_read_temperature = 0
        self.is_open = False
        self.client = mqtt.Client()

    def configure(self):
        self.client.on_connect = self.configure
        self.client.on_message = self.process_message
        self.client.connect(BROKER)
        self.client.publish("ask", f"desired/{self.area_id}")

    def listen(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop(force=True)
        self.client.disconnect() #?

    def process_message(self, client, userdata, message):
        topic, sensor_area_id, value = decode_with_id(message)
        print(topic, sensor_area_id, value)
        if sensor_area_id == self.area_id:
            self.process_desired_temperature(value)

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

    def open(self):
        print('open')
        self.is_open = True

    def configure(self, client, userdata, flags, rc):
        client.subscribe(f"desired")


if __name__ == "__main__":
    valve = Valve(AREA_ID)
    valve.listen()
