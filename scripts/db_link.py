import logging
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
