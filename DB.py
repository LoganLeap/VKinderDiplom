import psycopg2

from config import host, bd_user, bd_password, bd_database

offset = 0

connection = psycopg2.connect(
    host=host,
    user=bd_user,
    password=bd_password,
    database=bd_database
)

connection.autocommit = True

def create_table_users():
    '''Создание таблицы users'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id serial,
            First_name varchar(50) NOT NULL,
            Last_name varchar(40) NOT NULL,
            VK_id varchar(40) NOT NULL PRIMARY KEY);"""
        )

def create_table_view_users():
    '''Создание таблицы view_users'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS view_users(
            id serial,
            VK_id varchar(50) PRIMARY KEY);"""
        )


def create_db():
    create_table_users()
    create_table_view_users()