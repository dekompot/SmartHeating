#!/usr/bin/env python3
"""
SENDER - sends communication to the server
Periodically measures and sends info about current temperature.
"""
import sys
import paho.mqtt.client as mqtt
import w1thermsensor
from config import AREA_ID, BROKER
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont


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


# Add code that stops sensor from sending information?
class TemperatureSensor:

    def __init__(self, broker, area_id, frequency=2, callback: Callable = None):
        self.broker = broker
        self.area_id = area_id
        self.client = mqtt.Client()
        self.frequency = frequency
        self.sensor = w1thermsensor.W1ThermSensor()
        self.callback = callback

    def measure(self):
        while True:
            temp = self.sensor.get_temperature()
            self.send_message(temp)
            self.callback(temp)
            time.sleep(self.frequency)

    def send_message(self, value):
        self.client.connect(self.broker)
        self.client.publish("temperature", f"{self.area_id}:{value:.2f}")
        self.client.disconnect()


if __name__ == "__main__":
    id = AREA_ID if len(sys.argv) != 2 else sys.argv[1]
    sensor = TemperatureSensor(BROKER, id)
    sensor.measure()