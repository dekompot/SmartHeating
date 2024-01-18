"""Interface in-between receiving and sending messages. And sending all decisions to heating unit and valves."""
"""communicates with DB?"""
from paho.mqtt import client as mqtt
from server.decode import decode_with_id
from server.config import BROKER
from server.database_interface import Database


def heat():
    client = mqtt.Client()
    client.connect(BROKER)
    client.publish("heating", "heat")
    client.disconnect()


def process_temperature(sensor_area_id, actual_temperature):
    db = Database()
    db.insert_temperature(sensor_area_id, actual_temperature)
    desired_temperature = db.get_desired_temperature(sensor_area_id)
    if actual_temperature < desired_temperature:
        heat()


def process_valve(valve_area_id, value):
    Database().insert_valve(valve_area_id,value)

def process_desired_temperature(area_id, value):
    Database().insert_desired_temperature(area_id,value)

def get_temperature(message):
    _, area_id, value = decode_with_id(message)

def process_message(message):
    topic, sensor_area_id, value = decode_with_id(message)
    if topic == 'temperature':
        process_temperature(sensor_area_id, value)
    elif topic == 'valve' and sensor_area_id:
        process_valve(sensor_area_id, value)
