import json
from functools import wraps
import secrets
from flask import Flask, request, redirect, render_template, session,abort
import sqlite3
from send_email import send_confirm_email
import pdb


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex()


def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') is True:
            return func(*args, **kwargs)
        else:
            abort(403)
    #wrapper.__name__ = func.__name__
    return wrapper


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
    


def get_user_id(email):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    user_id = cur.execute(
        "select id from users_info where email = ?", (email,)).fetchone()[0]
    conn.commit()
    return (user_id)

@user_required
def duplicate_title(title):
    email = session['email']
    user_id = get_user_id(email)
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    try:
        titles = cur.execute(
            "select title from users_photo where user_id = ?", (user_id,)).fetchall()
        conn.commit()
        for tit in titles:            
            if title==tit[0]:                
                return True
        return False
    except:
        conn.commit()
        return False

    


@app.route('/add-album', methods=['GET','POST'])
@user_required
def _add_album():
    album_info = request.data.decode('utf-8')
    album_info = json.loads(album_info)
    title = album_info["title"]
    caption = album_info["info"]
    photo = album_info["photo"]
    photo_src ='/static/images/' + photo
    try:
        user_email = session['email']        
        user_id = get_user_id(user_email)
    except:
        redirect('/signin')
    
    if title == '' or caption == '' or photo == '':
        return 'empty'
    if duplicate_title(title):
        return 'duplicate title'
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()    
    cur.execute('insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)',
                (user_id, photo_src, title,caption))
    conn.commit()
    return 'True'



@app.route('/albums', methods=['POST'])
@user_required
def _albums():
    titles=[' ']
    albumsinfo=[]
    email = session['email']
    user_id = get_user_id(email)
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    albums_info = cur.execute(
        "select title,info,src from users_photo where user_id = ?", (user_id,)).fetchall()
    conn.commit()
    for i in albums_info:
        if i[0] in titles:
            continue
        titles.append(i[0])        
        albumsinfo.append(list(i))
    return albumsinfo



@app.route('/add_photo_to_album', methods=['GET','POST'])
@user_required
def _add_photo_to_album():
    photos=[]
    email = session['email']
    user_id = get_user_id(email)
    album_title = request.data.decode('utf-8')
    album_title = json.loads(album_title)
    title = album_title["album_title"]
    photo_name = album_title["photo_name"]
    src = '/static/images/' + photo_name
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    album_info = cur.execute(
        "select info from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    album_info = album_info[0][0]
    album_photos = cur.execute('insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)',
                (user_id, src, title,album_info))
    
    album_photos = cur.execute(
        "select src from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    
    conn.commit()
    for i in album_photos:
        photos.append(i[0])
    return photos[1:]



@app.route('/albumphotos', methods=['GET','POST'])
@user_required
def _albumphotos():
    photos=[]
    email = session['email']
    user_id = get_user_id(email)
    album_title = request.data.decode('utf-8')
    album_title = json.loads(album_title)
    title = album_title["album_title"]    
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    album_photos = cur.execute(
        "select src from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    conn.commit()    
    for i in album_photos:
        photos.append(i[0])
    return photos[1:]
    

@app.route('/sign-out', methods=['GET'])
def _signout():
    session['logged_in'] = False
    session['email']= False
    return 'True'

def confirm_email(link):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()    
    cur.execute("UPDATE users_info SET active=?  where link=?",
                (1,link))
    x = cur.fetchone()
    conn.commit()
    return 'True'


@app.route('/confirm', methods=['GET'])
def check_confirm():
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
	

@app.route('/signup', methods=['GET','POST'])
def _signup():
    user_info = request.data.decode('utf-8')
    user_info = json.loads(user_info)
    fullname = user_info["fullname"]
    email = user_info["email"]
    password = user_info["password"]
    repassword = user_info["confirm_password"]
    
    if fullname == '' or email == '' or password == '' or repassword == '':
        return 'empty'
    if is_exist_email(email) == True :        
        return 'duplicate_email'
    if password != repassword:        
        return 'missmatch_pass'
    link = send_confirm_email(email,fullname)
    
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute('insert into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)',
                (fullname, email, password,link))
    conn.commit()
    return 'True'



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



@app.route('/signin' ,methods=['GET' , 'POST'])
@app.route('/' ,methods=['GET' , 'POST'] )
def _signin():
    try :
        user_info = request.data.decode('utf-8')
        user_info = json.loads(user_info)
        email = user_info["email"]
        password = user_info["password"]
        check_user = check_login(email, password)
        if check_user == True:
            session['logged_in'] = True
            session['email'] = email
            return 'user'
        elif check_user == 'noactive':
            return 'noactive'
        return 'False'
    
    except:
        return render_template('index.html')
        


app.run(debug=True)
