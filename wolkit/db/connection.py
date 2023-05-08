import sqlite3

db_con = sqlite3.connect("wolkit.db", check_same_thread=False)
db_cursor = db_con.cursor()
