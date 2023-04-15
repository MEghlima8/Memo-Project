from flask import Flask, request, redirect, render_template, session
from send_email import send_confirm_email
import sqlite3
import json
import database
import email_management as email_mng


def check_login(email, password):
    all_users = []
    users = []
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    tuple_of_users = cur.execute("select email,password,active from users_info")
    conn.commit()
    for row in tuple_of_users:
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
    
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute('insert into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)',
                (info['fullname'], info['email'], info['password'],link))
    conn.commit()
    return 'True'


def get_user_id(email):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    user_id = cur.execute(
        "select id from users_info where email = ?", (email,)).fetchone()[0]
    conn.commit()
    return (user_id)
