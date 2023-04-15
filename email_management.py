from flask import Flask, request, redirect, render_template, session
from send_email import send_confirm_email
import sqlite3
import json
import database




def confirm_email(link):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()    
    cur.execute("UPDATE users_info SET active=?  where link=?",
                (1,link))
    x = cur.fetchone()
    conn.commit()
    return 'True'


def check_confirm_email():
    all_links = []
    link = request.args.get('link','')    
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    users_links = cur.execute("select link from users_info")
    conn.commit()
    for row in users_links:
        all_links.append(row[0])    
    for i in all_links:
        if i == link:
            confirm_email(link)
            return render_template('confirm_email.html')



def is_exist_email(email):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute("select email from users_info where email=?", (email,))
    x = cur.fetchone()
    conn.commit()
    if x == None:
        return False
    else:
        return True