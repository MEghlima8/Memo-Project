from App import config
import psycopg2

database_name = config.configs['DB_NAME']
database_host = config.configs['DB_HOST']
database_user = config.configs['DB_USER']
database_port = config.configs['DB_PORT']
database_password = config.configs['DB_PASSWORD']

def execute(query, args=()):
    
    conn = psycopg2.connect(
        host = database_host,
        database = database_name,
        user = database_user,
        password = database_password,
        port = database_port)
    
    cur = conn.cursor()
    cur.execute(query, args)
        
    conn.commit()

    return cur

