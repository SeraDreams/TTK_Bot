from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError

from db.constants import BASE_DIR
from db.secure_data import HOST, PORT, DB_USER_NAME, DB_USER_PASS, DATABASE


# делаем соединение с БД через sqlalchemy
SQL_ENGINE = create_engine(f'postgresql+psycopg2://{DB_USER_NAME}:{DB_USER_PASS}@{HOST}:{PORT}/{DATABASE}')
SQL_CONNECTION = SQL_ENGINE.connect()


# выполнение SQL запроса без отдачи
def exec_without_resp(query: str, need_commit: bool = False, printing: bool = False) -> bool:
    alright = False

    # выполняем SQL запрос
    try:
        SQL_CONNECTION.execute(sql_text(query))

        if need_commit:
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


# перед работой приложения готовим БД для работы с ним
def prepare_tables():
    # создание нового типа для поля category таблицы product
    create_query1 = "CREATE TYPE category AS ENUM ('food', 'drink');"
    exec_without_resp(query=create_query1, need_commit=True, printing=False)

    # создание таблицы продуктов
    create_query2 = '''CREATE TABLE IF NOT EXISTS product (
id SERIAL NOT NULL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
category category NOT NULL);'''
    exec_without_resp(query=create_query2, need_commit=True, printing=False)

    # создание таблицы пассажира
    create_query3 = '''
CREATE TABLE IF NOT EXISTS rzd_user (
id SERIAL NOT NULL PRIMARY KEY,
passport BYTEA NOT NULL,
ticket_num BYTEA NOT NULL,
train VARCHAR(10) NOT NULL,
num_carriage INT NOT NULL,
type_carriage VARCHAR(10) NOT NULL,
place INT NOT NULL);'''
    exec_without_resp(query=create_query3, need_commit=True, printing=False)

    # создание таблицы ТГ юзера
    create_query4 = '''CREATE TABLE IF NOT EXISTS tg_user (
id SERIAL NOT NULL PRIMARY KEY,
tg_id BIGINT NOT NULL,
rzd_user INT NOT NULL,
FOREIGN KEY (rzd_user) REFERENCES rzd_user(id) ON DELETE CASCADE);'''
    exec_without_resp(query=create_query4, need_commit=True, printing=False)


if __name__ == '__main__':
    # prepare_tables()
    pass
