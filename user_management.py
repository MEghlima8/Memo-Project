from flask import session , abort , request
from send_email import send_confirm_email
import db_management as db
import email_management as email_mng
from functools import wraps
import json

# This will check user is logined or not.if not getback error 403
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
    users_info = db.get_users()
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
        return 'user'
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
    db.do_signup(info)
    return 'True'


# Getback user_info
def get_user_info(data_request):
    info = []
    user_info = request.data.decode('utf-8')
    user_info = json.loads(user_info)
    for req in data_request:
        info.append(user_info[req])
    return (info)