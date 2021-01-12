from datetime import datetime

from scripts.db_link import *
from scripts.sci_discover import *


def get_bearer_code():
    return get_discover_bearer_code()


def register_user(email, password, unique_code, f_name, l_name):
    conn, cur = connect_to_database()
    data = cur.execute(f"SELECT * FROM users WHERE email_address = ?;", (email,)).fetchone()
    if not data:
        is_unique_code = cur.execute("SELECT * FROM UPC WHERE unique_pass_code = ?;", (unique_code,)).fetchone()
        if is_unique_code and is_unique_code[2] == 0:
            cur.execute(
                "INSERT INTO users('email_address','first_name','last_name','is_admin','is_active','user_password') "
                "VALUES (?,?,?,?,?,?);", (email, f_name.lower(), l_name.lower(), 0, 1, hash_password(password)))
            conn.commit()
            u_id = cur.execute(f"SELECT user_id FROM users WHERE email_address = ?;", (email,)).fetchone()
            cur.execute("UPDATE UPC SET used = ?, time_of_use = ?, user_id = ? WHERE unique_pass_code = ?;",
                        (True, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), u_id[0], unique_code))
            conn.commit()
            return True
        else:
            return "Sorry that code is incorrect"
    else:
        return "Sorry that email is being used already"


def login(email, password):
    return authenticate(email, password)


def get_auth_token():
    pass
