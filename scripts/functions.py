import jwt

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


def gen_auth_token(secret, user_id):
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    expiry_timestamp = timestamp + 86400
    payload = {
        "issue": timestamp,
        "expiry": expiry_timestamp,
        "id": user_id
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    store_token(token, user_id, timestamp, expiry_timestamp)
    return token


def get_auth_data(token):
    try:
        conn, cur = connect_to_database()
        valid = cur.execute("SELECT * FROM tokens WHERE token = ?;", (token,)).fetchone()
        if valid:
            if bool(valid[5]) is True:
                now = datetime.now()
                timestamp = int(datetime.timestamp(now))
                if timestamp < valid[3]:
                    cur.execute("UPDATE tokens SET expiry_time = ? WHERE token_id = ?;", (timestamp+86400, valid[0],))
                    return True, -1
                else:
                    update_token(valid[0])
                    return True, 1
    except Exception as e:
        print("Something went wrong: " + e)
    return False, -1

def get_auth_token(secret, u_id):
    try:
        conn, cur = connect_to_database()
        data = cur.execute("SELECT * FROM tokens WHERE user_id = ?;", (u_id,)).fetchall()
        if data:
            last = data[-1]
            now = datetime.now()
            timestamp = int(datetime.timestamp(now))
            if timestamp > last[3]:
                cur.execute("UPDATE tokens SET active = 0 WHERE token_id = ?;", (last[0],))
                conn.commit()
                return gen_auth_token(secret, u_id)
            else:
                cur.execute("UPDATE tokens SET expiry_time = ? WHERE token_id = ?;", (timestamp+86400, last[0]))
                conn.commit()
        else:
            return gen_auth_token(secret, u_id)
    except Exception as e:
        print(e)
