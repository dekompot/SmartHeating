#!/usr/bin/env python3
"""
ACTUATOR - receives communication from the server.
The valve functions as a gate, regulating the flow of heat to a specific part of the building.
"""
from typing import List, Callable

import paho.mqtt.client as mqtt
from config import BROKER, AREA_ID, DEBOUNCE_VALUE
from decode import decode_temperature


class Valve:
    def __init__(self, area_id, callbacks: List[Callable] = None):
        self.area_id = area_id
        self.desired_temperature = 20.0
        self.last_read_temperature = 0.0
        self.is_open = False
        self.callbacks = callbacks
        self.client = mqtt.Client()

    def configure(self):
        # self.client.on_connect = self.configure_client
        self.client.on_message = self.process_message
        self.client.on_disconnect = self.stop
        self.client.connect(BROKER)
        self.client.subscribe(f"desired")
        self.client.publish("ask", f"desired/{self.area_id}")

    def listen(self):
        self.client.loop_start()

    def stop(self, client, userdata, rc):
        self.client.loop_stop(force=True)

    def process_message(self, client, userdata, message):
        topic, sensor_area_id, value = decode_temperature(message)
        print(f"On valve {self.area_id}", topic, sensor_area_id, value)
        if sensor_area_id == self.area_id:
            self.process_desired_temperature(value)

    def process_current_temperature(self, temperature):
        self.last_read_temperature = temperature
        if temperature >= self.desired_temperature + DEBOUNCE_VALUE and self.is_open:
            self.close()
        elif temperature < self.desired_temperature - DEBOUNCE_VALUE and not self.is_open:
            self.open()
        for callback in self.callbacks:
            callback(self.is_open)

    def process_desired_temperature(self, value):
        self.desired_temperature = value
        self.process_current_temperature(self.last_read_temperature)

    def close(self):
        print('close')
        self.is_open = False

    def open(self):
        print('open')
        self.is_open = True
