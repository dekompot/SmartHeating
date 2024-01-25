from createdatabase import create_database
from decode import get_ask_update_id, decode_temperature
import paho.mqtt.client as mqtt
from database_interface import Database
from config import BROKER, DEBOUNCE_VALUE


def check_heating(changed_temperature_area_id):
    db = Database()
    actual_temperature = float(db.get_actual_temperature(changed_temperature_area_id))
    desired_temperature = float(db.get_desired_temperature(changed_temperature_area_id))
    current_heating_state = db.get_state()
    print(actual_temperature, desired_temperature, current_heating_state)
    if actual_temperature < desired_temperature - DEBOUNCE_VALUE and current_heating_state == "stop":
        db.update_state("start")
        send_state("start")
    elif (actual_temperature > desired_temperature + DEBOUNCE_VALUE
          and current_heating_state == "start" and can_stop()):
        db.update_state("stop")
        send_state("stop")


def send_state(state):
    heating_client = mqtt.Client()
    heating_client.connect(BROKER)
    heating_client.publish('heating', state)


def can_stop():
    db = Database()
    print(db.get_number_of_unsatisfied())
    return int(db.get_number_of_unsatisfied()) == 0


def process_actual(client, userdata, message):
    _, area_id, actual_temperature = decode_temperature(message)
    db = Database()
    print(f'pre from {area_id}: {db.get_actual_temperature(area_id)}')
    db.update_actual_temperature(area_id, actual_temperature)
    client.publish('update', f"temperature/{area_id}")
    check_heating(area_id)
    print(f'actual from {area_id}: {actual_temperature}')


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
