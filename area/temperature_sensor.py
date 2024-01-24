#!/usr/bin/env python3
"""
SENDER - sends communication to the server
Periodically measures and sends info about current temperature.
"""
import sys
from datetime import time
from typing import Callable

import paho.mqtt.client as mqtt
import w1thermsensor
from config import AREA_ID, BROKER
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont
from decode import decode_with_id


class DisplayInfo:

    def __init__(self):
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        # Clear display.
        self.disp.clear()
        self.font = ImageFont.truetype('./lib/oled/Font.ttf', 20)

    def display(self, temperature):
        self.display_on_screen(temperature)

    def display_on_screen(self, temperature):
        self.disp.clear()
        # self.disp.reset()
        image1 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        draw.text((8, 0), f'Temperature: {temperature:0.2f}', font=self.font, fill='BLACK')

    def display_on_leds(self, temperature):
        # to be implemented
        pass


# Add code that stops sensor from sending information?
class TemperatureSensor:

    def __init__(self, area_id, callback: Callable = None):
        self.area_id = area_id
        self.client = mqtt.Client()
        self.sensor = w1thermsensor.W1ThermSensor()
        self.callback = callback

    def listen(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop(force=True)
        self.client.disconnect()

    def configure(self):
        self.client.on_message = self.process_message
        self.client.connect(BROKER)
        self.client.subscribe("desired")

    def process_message(self, client, userdata, message):
        topic, sensor_area_id, value = decode_with_id(message)
        print(topic, sensor_area_id, value)
        if sensor_area_id == self.area_id:
            self.send_measurement()

    def send_measurement(self):
        temp = self.sensor.get_temperature()
        self.publish(temp)
        self.callback(temp)

    def publish(self, value):
        self.client.connect(BROKER)
        self.client.publish(f"actual", f"{self.area_id}/{value:.2f}")
        self.client.disconnect()



if __name__ == "__main__":
    id = AREA_ID if len(sys.argv) != 2 else sys.argv[1]
    sensor = TemperatureSensor(id)
    sensor.send_measurement()