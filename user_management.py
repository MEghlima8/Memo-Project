from flask import session , abort
from send_email import send_confirm_email
import db_management as db
import email_management as email_mng
from functools import wraps

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') is True:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper




def check_login(email, password):
    all_users = []
    users_info = db.get_users()
    for row in users_info:
        all_users.append(row)
    for i in all_users:
        if i[0] == email and i[1] == password:
            if i[2]==1:                
                return True
            return 'noactive'
    return False



def signin(info):
    check_user = check_login(info['email'], info['password'])
    if check_user == True:
        session['logged_in'] = True
        session['email'] = info['email']
        return 'user'
    elif check_user == 'noactive':
        return 'noactive'
    return 'False'

    
    
def signup(info):
    for i in info:
        if info[i] == '':
            return 'empty'
    if email_mng.is_exist_email(info['email']) == True :        
        return 'duplicate_email'
    if info['password'] != info['repassword']:
        return 'missmatch_pass'
    link = send_confirm_email(info['email'],info['fullname'])
    info['link'] = link
    db.do_signup(info)
    return 'True'

    