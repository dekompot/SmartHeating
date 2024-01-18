import sqlite3
import time


class Database:
    def __init__(self, database_name='temperatures.db'):
        self.name = database_name

    def create_table(self, name, *args):
        table_attr = ''.join([attribute + ' text, ' for attribute in args])[:-2]
        create_command = f" CREATE TABLE {name} ({table_attr})"
        self.execute_with_connection(create_command)

    def insert(self, table, *args):
        insert_attr = ', '.join([f"'{val}'" for val in args])
        insert_command = f"INSERT INTO {table} VALUES ('{time.ctime()}', {insert_attr})"
        self.execute_with_connection(insert_command)

    def get(self, table, expression='1=1'):
        get_command = f"SELECT * FROM {table} WHERE {expression}"
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(get_command)
        return_list = cursor.fetchall()
        cursor.close()
        return return_list

    def get_desired_temperature(self, area_id):
        expression = f'area_id = {area_id}'
        return self.get('desired_temperatures', expression)[0]

    def execute_with_connection(self, sql_command):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()
        cursor.close()

    def insert_temperature(self, sensor_area_id, actual_temperature):
        self.insert('temperatures',sensor_area_id, actual_temperature)

    def insert_valve(self, valve_area_id, valve_invo):
        self.insert('valves',valve_area_id, valve_invo)

    def insert_desired_temperature(self, sensor_area_id, desired_temperature):
        self.insert('desired_temperatures',sensor_area_id, desired_temperature)

    def insert_heating(self):
        self.insert('heating')