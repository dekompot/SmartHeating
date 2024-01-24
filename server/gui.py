#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""
"""may present current temperature?"""
"""from db???"""

import paho.mqtt.client as mqtt
import tkinter
from process import process_desired_temperature, get_temperature
from config import NUMBER_OF_AREAS, DEFAULT_TEMPERATURE, BROKER

client = mqtt.Client()

class GUI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.number_of_areas = NUMBER_OF_AREAS
        self.desired_temperatures = [tkinter.IntVar(self.window, DEFAULT_TEMPERATURE) for i in range(NUMBER_OF_AREAS)] 
        self.actual_temperatures = [tkinter.IntVar(self.window, 0) for i in range(NUMBER_OF_AREAS)] 

    def run(self):
        self.setup()
        self.window.mainloop()

    def setup(self):
        self.window.title("TITLE")
        label = tkinter.Label(self.window, text="MAIN_LABEL")
        label.grid(row=0, columnspan=NUMBER_OF_AREAS)

        for i in range(NUMBER_OF_AREAS):
            label = tkinter.Label(self.window, text=f"area {i} : ")
            label.grid(row=i+1, column=0)
            spinbox = tkinter.Spinbox(self.window, from_=0, to=30,
                                      textvariable=self.desired_temperatures[i], command=lambda i=i: self.update(i))
            spinbox.grid(row=i+1, column=1)
            label = tkinter.Label(self.window, textvariable=self.actual_temperatures[i])
            label.grid(row=i+1, column=2)

        exit_button = tkinter.Button(self.window, text="Exit", command=self.window.quit)
        exit_button.grid(row=i+2, column=1)

    def update(self, index):
        """TO MOZE NIE DZIALA CXDDDDD"""
        desired_temperature = self.desired_temperatures[index].get()
        print(desired_temperature)
        # process_desired_temperature(index, desired_temperature)
        client.publish('desired_temperature', f'{index}:{desired_temperature}')

    def refresh(self, client, userdata, message):
        id, value = get_temperature(message)
        self.actual_temperatures[id].set(value)


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()

def configure(client, userdata, flags, rc):
    client.subscribe(f"temperature")

if __name__ == "__main__":
    client.connect(BROKER)
    gui = GUI()
    client.on_connect = configure
    client.on_message = gui.refresh
    client.loop_start()
    gui.run()
    disconnect_from_broker()
