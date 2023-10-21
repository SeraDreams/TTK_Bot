import os
import hashlib

from psycopg2 import Binary
from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError

from db.secure_data import HOST, PORT, DB_USER_NAME, DB_USER_PASS, DATABASE


# делаем соединение с БД через sqlalchemy
SQL_ENGINE = create_engine(f'postgresql+psycopg2://{DB_USER_NAME}:{DB_USER_PASS}@{HOST}:{PORT}/{DATABASE}')
SQL_CONNECTION = SQL_ENGINE.connect()


# выполнение SQL запроса без отдачи
def exec_without_resp(query: str, printing: bool = False) -> bool:
    alright = False

    # выполняем SQL запрос
    try:
        SQL_CONNECTION.execute(sql_text(query))
        # применяем изменения
        SQL_CONNECTION.commit()

        alright = True
        # выводим, что всё ок
        if printing:
            print(f'Query "{query.split()[0]}" OK!')

    # если произошла ошибка
    except SQLAlchemyError as error:
        # отменяем транзакцию
        SQL_CONNECTION.rollback()
        # выводим ошибку
        if printing:
            print(f'''You've got error in file "db_connect.py" in query "{query.split()[0]}": {error}''')

    return alright


# выполнение SQL запроса с отдачей
def exec_with_resp(query: str, printing: bool = False) -> (bool, list):
    alright = False
    result = []

    # выполняем SQL запрос
    try:
        gotten_info = SQL_CONNECTION.execute(sql_text(query))
        result = gotten_info.fetchall()
        alright = True

        # выводим, что всё ок
        if printing:
            print(f'Query "{query.split()[0]}" OK!')

    # если произошла ошибка
    except SQLAlchemyError as error:
        # выводим ошибку
        if printing:
            print(f'''You've got error in file "db_connect.py" in query "{query.split()[0]}": {error}''')

    return alright, result


# перед работой приложения готовим таблицы БД для работы с ними
def prepare_tables():
    # создание нового типа для поля category таблицы product
    create_query1 = "CREATE TYPE category AS ENUM ('food', 'drink');"
    exec_without_resp(query=create_query1, printing=False)

    # создание таблицы продуктов
    create_query2 = '''CREATE TABLE IF NOT EXISTS product (
id SERIAL NOT NULL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
category category NOT NULL);'''
    exec_without_resp(query=create_query2, printing=False)

    # создание таблицы пассажира
    create_query3 = '''
CREATE TABLE IF NOT EXISTS rzd_user (
id SERIAL NOT NULL PRIMARY KEY,
passport BYTEA NOT NULL,
ticket_num BYTEA NOT NULL,
train VARCHAR(10) NOT NULL,
num_carriage INT NOT NULL,
type_carriage VARCHAR(10) NOT NULL,
place INT NOT NULL,
salt BYTEA NOT NULL);'''
    exec_without_resp(query=create_query3, printing=False)

    # создание таблицы ТГ юзера
    create_query4 = '''CREATE TABLE IF NOT EXISTS tg_user (
id SERIAL NOT NULL PRIMARY KEY,
tg_id BIGINT NOT NULL,
rzd_user INT NOT NULL,
FOREIGN KEY (rzd_user) REFERENCES rzd_user(id) ON DELETE CASCADE);'''
    exec_without_resp(query=create_query4, printing=False)


# добавление пассажира в БД
def add_rzd_user(passport: int, ticket_num: int, train: str, num_carriage: int, type_carriage: str, place: int) -> bool:
    # создание соли для хеширования
    salt = os.urandom(16)
    # хеширование серии-номера паспорта
    hash_passport = hashlib.pbkdf2_hmac(
        'sha256',
        str(passport).encode('utf-8'),
        salt,
        100000
    )
    # хеширование номера билета
    hash_ticket_num = hashlib.pbkdf2_hmac(
        'sha256',
        str(ticket_num).encode('utf-8'),
        salt,
        100000
    )

    insert_query = f'''INSERT INTO rzd_user (passport, ticket_num, train, num_carriage, type_carriage, place, salt)
VALUES ({Binary(hash_passport)}, {Binary(hash_ticket_num)}, '{train}', {num_carriage}, '{type_carriage}', {place}, {Binary(salt)});'''

    print(insert_query)
    result = exec_without_resp(query=insert_query, printing=True)
    return result


if __name__ == '__main__':
    # prepare_tables()
    # add_rzd_user(
    #     passport=5432154321,
    #     ticket_num=90129012901290,
    #     train='31EG',
    #     num_carriage=5,
    #     type_carriage='4H',
    #     place=11,
    # )
    pass
