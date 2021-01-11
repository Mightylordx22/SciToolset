from random import randint
from db_link import connect_to_database


def gen_unique_code():
    conn, cur = connect_to_database()
    LETTERS = [chr(i) for i in range(33, 126)]
    code = ""
    for i in range(0, 16):
        code += LETTERS[randint(0, len(LETTERS) - 1)]
    print(code)