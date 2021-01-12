import binascii
import hashlib
import logging
import os
import sqlite3 as sql


def connect_to_database():
    try:
        conn = sql.connect("database.db")
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Something went wrong.")
        logging.debug("Error message: ", e)


def authenticate(email, password):
    result = data_query(f"SELECT * FROM users WHERE email_address = '{email}'")
    return result


def data_query(query):
    conn, cursor = connect_to_database()
    return cursor.execute(query).fetchall()


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
