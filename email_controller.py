from flask import request, render_template
import db_controller as db
import smtplib
import ssl
from getpass import getpass
import random
import string

def check_confirm_email():
    l_all_links = []
    s_link = request.args.get('link','')    
    
    # Get All confirm links 
    query = 'select link from users_info'
    users_links = db.execute(query,)
    
    for row in users_links:
        l_all_links.append(row[0])    
    for i in l_all_links:
        if i == s_link: # The link in database and the input confirmation link are match
            
            query = 'UPDATE users_info SET active=?  where link=?'
            db.execute(query, (1,s_link,)).fetchone()
            return render_template('confirm_email.html')



def is_exist_email(email):
    
    l_all_users=[]
    # Getback users info
    l_users_info = db.execute('select email,active from users_info' ,)

    for row in l_users_info:
        l_all_users.append(row)
    for i in l_all_users:
        
        # i[0] is email and i[1] is password
        if i[0] == email :
            if i[1] == 1:                      
                return True            
            return 'noactive'
        return False
    
    
def send_confirm_email(email, username):

    s_smtp_server = 'smtp.gmail.com'
    i_port = 465
    s_sender_email = 'eghlima.mohammad@gmail.com'
    
    # This password is random
    s_password = 'bqdfacwywjjdhdvp'

    # Verify link key
    s_link_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    
    # The link to which the confirmation request will be emailed
    s_link = 'http://localhost:5000/confirm?link=%s' % s_link_key
    
    # The message that is sent to the user's email
    s_text = '''Hello {username} , Click on the link below to confirm your email in MemorizeMemories.com, otherwise ignore this message.
    {link}
    '''.format(username=username, link=s_link)
    
    # Email subject
    s_subject = 'Confirmation Email'
    
    # Email message
    s_message = 'Subject: {}\n\n{}'.format(s_subject, s_text)


    # reference : https://www.mongard.ir/one_part/170/sending-email-python/
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(s_smtp_server, i_port, context=context) as server:
        server.login(s_sender_email, s_password) 
        server.sendmail(s_sender_email, email, s_message)
        server.quit()
        return s_link_key
  
