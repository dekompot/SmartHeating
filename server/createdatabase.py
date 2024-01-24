#!/usr/bin/env python3

import os
from database_interface import Database
from config import NUMBER_OF_AREAS, DEFAULT_TEMPERATURE


def create_database():
    if os.path.exists("temperatures.db"):
        os.remove("temperatures.db")
        print("An old database removed.")

    db = Database("temperatures.db")
    db.create_table('Temperatures', 'areaId', 'actualTemperature',
                    'actualTemperatureTimestamp', 'desiredTemperature',
                    'desiredTemperatureTimestamp', )
    db.create_table('Heating', 'state', 'changeTimestamp')
    for i in range(NUMBER_OF_AREAS):
        db.init_temperature(i, DEFAULT_TEMPERATURE)
    db.init_heating()
    print("The new database created.")


if __name__ == "__main__":
    create_database()

