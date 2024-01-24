'''
import paho.mqtt.client as mqtt
# import w1thermsensor
import neopixel
import board
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
        self.pixels = neopixel.NeoPixel(board.D18, N_LEDS, brightness=1.0/32, auto_write=False)

    def display(self, temperature):
        self.display_on_screen(temperature)

    def display_on_screen(self, temperature):
        self.disp.clear()
        # self.disp.reset()
        image1 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        draw.text((8, 0), f'Temperature: {temperature:0.2f}', font=self.font, fill='BLACK')
        print(f'Temperature: {temperature:0.2f}')

    def display_on_leds(self, valve_status):
        # to be implemented
        if valve_status:
            self.pixels.fill((0, 255, 0))
        else:
            self.pixels.fill((255, 0, 0))
        self.pixels.show()
        print(f"Valve status is {valve_status}")

'''