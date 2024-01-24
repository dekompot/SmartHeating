#!/usr/bin/env python3
"""Managing simple GUI for user to change desired temperature in each area."""

"""may present current temperature?"""
"""from db???"""

from createdatabase import create_database
from decode import get_ask_update_id, decode_temperature
import paho.mqtt.client as mqtt
from database_interface import Database
from config import BROKER


def process_actual(client, userdata, message):
    _, area_id, actual_temperature = decode_temperature(message)
    db = Database()
    db.update_actual_temperature(area_id, actual_temperature)
    area_id = get_ask_update_id(message)
    client.publish('update', f"temperature/{area_id}")
    print(f'actual from {area_id}: {actual_temperature}')
    print(f'actual from {area_id}: {db.get_actual_temperature(area_id)}')


def process_ask(client, userdata, message):
    area_id = get_ask_update_id(message)
    db = Database()
    desired_temperature = db.get_desired_temperature(area_id)
    client.publish('desired', f"{area_id}/{desired_temperature}")
    print('ask : ' + str(message.payload.decode("utf-8")))


def config_actual():
    actual_client = mqtt.Client()
    actual_client.connect(BROKER)
    actual_client.on_message = process_actual
    actual_client.subscribe("actual")
    actual_client.loop_start()


def config_ask():
    ask_client = mqtt.Client()
    ask_client.connect(BROKER)
    ask_client.on_message = process_ask
    ask_client.subscribe("ask")
    ask_client.loop_start()


def config():
    create_database()
    config_actual()
    config_ask()
    print('Configuration succeeded')


if __name__ == "__main__":
    config()
    while True:
        pass
