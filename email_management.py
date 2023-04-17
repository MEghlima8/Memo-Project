from flask import request, render_template
import db_management as db


def check_confirm_email():
    all_links = []
    link = request.args.get('link','')    
    users_links = db.get_all_confirm_links()
    for row in users_links:
        all_links.append(row[0])    
    for i in all_links:
        if i == link:
            db.confirm_email(link)
            return render_template('confirm_email.html')



def is_exist_email(email):
    x = db.check_email_exist(email)
    if x == None:
        return False
    else:
        return True