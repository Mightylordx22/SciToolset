import sqlite3 as sql



conn = sql.connect("database.db")
cur = conn.cursor()



cur.execute("INSERT INTO test VALUES ('1','1')")

