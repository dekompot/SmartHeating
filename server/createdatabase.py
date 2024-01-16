#!/usr/bin/env python3

import sqlite3
import time
import os


def create_database():
    if os.path.exists("temperatures.db"):
        os.remove("temperatures.db")
        print("An old database removed.")
    connection = sqlite3.connect("temperatures.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE temperatures_log (
        log_time text,
        id text,
        value text
    )""")
    connection.commit()
    connection.close()
    print("The new database created.")


if __name__ == "__main__":
    create_database()
