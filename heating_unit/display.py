import random
import time

import RPi.GPIO as GPIO
import board
import neopixel

from config import N_LEDS, SLEEP

GPIO.setmode(GPIO.BCM)
buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.HIGH)


def generate_fire_color():
    red = random.randint(200, 255)
    green = random.randint(0, 100)
    blue = random.randint(0, 25)

    color = (red, green, blue)
    return color


def visualize_fire(pixels, n_pixels):
    for i in range(n_pixels):
        pixels[i] = generate_fire_color()
    pixels.show()


def signalize_heating_state_change():
    for i in range(2):
        buzz()


def buzz():
    GPIO.output(buzzerPin, GPIO.LOW)
    time.sleep(SLEEP)
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(SLEEP)

class HeatingDisplay:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, N_LEDS, brightness=1.0 / 32, auto_write=False)
        self.colors = []
        self.heating_state = "stop"

    def on_state_change(self, new_state):
        if new_state != self.heating_state:
            self.heating_state = new_state
            if self.heating_state == "stop":
                # clear pixels
                self.pixels.fill((0, 0, 0))
                self.pixels.show()
                print("cleared out")
            signalize_heating_state_change()

    def display_heating(self):
        visualize_fire(self.pixels, N_LEDS)
