"""Databse setup script"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .check_if_db import check_db_exists


class Database:
    """connecting to db, creating and droping database tables"""

    def __init__(self):
        """Initialize by setting up and connecting to database"""
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        self.host = os.getenv('HOST')
        con = psycopg2.connect(dbname=os.getenv('DEFAULT_DB'),
                               user=self.user, host=self.host,
                               password=self.password)
        #All other transactions are stopped and no commit() or rollback() is required
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        if os.getenv('FLASK_ENV') == 'development':
            self.database = os.getenv("DEV_DATABASE")
            db_connected = check_db_exists(self.database)
            if db_connected[0]:
                self.connection = db_connected[1]
            else:
                cur.execute("CREATE DATABASE {};".format(self.database))
        elif os.getenv('FLASK_ENV') == 'testing':
            self.database = os.getenv("TEST_DATABASE")
            db_connected = check_db_exists(self.database)
            if db_connected[0]:
                self.connection = db_connected[1]
            else:
                cur.execute("CREATE DATABASE {};".format(self.database))
        elif os.getenv('FLASK_ENV') == 'production':
            self.database = os.getenv("DATABASE")
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                host=self.host,
                password=self.password)
        except BaseException:
            print("Can't connect to database")

    @staticmethod
    def tables():
        """List of tables to be created"""
        queries = [
            'CREATE TABLE IF NOT EXISTS users (\
                    id SERIAL PRIMARY KEY,\
                    first_name VARCHAR(30) NOT NULL,\
                    last_name VARCHAR(30) NOT NULL,\
                    username VARCHAR(30) UNIQUE NOT NULL,\
                    email VARCHAR(90) NOT NULL,\
                    password VARCHAR(200) NOT NULL,\
                    admin bool,\
                    created_at TIMESTAMP\
                    )',


            'CREATE TABLE IF NOT EXISTS categories(\
                    cat_id SERIAL PRIMARY KEY,\
                    name VARCHAR(50))\
            ',

            'CREATE TABLE IF NOT EXISTS menu (\
                    item_id SERIAL PRIMARY KEY,\
                    name VARCHAR(70) NOT NULL,\
                    price numeric(10, 2) NOT NULL,\
                    category VARCHAR(200),\
                    image VARCHAR(250) NOT NULL,\
                    created_at TIMESTAMP,\
                    updated_at TIMESTAMP\
                    )',

            'CREATE TABLE IF NOT EXISTS orders (\
                    order_id SERIAL PRIMARY KEY,\
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,\
                    items VARCHAR(250) NOT NULL,\
                    total numeric(10, 2) NOT NULL,\
                    status VARCHAR(10) NOT NULL,\
                    created_at TIMESTAMP,\
                    updated_at TIMESTAMP\
                    )',

            'CREATE TABLE IF NOT EXISTS tokens (\
                    token_id SERIAL PRIMARY KEY,\
                    user_id VARCHAR REFERENCES users(username) ON DELETE CASCADE,\
                    token VARCHAR\
                    )',
            'CREATE TABLE IF NOT EXISTS blacklist (\
                    token_id SERIAL PRIMARY KEY,\
                    user_id VARCHAR REFERENCES users(username) ON DELETE CASCADE,\
                    token VARCHAR\
                    )'
        ]
        return queries

    def cursor(self):
        """cursor method for executing queries
        RealDictCursor - A cursor that uses a real python dict as the base type for rows."""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        return cur

    def commit(self):
        """for saving changes permanently to db"""
        self.connection.commit()

    def create_tables(self):
        """create all tables else return executuon error"""
        cur = self.cursor()
        try:
            for table in self.tables():
                cur.execute(table)
                self.commit()
            print('All tables created sucessfully')
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def drop_tables(self):
        """drop tables else return exection error"""
        cur = self.cursor()
        table_drops = ["DELETE FROM users CASCADE",
                       "DELETE FROM categories CASCADE",
                       "DELETE FROM menu",
                       "DELETE FROM orders",
                       "DELETE FROM tokens",
                       "DELETE FROM blacklist",
                       "ALTER SEQUENCE users_id_seq RESTART WITH 1;",
                       "ALTER SEQUENCE categories_cat_id_seq RESTART WITH 1;",
                       "ALTER SEQUENCE menu_item_id_seq RESTART WITH 1;"
                       "ALTER SEQUENCE orders_order_id_seq RESTART WITH 1;"
                       "ALTER SEQUENCE tokens_token_id_seq RESTART WITH 1;"
                       "ALTER SEQUENCE blacklist_token_id_seq RESTART WITH 1;"
                       ]

        try:
            for table in table_drops:
                cur.execute(table)
                self.connection.commit()
            print("All tables dropped successfully")
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
