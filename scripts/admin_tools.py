from random import randint

from scripts.db_link import connect_to_database


def gen_unique_code():
    conn, cur = connect_to_database()
    letters = [chr(i) for i in range(33, 126)]
    code = ""
    for i in range(0, 16):
        code += letters[randint(0, len(letters) - 1)]
    cur.execute("INSERT INTO UPC('unique_pass_code','used','admin_token') VALUES (?,?,?);", (code, False, 0,))
    conn.commit()
