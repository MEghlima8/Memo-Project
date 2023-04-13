import smtplib
import ssl
from getpass import getpass
import random
import string


def send_confirm_email(email, username):

    smtp_server = 'smtp.gmail.com'
    port = 465
    sender_email = 'eghlima.mohammad@gmail.com'
    password = 'wgzjagoknsnswjtb'


    link_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
    link = "http://localhost:5000/confirm?link=%s" % link_key
    
    TEXT = '''Hello {username} , Click on the link below to confirm your email in MemorizeMemories.com, otherwise ignore this message.
    {link}
    '''.format(username=username, link=link)
    SUBJECT = 'Confirmation Email'
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password) 
        server.sendmail(sender_email, email, message)
        server.quit()
        return link_key
  
