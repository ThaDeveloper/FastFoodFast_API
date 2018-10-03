import os
import psycopg2

user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')

def check_db_exists(db):
    try:
        connection = psycopg2.connect(
                        database=db,
                        user=user,
                        host=host,
                        password=password)
        return True, connection
    except BaseException:
        return False
