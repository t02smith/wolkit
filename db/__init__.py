import sqlite3

_connection = sqlite3.connect("wolkit.db", check_same_thread=False)
_cursor = _connection.cursor()
