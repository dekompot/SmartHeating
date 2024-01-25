import sys
import time

from display import AreaDisplay, MockSensor
from temperature_sensor import TemperatureSensor
from valve import Valve


class Area:

    def __init__(self, area_id, frequency, is_mock, temp_callbacks, valve_callbacks):
        self.area_id = area_id
        self.frequency = frequency
        self.valve = Valve(self.area_id, callbacks=valve_callbacks)
        self.temperature_sensor = TemperatureSensor(self.area_id,
                                                    callbacks=[self.valve.process_current_temperature,
                                                               *temp_callbacks])
        if is_mock:
            self.temperature_sensor.sensor = MockSensor()

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


if __name__ == "__main__":
    area_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    frequency = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    is_mock = len(sys.argv) > 3

    area_display = AreaDisplay(area_id=area_id)
    area = Area(area_id=area_id, frequency=frequency, is_mock=is_mock,
                valve_callbacks=[area_display.display_valve],
                temp_callbacks=[area_display.display_temperature])
    area.configure()
    area.listen()
    area.loop()
