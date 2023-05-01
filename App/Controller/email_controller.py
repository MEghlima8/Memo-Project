from flask import request, render_template,abort
from App.Controller import db_controller as db
import smtplib
import ssl
from getpass import getpass
import random
import string


class Email:
    
    def  __init__(self):
        self.s_smtp_server = 'smtp.gmail.com'
        self.i_port = 465
        self.s_sender_email = 'eghlima.mohammad@gmail.com'
        self.s_password = 'bqdfacwywjjdhdvp'

    def send_confirmation_email(self, email, username):

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
        with smtplib.SMTP_SSL(self.s_smtp_server, self.i_port, context=context) as server:
            server.login(self.s_sender_email, self.s_password) 
            server.sendmail(self.s_sender_email, email, s_message)
            server.quit()
            return s_link_key
    

    @staticmethod
    def check_confirm_email():
        l_all_links = []
        s_link = request.args.get('link','')    
        
        # Get All confirm links 
        query = 'select link from users_info where link=?'
        is_exist = db.execute(query,(s_link,)).fetchone()
        
        if is_exist is not None :
            query = 'UPDATE users_info SET active=?  where link=?'
            db.execute(query, (1,s_link,)).fetchone()
            return render_template('confirm_email.html')
        abort (403)
    

    @staticmethod
    def is_exist_email(email):        
        # Getback users info
        query = 'select active from users_info where email=?'
        l_users_info = db.execute(query ,(email,)).fetchone()        
        if l_users_info is None :            
            return False
        elif l_users_info[0]==1:            
            return True            
        return 'noactive'
        
        