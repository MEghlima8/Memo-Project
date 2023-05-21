import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'HOST' : os.getenv('HOST') , 
    'DEBUG' : os.getenv('DEBUG') , 
    'PORT' : os.getenv('PORT') , 
    'DATABASE' : os.getenv('DATABASE') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,
    'SESSION_TYPE' : os.getenv('SESSION_TYPE') ,
    'REDIS_HOST' : os.getenv('REDIS_HOST') ,
    'REDIS_PORT' : os.getenv('REDIS_PORT') ,
    'REDIS_PASSWORD' : os.getenv('REDIS_PASSWORD') ,
    'REDIS_DB_NUMBER' : os.getenv('REDIS_DB_NUMBER')
}