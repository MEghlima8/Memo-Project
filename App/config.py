import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'HOST' : os.getenv('HOST') , 
    'DEBUG' : os.getenv('DEBUG') , 
    'PORT' : os.getenv('PORT') , 
    'DATABASE' : os.getenv('DATABASE') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT')
}