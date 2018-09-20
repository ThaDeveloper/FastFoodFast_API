import psycopg2
import os
from psycopg2.extras import RealDictCursor


class Database:
    '''constructor to set up database connection'''

    def __init__(self):
        self.database = os.getenv('DEV_DATABASE')
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        self.host = os.getenv('HOST')
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                host=self.host,
                password=self.password)
        except:
            print("Can't connet to database")
            
    def tables(self):
    
        queries = [
            'CREATE TABLE IF NOT EXISTS users (\
                    id SERIAL PRIMARY KEY,\
                    first_name VARCHAR(30),\
                    last_name VARCHAR(30),\
                    username VARCHAR(30),\
                    email VARCHAR(90),\
                    password VARCHAR(90),\
                    admin bool\
                    )',

            
            'CREATE TABLE IF NOT EXISTS categories(\
                    cat_id SERIAL PRIMARY KEY,\
                    name VARCHAR(50))\
            ',

            'CREATE TABLE IF NOT EXISTS menu (\
                    item_id SERIAL PRIMARY KEY,\
                    name VARCHAR(70),\
                    price DECIMAL(10, 2),\
                    cat_id INTEGER REFERENCES categories(cat_id) ON DELETE CASCADE,\
                    image VARCHAR(250),\
                    created_at TIMESTAMP,\
                    updated_at TIMESTAMP\
                    )',

            'CREATE TABLE IF NOT EXISTS orders (\
                    order_id SERIAL PRIMARY KEY,\
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,\
                    items VARCHAR(250),\
                    total DECIMAL(10, 2),\
                    status VARCHAR(10),\
                    created_at TIMESTAMP,\
                    updated_at TIMESTAMP\
                    )',

            'CREATE TABLE IF NOT EXISTS tokens (\
                    token_id SERIAL PRIMARY KEY,\
                    token VARCHAR(200)\
                    )',
            'CREATE TABLE IF NOT EXISTS blacklist (\
                    token_id SERIAL PRIMARY KEY,\
                    token VARCHAR(200)\
                    )'
        ]
        return queries
    
    def cursor(self):
        '''cursor method for executing queries
        RealDictCursor - A cursor that uses a real dict as the base type for rows.'''
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        return cur
    
    def commit(self):
        '''save changes to db'''
        self.connection.commit()
    
    def create_tables(self):
        cur = self.connection.cursor()
        for table in self.tables():
            cur.execute(table)
            self.commit()
        print('All tables created sucessfully')

db = Database()
db.create_tables()