"""check db exists module"""
import os
import psycopg2

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')

def check_db_exists(db):
    """Returns true & connection if db exists else false"""
    try:
        connection = psycopg2.connect(
            database=db,
            user=USER,
            host=HOST,
            password=PASSWORD)
        return True, connection
    except BaseException:
        return False
