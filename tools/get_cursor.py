import sqlite3


def get_connection_cursor(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    return con, cur