import binascii
import hashlib
import logging
import os
import sqlite3 as sql

from datetime import datetime


def connect_to_database():
    try:
        conn = sql.connect("database.db")
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Something went wrong.")
        logging.debug("Error message: ", e)


def authenticate(email, password):
    conn, cursor = connect_to_database()
    result = cursor.execute(f"SELECT * FROM users WHERE email_address = ?;", (email,)).fetchall()
    if result:
        if check_password(password, result[0][6]):
            if result[0][5]:
                if result[0][4]:
                    return True, True, result[0][0]
                else:
                    return True, False, result[0][0]
            else:
                return False, "Problem signing in. Please contact a admin", -1

    return False, "Wrong Email or Password try again", -1


def store_token(token, u_id, issue, expire):
    conn, cur = connect_to_database()
    cur.execute("INSERT INTO tokens('user_id','issue_time','expiry_time','token','active') VALUES (?,?,?,?,?)",
                (u_id, issue, expire, token, True,))
    conn.commit()


def update_token(token_id):
    conn, cur = connect_to_database()
    cur.execute("UPDATE tokens SET active = 0 WHERE token_id = ?;", (token_id,))
    conn.commit()


def save_bearer_token(data):
    conn, cur = connect_to_database()
    expiry_timestamp = get_time_now() + data["expires_in"]
    cur.execute(
        "INSERT INTO sci_tokens('token','token_type','refresh_token','expiry_time', 'permissions', 'number_of_use') VALUES (?,?,?,?,?,?)",
        (data["access_token"], data["token_type"], data["refresh_token"], expiry_timestamp, data["scope"], 0,))
    conn.commit()


def check_for_bearer_token():
    conn, cur = connect_to_database()
    data = cur.execute("SELECT * FROM sci_tokens ORDER BY token_id DESC LIMIT 1;").fetchone()
    if data:
        if get_time_now() < data[4]:
            return data[1]
    return False


def use_bearer_token():
    """
    Adds one to number of use in token
    :return:
    """
    conn, cur = connect_to_database()
    cur.execute(
        "UPDATE sci_tokens SET number_of_use = number_of_use + 1 WHERE token_id = (SELECT token_id FROM sci_tokens ORDER BY token_id DESC LIMIT 1);")
    conn.commit()


def get_user_data(u_id):
    conn, cur = connect_to_database()
    data = cur.execute("SELECT * FROM users WHERE user_id = ?;", (u_id,)).fetchone()
    return data


def get_user_id(token):
    conn, cur = connect_to_database()
    return cur.execute("SELECT user_id FROM tokens WHERE token = ?;", (token,)).fetchone()[0]


def check_password(user_password, stored_password):
    """
    A function that checks to see if the user's password is correct or not
    :param user_password: The password the user enters
    :param stored_password: The password that userPassword is being checked against
    :return: True or False
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pass_hash = hashlib.pbkdf2_hmac('sha512', user_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pass_hash = binascii.hexlify(pass_hash).decode('ascii')
    return pass_hash == stored_password


def hash_password(password):
    """
    A function that hashes a password the user enters
    :param password: The password the user enters
    :return: Hashed version of the password
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pass_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pass_hash = binascii.hexlify(pass_hash)
    return (salt + pass_hash).decode('ascii')


def get_time_now():
    now = datetime.now()
    return int(datetime.timestamp(now))
