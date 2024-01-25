
#!/usr/bin/env python3
import random
import sys
import time
from typing import Callable, List

import paho.mqtt.client as mqtt
import w1thermsensor
from config import AREA_ID, BROKER
from decode import decode_temperature

N_LEDS = 8


class MockSensor:
    def get_temperature(self):
        return 16 + random.random() * 2


# Add code that stops sensor from sending information?
class TemperatureSensor:

    def __init__(self, area_id, callbacks: List[Callable] = None):
        self.area_id = area_id
        self.temperature = 0
        self.client = mqtt.Client()
        self.sensor = w1thermsensor.W1ThermSensor()
        self.callbacks = callbacks

    def listen(self):
        self.client.loop_start()

    def stop(self, client, userdata, rc):
        self.client.loop_stop(force=True)

    def configure(self):
        self.client.on_message = self.process_message
        self.client.connect(BROKER)
        self.client.on_disconnect = self.stop
        self.client.subscribe("desired")

    def process_message(self, client, userdata, message):
        topic, sensor_area_id, value = decode_temperature(message)
        print(topic, sensor_area_id, value)
        if sensor_area_id == self.area_id:
            self.send_measurement()

    def send_measurement(self):
        self.temperature = self.sensor.get_temperature()
        self.publish(self.temperature)
        for callback in self.callbacks:
            callback(self.temperature)

    def publish(self, value):
        print(f"Publishing actual {self.area_id}/{value:.2f}")
        self.client.publish(f"actual", f"{self.area_id}/{value:.2f}")