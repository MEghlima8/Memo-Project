from flask import request
import db_controller as db
from datetime import datetime

def add_log(user_id,note):
    s_os = request.headers['Sec-Ch-Ua-Platform']
    s_browser = request.headers['Sec-Ch-Ua'].split(',')[1]
    s_path = request.path
    s_host = request.headers['Host']
    s_time = str(datetime.now())
    
    s_query = 'insert into users_log (user_id,os,browser,path,time,note) values(? , ? , ? , ? , ? , ?)'
    db.execute( s_query , (user_id, s_os, s_browser, s_path, s_time, note,))