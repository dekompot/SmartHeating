#!/usr/bin/env python3
"""
SENDER - sends communication to the server
Periodically measures and sends info about current temperature.
"""
import sys
import paho.mqtt.client as mqtt
import w1thermsensor
from config import AREA_ID, BROKER

class TemperatureSensor:

    def __init__(self, broker, area_id, frequency=2):
        self.broker = broker
        self.area_id = area_id
        self.client = mqtt.Client()
        self.frequency = frequency
        self.sensor = w1thermsensor.W1ThermSensor()


    def measure(self):
        temp = self.sensor.get_temperature()
        self.send_message(temp)
        return temp

    def send_message(self, value):
        self.client.connect(self.broker)
        self.client.publish("temperature", f"{self.area_id}:{value:.2f}")
        self.client.disconnect()


if __name__ == "__main__":
    sensor = TemperatureSensor(BROKER, AREA_ID, 2)
    print(sensor.measure())