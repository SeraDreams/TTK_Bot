from typing import Tuple

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
def exec_with_resp(query: str, printing: bool = False) -> Tuple[bool, list]:
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
name VARCHAR(50) NOT NULL UNIQUE,
category category NOT NULL);'''
    exec_without_resp(query=create_query2, printing=False)

    # создание таблицы пассажира
    create_query3 = '''
CREATE TABLE IF NOT EXISTS rzd_user (
id SERIAL NOT NULL PRIMARY KEY,
passport VARCHAR(10) NOT NULL UNIQUE,
ticket_num VARCHAR(15) NOT NULL UNIQUE,
train VARCHAR(10) NOT NULL,
num_carriage INT NOT NULL,
type_carriage VARCHAR(10) NOT NULL,
place INT NOT NULL);'''
    exec_without_resp(query=create_query3, printing=False)

    # создание таблицы ТГ юзера
    create_query4 = '''CREATE TABLE IF NOT EXISTS tg_user (
id SERIAL NOT NULL PRIMARY KEY,
tg_id BIGINT NOT NULL UNIQUE,
rzd_user VARCHAR(10) NOT NULL UNIQUE,
FOREIGN KEY (rzd_user) REFERENCES rzd_user(passport) ON DELETE CASCADE);'''
    exec_without_resp(query=create_query4, printing=False)

    # создание таблицы истории покупок
    create_query4 = '''CREATE TABLE IF NOT EXISTS pay_history (
id SERIAL NOT NULL PRIMARY KEY,
customer INT NOT NULL,
product INT NOT NULL,
datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
FOREIGN KEY (customer) REFERENCES tg_user(id) ON DELETE CASCADE,
FOREIGN KEY (product) REFERENCES product(id) ON DELETE CASCADE);'''
    exec_without_resp(query=create_query4, printing=True)


# добавление пассажира в БД
def add_rzd_user(passport: str, ticket_num: str, train: str, num_carriage: int, type_carriage: str, place: int) -> bool:
    # создание SQL запроса
    insert_query = f'''INSERT INTO rzd_user (passport, ticket_num, train, num_carriage, type_carriage, place)
VALUES ('{passport}', '{ticket_num}', '{train}', {num_carriage}, '{type_carriage}', {place});'''

    alright = exec_without_resp(query=insert_query, printing=False)
    return alright


# добавление ТГ юзера в БД
def add_tg_user(tg_id: int, rzd_user: str) -> bool:
    # создание SQL запроса
    insert_query = f'''INSERT INTO tg_user (tg_id, rzd_user)
VALUES ({tg_id}, {rzd_user});'''

    alright = exec_without_resp(query=insert_query, printing=False)
    return alright


# добавление продукта в БД
def add_product(name: str, category: str) -> bool:
    # создание SQL запроса
    insert_query = f'''INSERT INTO product (name, category)
VALUES ('{name}', '{category}');'''

    alright = exec_without_resp(query=insert_query, printing=False)
    return alright


# добавление покупки в историю
def add_pay_to_history(customer: int, product: int) -> bool:
    # создание SQL запроса
    insert_query = f'''INSERT INTO pay_history (customer, product)
VALUES ({customer}, {product});'''

    alright = exec_without_resp(query=insert_query, printing=False)
    return alright


# обновление информации о поезде пассажира
def update_rzd_user_train(passport: str, ticket_num: str, train: str, num_carriage: int, type_carriage: str, place: int) -> bool:
    # создание SQL запроса
    update_query = f'''UPDATE rzd_user SET
ticket_num = '{ticket_num}',
train = '{train}',
num_carriage = {num_carriage},
type_carriage = '{type_carriage}',
place = {place} WHERE passport = '{passport}';'''

    alright = exec_without_resp(query=update_query, printing=True)
    return alright


# получение tg_id юзера
def check_tg_user(tg_id: int) -> bool:
    # создание SQL запроса
    select_query = f'''SELECT * FROM tg_user WHERE tg_id = {tg_id};'''

    alright, found = exec_with_resp(query=select_query, printing=False)

    # print(found)
    if found:
        return True
    return False


# получение продукта из БД
def get_product(table_id: int) -> bool:
    # создание SQL запроса
    select_query = f'''SELECT name, category FROM product WHERE id = {table_id};'''

    alright, found = exec_with_resp(query=select_query, printing=False)

    if found:
        res = {'name': found[0][0], 'category': found[0][1]}
        return res
    else:
        return None


# получение инфы о пассажире по его паспорту или номеру билета
def get_passenger_info(passport: str = None, ticket_num: str = None) -> dict | None:
    # создание SQL запроса

    if passport:
        select_query = f'''SELECT * FROM rzd_user WHERE passport = '{passport}';'''
    else:
        select_query = f'''SELECT * FROM rzd_user WHERE ticket_num = '{ticket_num}';'''

    alright, found = exec_with_resp(query=select_query, printing=False)

    if found:
        res = {
            'id': found[0][0],
            'passport': found[0][1],
            'ticket_num': found[0][2],
            'train': found[0][3],
            'num_carriage': found[0][4],
            'type_carriage': found[0][5],
            'place': found[0][5]
        }
        return res
    else:
        return None


if __name__ == '__main__':
    # add_rzd_user(
    #     passport='9876543210',
    #     ticket_num='89898989898989',
    #     train='13F',
    #     num_carriage=32,
    #     type_carriage='1R',
    #     place=23,
    # )

    # # passport - img_1.png
    # # ticket - photo_2023-10-20_14-09-59 (2).jpg
    add_rzd_user(
        passport='1104000000',
        ticket_num='31633461289261',
        train='131H',
        num_carriage=26,
        type_carriage='2H',
        place=37,
    )

    # # passport - img_5.png
    # # ticket - img_4.png
    # add_rzd_user(
    #     passport='6019767612',
    #     ticket_num='78994443225102',
    #     train='17R',
    #     num_carriage=32,
    #     type_carriage='2E',
    #     place=8,
    # )
