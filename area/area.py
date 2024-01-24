import time

import paho.mqtt.client as mqtt

from area.temperature_sensor import TemperatureSensor
from area.valve import Valve


class Area:

    def __init__(self, area_id, frequency):
        self.area_id = area_id
        self.frequency = frequency
        self.valve = Valve(self.area_id)
        self.temperature_sensor = TemperatureSensor(self.area_id, callback=self.valve.process_current_temperature)

    def configure(self):
        self.valve.configure()
        self.temperature_sensor.configure()

    def listen(self):
        self.valve.listen()
        self.temperature_sensor.listen()

    def loop(self):
        while True:
            self.temperature_sensor.send_measurement()
            time.sleep(self.frequency)

    def stop(self):
        self.valve.stop()
        self.temperature_sensor.stop()



