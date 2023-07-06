import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    
    'HOST' : os.getenv('HOST') , 
    'DEBUG' : os.getenv('DEBUG') , 
    'PORT' : os.getenv('PORT') , 
    
    # Database 
    'DB_NAME' : os.getenv('DB_NAME') ,
    'DB_HOST' : os.getenv('DB_HOST') ,
    'DB_USER' : os.getenv('DB_USER') ,
    'DB_PASSWORD' : os.getenv('DB_PASSWORD') ,
    'DB_PORT' : os.getenv('DB_PORT') ,
    
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,
    'SESSION_TYPE' : os.getenv('SESSION_TYPE') ,
    
    # Upolad photos
    'UPLOAD_USERS_PHOTOS' : os.getenv('UPLOAD_USERS_PHOTOS') ,
    
    # Redis
    'REDIS_HOST' : os.getenv('REDIS_HOST') ,
    'REDIS_PORT' : os.getenv('REDIS_PORT') ,
    'REDIS_PASSWORD' : os.getenv('REDIS_PASSWORD') ,
    'REDIS_DB_NUMBER' : os.getenv('REDIS_DB_NUMBER')
}