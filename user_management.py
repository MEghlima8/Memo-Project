from flask import session , abort , request,make_response
from send_email import send_confirm_email
import db_controller as db
import email_controller as email_mng
from functools import wraps
import secrets
import json

# This will check user is logged in or not.if not getback error 403
def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') is True:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


# True if user password is True. noactive if user did signup but did not active
def check_login(email, password):
    all_users = []
    
    query = "select email from users_info where user_hash = ?"
    users_info = db.execute("select email,password,active from users_info" ,)

    for row in users_info:
        all_users.append(row)
    for i in all_users:
        
        # i[0] is email and i[1] is password
        if i[0] == email and i[1] == password:
            if i[2]==1:                
                return True
            return 'noactive'
    return False


# Do signin user
def signin(info):
    check_user = check_login(info['email'], info['password'])
    if check_user == True:
        session['logged_in'] = True
        session['email'] = info['email']
        user_hash = secrets.token_urlsafe(32)
        resp = make_response('user')
        resp.set_cookie('user_hash', user_hash,max_age=60 * 60 * 24 * 90)
        query = "UPDATE users_info SET user_hash = '{user_hash}' WHERE email = '{email}';".format(user_hash=user_hash , email=info['email'])
        db.execute(query)
        return resp
    elif check_user == 'noactive':
        return 'noactive'
    return 'False'

    
# Do signup user
def signup(info):
    for i in info:
        if info[i] == '':
            return 'empty'
        
    # Check duplicate email
    if email_mng.is_exist_email(info['email']) == True :        
        return 'duplicate_email'
    
    # Check password and repassword
    if info['password'] != info['confirm_password']:
        return 'missmatch_pass'
    
    # Send confirm link
    link = send_confirm_email(info['email'],info['fullname'])
    info['link'] = link
    
    query = 'insert into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)'
    db.execute(query , (info['fullname'], info['email'], info['password'], info['link'],))
    return 'True'


# Getback user_info
def get_user_info(data_request):
    info = []
    user_info = request.data.decode('utf-8')
    user_info = json.loads(user_info)
    for req in data_request:
        info.append(user_info[req])
    return (info)