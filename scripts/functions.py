from scripts.db_link import *
from scripts.sci_discover import *


def get_bearer_code():
    return get_discover_bearer_code()


def register_user(email, password, unique_code, f_name, l_name):
    data = data_query(f"SELECT * FROM users WHERE email_address = '{email}';")
    if not data:
        is_unique_code = data_query(f"SELECT * FROM UPC WHERE unique_pass_code = '{unique_code}';")
        if is_unique_code and is_unique_code[0][2] == 0:
            conn, cur = connect_to_database()
            cur.execute(
                "INSERT INTO users('email_address','first_name','last_name','is_admin','is_active','user_password') "
                "VALUES (?,?,?,?,?,?);", (email, f_name.lower(), l_name.lower(), 0, 1, hash_password(password)))
            conn.commit()
            u_id = data_query(f"SELECT user_id FROM users WHERE email_address = '{email}';")
            cur.execute("UPDATE UPC SET used = ?, time_of_use = ?, user_id = ? WHERE unique_pass_code = ?;",
                        (True, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), u_id[0][0], unique_code))
            conn.commit()
            return True
        else:
            return "Sorry that code is incorrect"
    else:
        return "Sorry that email is being used already"


def login(email, password):
    if authenticate(email, password):
        return True
    else:
        return False
