import sqlite3
from App import config

def execute(query, args=()):
    s_database_name = config.configs['DATABASE']
    
    conn = sqlite3.connect(s_database_name)
    cur = conn.cursor()
    x = cur.execute(query, args)
    conn.commit()
    return x

