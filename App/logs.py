from flask import request
from App.Controller import db_controller as db
from datetime import datetime

class Log:
    def __init__(self,user_id,note) :
        self.os = request.headers['Sec-Ch-Ua-Platform']
        self.browser = request.headers['Sec-Ch-Ua'].split(',')[1]
        self.path = request.path
        self.time = str(datetime.now())
        self.user_agent = request.headers['User-Agent']
        self.req_method = request.method
        self.ip =  request.remote_addr
        
        self.user_id = user_id
        self.note = note
        
        self.query = "INSERT INTO users_log (user_id,os,browser,path,time,note,user_agent,request_method,ip) VALUES (%s , %s , %s , %s , %s , %s , %s , %s , %s)"
        db.execute( self.query , (self.user_id, self.os, self.browser, self.path, self.time, self.note, self.user_agent, self.req_method, self.ip))
            