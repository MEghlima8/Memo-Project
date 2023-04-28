import sqlite3
import os
from dotenv import load_dotenv

def execute(query, args=()):
    load_dotenv()
    database = os.getenv('DATABASE')
    
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    x = cur.execute(query, args)
    conn.commit()
    return x

