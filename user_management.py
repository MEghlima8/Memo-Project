from flask import session , abort , request,make_response
from email_controller import send_confirm_email
import db_controller as db
import email_controller as email_ctrl
from functools import wraps
import secrets
import json
import validation


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
def is_auth_for_signin(email, password):
    l_all_users = []
    
    valid_info = validation.signin(email, password)
    if (valid_info=='email_length') or (valid_info=='password_length') or (valid_info=="char_email") or (valid_info=="char_password") or (valid_info=='empty_email') or (valid_info=='empty_password') :
        return valid_info    
    # Getback users info
    l_users_info = db.execute("select email,password,active from users_info" ,)

    for row in l_users_info:
        l_all_users.append(row)
    for i in l_all_users:
        # i[0] is email and i[1] is password
        if i[0] == email and i[1] == password:
            if i[2]==1:                      
                return True            
            return 'noactive'    
    return False


def is_auth_for_signup(fullname,email, password,confirm_password):
    l_all_users = []
    
    # Check duplicate email
    if email_ctrl.is_exist_email(email) == True :        
        return 'duplicate_email'
    elif email_ctrl.is_exist_email(email) == 'noactive':
        return 'noactive'
        
    valid_info = validation.signup(fullname, email, password, confirm_password)
    if (valid_info=='email_length') or (valid_info=='char_email') or (valid_info=='empty_email'):        
        return valid_info
    
    if (valid_info=='password_length') or (valid_info=="char_password") or (valid_info=='empty_password') :        
        return valid_info
    
    if (valid_info=='fullname_length') or (valid_info=='char_fullname') or (valid_info=='empty_fullname') :        
        return valid_info
    
    if (valid_info=='no_match_passwords'):        
        return valid_info

    return True


# Do signup user
def signup(info):
    check_user_info = is_auth_for_signup(info['fullname'],info['email'], info['password'], info['confirm_password'])
    
    if check_user_info is not True:
        return check_user_info
    
    # Send confirm link
    link = send_confirm_email(info['email'],info['fullname'])
    info['link'] = link
    
    query = 'insert or ignore into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)'
    db.execute(query , (info['fullname'], info['email'], info['password'], info['link'],))
    return 'True'


# Do signin user
def signin(info):
    
    check_user_info = is_auth_for_signin(info['email'], info['password'])    
    if check_user_info == True:
        session['logged_in'] = True
        session['email'] = info['email']
        
        # Get random hash
        user_hash = secrets.token_urlsafe(32)
        resp = make_response('user')
        resp.set_cookie('user_hash', user_hash,max_age=60 * 60 * 24 * 90)
        
        # Set hash for user
        s_query = "UPDATE users_info SET user_hash = ? WHERE email = ?"
        db.execute(s_query , (user_hash, info['email'],) )
        
        return resp
    elif check_user_info == 'noactive':
        return 'noactive'
    
    elif (check_user_info=='email_length') or (check_user_info=='password_length') or (check_user_info=="char_email") or (check_user_info=="char_password") or (check_user_info=='empty_password') or (check_user_info=='empty_email'):
        return check_user_info
    
    return 'False'

    


# Getback user_info
def get_user_info(data_request):
    l_info = []
    user_info = request.data.decode('utf-8')
    user_info = json.loads(user_info)
    for req in data_request:
        l_info.append(user_info[req])
    return (l_info)