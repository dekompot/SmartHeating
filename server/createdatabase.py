#!/usr/bin/env python3

import sqlite3
import os
from database_interface import Database


def create_database():
    if os.path.exists("temperatures.db"):
        os.remove("temperatures.db")
        print("An old database removed.")or()

    db = Database("temperatures.db")
    db.create_table('actual_temperatures', 'log_time', 'area_id', 'value')
    db.create_table('desired_temperatures', 'log_time', 'area_id', 'value')
    db.create_table('valves', 'log_time', 'area_id', 'value')
    db.create_table('heating', 'log_time', 'value')
    print("The new database created.")


if __name__ == "__main__":
    create_database()

    