from datetime import datetime
import jwt

from scripts.db_link import connect_to_database, store_token, update_token, get_user_data


def gen_auth_token(secret, user_id):
    timestamp = get_time_now()
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
                timestamp = get_time_now()
                if timestamp < valid[3]:
                    cur.execute("UPDATE tokens SET expiry_time = ? WHERE token_id = ?;", (timestamp + 86400, valid[0],))
                    user = get_user_data(valid[1])

                    if bool(user[4]) is True:
                        return True, 2

                    return True, 1
                else:
                    update_token(valid[0])
                    return True, -1
    except Exception as e:
        print("Something went wrong: " + e)
    return False, -1


def get_auth_token(secret, u_id):
    try:
        conn, cur = connect_to_database()
        data = cur.execute("SELECT * FROM tokens WHERE user_id = ?;", (u_id,)).fetchall()
        if data:
            last = data[-1]
            timestamp = get_time_now()
            if timestamp > last[3]:
                cur.execute("UPDATE tokens SET active = 0 WHERE token_id = ?;", (last[0],))
                conn.commit()
                return gen_auth_token(secret, u_id)
            else:
                cur.execute("UPDATE tokens SET expiry_time = ? WHERE token_id = ?;", (timestamp + 86400, last[0]))
                conn.commit()
                return last[4]
        else:
            return gen_auth_token(secret, u_id)
    except Exception as e:
        print(e)


def get_time_now():
    now = datetime.now()
    return int(datetime.timestamp(now))
