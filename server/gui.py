#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""
from database_interface import Database

"""may present current temperature?"""
"""from db???"""

import paho.mqtt.client as mqtt
import tkinter
from config import NUMBER_OF_AREAS, DEFAULT_TEMPERATURE, BROKER


class GUI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.db = Database()
        self.client = mqtt.Client()
        self.number_of_areas = NUMBER_OF_AREAS
        self.desired_temperatures = [tkinter.IntVar(self.window, self.db.get_desired_temperature(i))
                                     for i in range(NUMBER_OF_AREAS)]
        self.actual_temperatures = [tkinter.IntVar(self.window, self.db.get_actual_temperature(i)) for i in
                                    range(NUMBER_OF_AREAS)]
        self.heating_state = tkinter.StringVar(self.window, value=self.db.get_state())

    def run(self):
        self.setup()
        self.window.mainloop()

    def connect_to_broker(self):
        self.client.connect(BROKER)
        self.client.on_connect = self.configure
        self.client.on_message = self.refresh
        self.client.loop_start()

    def setup(self):
        self.window.title("Smart Heating")
        label_desired = tkinter.Label(self.window, text="Temperature control panel")
        label_desired.grid(row=0, columnspan=NUMBER_OF_AREAS)

        label_actual = tkinter.Label(self.window, text="Actual")
        label_actual.grid(row=0, column=2)

        for i in range(NUMBER_OF_AREAS):
            label = tkinter.Label(self.window, text=f"area {i} : ")
            label.grid(row=i + 1, column=0)
            spinbox = tkinter.Spinbox(self.window, from_=0, to=30,
                                      textvariable=self.desired_temperatures[i], command=lambda i=i: self.update(i))
            spinbox.grid(row=i + 1, column=1)
            label = tkinter.Label(self.window, textvariable=self.actual_temperatures[i])
            label.grid(row=i + 1, column=2)

        exit_button = tkinter.Button(self.window, text="Exit", command=self.window.quit)
        exit_button.grid(row=i + 2, column=2)

        heating_state_label = tkinter.Label(self.window, textvariable=self.heating_state)
        heating_state_label.grid(row=i + 2, column=1)
        heating_state_field = tkinter.Label(self.window, text='Heating')
        heating_state_field.grid(row=i + 2, column=0)
        # kontrolka kiedy grzeje

    def update(self, index):
        desired_temperature = self.desired_temperatures[index].get()
        print(desired_temperature)
        # process_desired_temperature(index, desired_temperature)
        self.client.publish('ask', f'desired/{index}')
        self.db.update_desired_temperature(index, desired_temperature)

    def refresh(self, client, userdata, message):
        print(f"GUI {message.payload.decode('utf-8')}")
        for area_id in range(NUMBER_OF_AREAS):
            self.actual_temperatures[area_id].set(self.db.get_actual_temperature(area_id))
        self.heating_state.set(self.db.get_state())

    def disconnect_from_broker(self):
        self.client.loop_stop()
        self.client.disconnect()

    def configure(self, client, userdata, flags, rc):
        self.client.subscribe(f"update")


if __name__ == "__main__":
    gui = GUI()
    gui.connect_to_broker()
    gui.run()
    gui.disconnect_from_broker()
