import psycopg2
from psycopg2 import Error

import config
from config import *


connection = psycopg2.connect(user=user_name,
                              password=password_db,
                              database=db_name,
                              host=host_db)


class create:
    try:
        cursor = connection.cursor()

        query_create_first_table = '''CREATE TABLE IF NOT EXISTS all_users(
                id_cod serial4,
                vk_id_user VARCHAR (50) NOT NULL,
                first_name VARCHAR (25) NOT NULL,
                last_name VARCHAR (25) NOT NULL,
                CONSTRAINT all_users_pkey PRIMARY KEY (vk_id_user));'''

        cursor.execute(query_create_first_table)
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    try:
        cursor = connection.cursor()

        query_create_second_table = '''CREATE TABLE IF NOT EXISTS found_users(
                id_cod serial4,
	            vk_id_user varchar(50) NOT NULL,
	            vk_id_found_user varchar(50) NOT NULL,
	            date_time date NOT NULL,
	            CONSTRAINT found_users_fk FOREIGN KEY (vk_id_user) REFERENCES all_users(vk_id_user) ON UPDATE CASCADE);'''

        cursor.execute(query_create_second_table)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

class insert_user:
    cursor = connection.cursor()
    insert_data = (config.user_id_insert, config.first_name_insert, config.last_name_insert)
    cursor.execute("INSERT INTO all_users (vk_id_user, first_name, last_name) VALUES (%s, %s, %s)", insert_data)
    connection.commit()
    count = cursor.rowcount

