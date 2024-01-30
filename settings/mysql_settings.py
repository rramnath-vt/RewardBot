import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector


def init():
    global connection

    load_dotenv()

    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USERNAME"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=os.getenv("MYSQL_PORT"),
        autocommit=True
    )

    try:
        if connection.is_connected():
            cursor = connection.cursor()
        cursor.execute("select @@version ")
        version = cursor.fetchone()
        if version:
            print('Running version: ', version)
        else:
            print('Not connected.')

    except Error as e:
        print("Error while connecting to MySQL", e)
        connection.close()
