import paho.mqtt.client as mqtt
# import w1thermsensor
import neopixel
import board
import time
from config import AREA_ID, BROKER, N_LEDS
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont
from temperature_sensor import MockSensor


class AreaDisplay:

    def __init__(self, area_id):
        self.area_id = area_id
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        # Clear display.
        self.disp.clear()
        self.fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
        self.fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 13)
        self.pixels = neopixel.NeoPixel(board.D18, N_LEDS, brightness=1.0/32, auto_write=False)
        self.pixels.fill((0,0,0))
        self.pixels.show()

    def display(self, temperature):
        self.display_temperature(temperature)

    def display_temperature(self, temperature: float):
        self.disp.clear()
        image1 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        draw.text((8, 0), f'Area: {self.area_id}', font=self.fontSmall, fill='BLACK')
        draw.text((8, 10), f'Temp: {temperature:0.2f}', font=self.fontLarge, fill='BLACK')
        self.disp.ShowImage(image1, 0, 0)
        print(f'Temperature: {temperature:0.2f}')

    def display_valve(self, valve_status: bool):
        # to be implemented
        if valve_status:
            self.pixels.fill((0, 255, 0))
        else:
            self.pixels.fill((255, 0, 0))
        self.pixels.show()
        print(f"Valve status is {valve_status}")

if __name__ == "__main__":
    area_display = AreaDisplay(1)
    sensor = MockSensor()
    while True:
        area_display.display_valve(False)
        time.sleep(1)
        area_display.display_valve(True)
        time.sleep(1)
        area_display.display_temperature(sensor.get_temperature())
        time.sleep(1)