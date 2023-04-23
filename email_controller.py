from flask import request, render_template
import db_controller as db


def check_confirm_email():
    all_links = []
    link = request.args.get('link','')    
    
    # Get All confirm links 
    query = "select link from users_info"
    users_links = db.execute(query,)
    
    for row in users_links:
        all_links.append(row[0])    
    for i in all_links:
        if i == link:
            
            query = "UPDATE users_info SET active=?  where link=?"
            db.execute(query, (1,link,)).fetchone()
            return render_template('confirm_email.html')



def is_exist_email(email):
    
    query = "select email from users_info where email=?"
    x = db.execute(query , (email,)).fetchone()
    
    # False If not already confirmed
    if x == None:
        return False
    else:
        return True