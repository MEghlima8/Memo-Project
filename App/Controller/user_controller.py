from flask import session , abort , request ,make_response
from App.Controller.email_controller import Email
from App.Controller import db_controller as db
from functools import wraps
import secrets
import json
from App.Controller.validation import Valid
from App.logs import Log
import hashlib


class User:
    
    def __init__(self,  fullname=None, email=None, password=None, confirm_password=None ):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        
    # Do signup user
    def signup(self):        
        check_user_info = self.is_valid_signup()        
        
        if check_user_info is not True:
            return check_user_info
        
        # Send confirmation email
        email = Email()
        s_confirmation_link = email.send_confirmation_email(self.email, self.fullname)
        
        # To save password in database as hash.
        password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        
        query = 'insert or ignore into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)'
        db.execute(query , (self.fullname, self.email, password, s_confirmation_link,))
        return 'True'
    
    
    def is_valid_signup(self):
        
        # Check duplicate email
        check_exist_email = Email.is_exist_email(self.email)        
        if check_exist_email is None :
            return False
        elif check_exist_email == True :
            return 'duplicate_email'
        elif check_exist_email == 'noactive':
            return 'noactive'        
        # Validate signup info
        valid = Valid(email=self.email , password=self.password , confitm_password=self.confirm_password , fullname=self.fullname)
        valid_info = valid.signup()
        if (valid_info=='email_length') or (valid_info=='char_email') or (valid_info=='empty_email'):        
            return valid_info        
        
        if (valid_info=='password_length') or (valid_info=='char_password') or (valid_info=='empty_password') :        
            return valid_info        
        
        if (valid_info=='fullname_length') or (valid_info=='char_fullname') or (valid_info=='empty_fullname') :        
            return valid_info        
        
        if (valid_info=='no_match_passwords'):        
            return valid_info        

        return True


    # This will check user is logged in or not.if not getback error 403
    @staticmethod
    def user_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get('logged_in') is True:
                return func(*args, **kwargs)
            else:
                abort(403)
        return wrapper
    
    

    # Do signin user
    def signin(self):                
        check_user_info = self.is_valid_signin()
        if check_user_info == True :            
            session['logged_in'] = True
            session['email'] = self.email
            
            s_query = 'select id from users_info where email = ?'
            i_user_id = db.execute(s_query, (self.email,)).fetchone()[0]
            
            log = Log(i_user_id, 'logged in')
            
            # Get random hash
            user_hash = secrets.token_urlsafe(32)
            resp = make_response('user')
            resp.set_cookie('user_hash', user_hash,max_age=60 * 60 * 24 * 90)            
            # Set hash for user
            s_query = 'UPDATE users_info SET user_hash = ? WHERE email = ?'
            db.execute(s_query , (user_hash, self.email,) )                        
            
            return resp
        elif check_user_info == 'noactive':               
            return 'noactive'
        
        elif (check_user_info=='email_length') or (check_user_info=='password_length') or (check_user_info=='char_email') or (check_user_info=='char_password') or (check_user_info=='empty_password') or (check_user_info=='empty_email'):                        
            return check_user_info        
        return 'False'
    
    
    # True if user password is True. noactive if user did signup but did not active
    def is_valid_signin(self):        
        valid = Valid(email=self.email, password=self.password)        
        valid_info = valid.signin()        
        
        if (valid_info=='empty_email') or (valid_info=='empty_password') :
            return valid_info    
        elif (valid_info=='email_length') or (valid_info=='char_email') or (valid_info=='password_length') or (valid_info=='char_password'):
            return False
        # Getback users info
        hash_password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        
        s_query = 'select email,password,active from users_info where email=? and password=?'
        l_user_info = db.execute(s_query ,(self.email,hash_password,)).fetchone()

        # i[0] is email and i[1] is password        
        if l_user_info is not None:
            if l_user_info[2] == 1:           
                return True  
            return 'noactive'
        return False


    # Getback user_info
    @staticmethod
    def get_user_info(l_data_request):        
        user_info = request.data.decode('utf-8')
        user_info = json.loads(user_info)        
        return [user_info[req] for req in l_data_request]