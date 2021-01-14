from random import randint
from string import ascii_letters, digits
from scripts.db_link import connect_to_database


def gen_unique_code(is_admin):
    conn, cur = connect_to_database()
    letters = ascii_letters + digits
    code = ""
    for i in range(0, 16):
        code += letters[randint(0, len(letters) - 1)]
    cur.execute("INSERT INTO UPC('unique_pass_code','used','admin_token') VALUES (?,?,?);", (code, False, is_admin,))
    conn.commit()


def get_codes():
    conn, cur = connect_to_database()
    data = cur.execute("SELECT unique_pass_code FROM UPC WHERE used = 0;").fetchall()
    t = []
    for i in data:
        t.append(i[0])
    return t