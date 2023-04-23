import sqlite3


def execute(query, args=()):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    x = cur.execute(query, args)
    conn.commit()
    return x

