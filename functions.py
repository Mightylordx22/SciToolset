import sqlite3 as sql
from random import randint


def connect_to_database():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    return conn, cur


def gen_unique_code():
    conn, cur = connect_to_database()
    LETTERS = [chr(i) for i in range(33, 126)]
    code = ""
    for i in range(0, 16):
        code += LETTERS[randint(0, len(LETTERS) - 1)]
    print(code)


def get_bearer_code():
    return "hi"
