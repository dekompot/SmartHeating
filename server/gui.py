#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""
"""may present current temperature?"""
"""from db???"""

import paho.mqtt.client as mqtt
import tkinter
from process import process_desired_temperature, get_temperature
from server.config import NUMBER_OF_AREAS, DEFAULT_TEMPERATURE, BROKER

client = mqtt.Client()

class GUI:
    def __int__(self, number):
        self.window = tkinter.Tk()
        self.number_of_areas = NUMBER_OF_AREAS
        self.desired_temperatures = [tkinter.IntVar(DEFAULT_TEMPERATURE)] * NUMBER_OF_AREAS
        self.actual_temperatures = [tkinter.IntVar(0)] * NUMBER_OF_AREAS

    def run(self):
        self.setup()
        self.window.mainloop()

    def setup(self):
        self.window.geometry(F"250x{self.number_of_areas * 150}")
        self.window.title("TITLE")
        label = tkinter.Label(self.window, text="MAIN_LABEL")
        label.grid(row=0,columnspan=NUMBER_OF_AREAS)

        for i in range(NUMBER_OF_AREAS):
            label = tkinter.Label(self.window, text=f"area {i} : ")
            label.grid(row=i+1, column=0)
            spinbox = tkinter.Spinbox(self.window, from_=0, to=30,
                                      textvariable=self.desired_temperatures[i], command=lambda: self.update(i))
            spinbox.grid(row=i+1, column=1)
            label = tkinter.Label(self.window, textvariable=self.actual_temperatures[i])

        exit_button = tkinter.Button(self.window, text="Exit", command=window.quit)
        print_log_button = tkinter.Button(self.window, text="REFRESH", command=refresh)
        label.pack()
        exit_button.pack(side="right")
        print_log_button.pack(side="right")

    def update(self, index):
        """TO MOZE NIE DZIALA CXDDDDD"""
        desired_temperature = self.desired_temperatures[index]
        process_desired_temperature(index, desired_temperature)
        client.publish('desired_temperature', f'{index}:{self.desired_temperatures[index]}')

    def refresh(self, client, userdata, message):
        id, value = get_temperature(message)
        self.actual_temperatures[id].set(value)


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    client.connect(BROKER)
    gui = GUI()
    client.on_message = gui.refresh()
    client.loop_start()
    gui.run()
    disconnect_from_broker()
