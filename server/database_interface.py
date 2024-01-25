from datetime import datetime
import sqlite3


class Database:
    def __init__(self, database_name='temperatures.db'):
        self.name = database_name

    def create_table(self, name, *args):
        table_attr = ''.join([attribute + ' text, ' for attribute in args])[:-2]
        create_command = f" CREATE TABLE {name} ({table_attr})"
        self.execute_with_connection(create_command)

    def insert(self, table, *args):
        insert_attr = ''.join([f"'{val}', " for val in args])[:-2]
        insert_command = f"INSERT INTO {table} VALUES ({insert_attr})"
        self.execute_with_connection(insert_command)

    def update_temperature(self, area_id, attribute, value):
        insert_command = (f"UPDATE Temperatures SET {attribute} = '{value}', "
                          f"{attribute}Timestamp='{get_timestamp()}' "
                          f"WHERE areaId={area_id}")
        self.execute_with_connection(insert_command)

    def get(self, table, attribute, expression='1=1'):
        get_command = f"SELECT {attribute} FROM {table} WHERE {expression}"
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(get_command)
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def execute_with_connection(self, sql_command):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()
        connection.close()

    def get_number_of_unsatisfied(self):
        return self.get('Temperatures', 'COUNT(*)', 'CAST(desiredTemperature as decimal)'
                                                    '>CAST(actualTemperature as decimal)')

    def get_actual_temperature(self, area_id):
        return self.get('Temperatures', 'actualTemperature', f'areaId={area_id}')

    def get_desired_temperature(self, area_id):
        return self.get('Temperatures', 'desiredTemperature', f'areaId={area_id}')

    def get_state(self):
        return self.get('Heating', 'state')

    def update_actual_temperature(self, area_id, actual_temperature):
        self.update_temperature(area_id, 'actualTemperature', actual_temperature)

    def update_desired_temperature(self, area_id, desired_temperature):
        self.update_temperature(area_id, 'desiredTemperature', desired_temperature)

    def update_state(self, new_state):
        insert_command = (f"UPDATE Heating SET state = '{new_state}'")

        self.execute_with_connection(insert_command)

    def init_temperature(self, areaId, defaultTemperature):
        self.insert('Temperatures', areaId, defaultTemperature, get_timestamp(),
                    defaultTemperature, get_timestamp())

    def init_heating(self):
        self.insert('Heating', 'stop', get_timestamp())


def get_timestamp():
    return datetime.now()
