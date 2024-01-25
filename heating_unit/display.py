import time

import neopixel
import board
import RPi.GPIO as GPIO
from random_colors import visualize_fire

GPIO.setmode(GPIO.BCM)
buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.HIGH)

N_LEDS = 8


class HeatingDisplay:

    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, N_LEDS, brightness=1.0 / 32, auto_write=False)
        self.colors = []
        self.heating_state = "stop"

    def on_state_change(self, new_state):
        self.heating_state = new_state
        if self.heating_state == "stop":
            # clear pixels
            self.pixels.fill((0, 0, 0))
        self.signalize_heating_state_change()

    def display_heating(self):
        if self.heating_state == "start":
            visualize_fire(self.pixels, N_LEDS)
            time.sleep(1)


    def signalize_heating_state_change(self):
        GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(buzzerPin, GPIO.HIGH)