import pdb
import secrets
from App import config
from flask import Flask, request, render_template, session, make_response
from App.Controller.email_controller import Email
from App.Controller.user_controller import User
from App.Controller import db_controller as db
from App.logs import Log
import os


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']

@app.route('/signup', methods=['GET','POST'])
def _signup():
    l_data_request = ['fullname' , 'email' , 'password' , 'confirm_password']
    l_user_info = User.get_user_info(l_data_request)
    o_user = User(l_user_info[0] , l_user_info[1] , l_user_info[2] , l_user_info[3])
    l_user_info = { 'fullname':l_user_info[0] , 'email':l_user_info[1] , 'password':l_user_info[2] , 'confirm_password':l_user_info[3]}
    s_user = o_user.signup()
    return s_user


@app.route('/signin' ,methods=['GET' , 'POST'])
def _signin():
    s_user_hash = request.cookies.get('user_hash')     
    if s_user_hash is None:        
        try:            
            l_info=['email' , 'password' ]            
            l_user_info = User.get_user_info(l_info) 
            o_user = User(email=l_user_info[0] , password=l_user_info[1])            
            o_user = o_user.signin()            
            return o_user
        except:            
            return render_template('index.html')    
    # Get email
    s_query = 'select email from users_info where user_hash = ?'
    s_email = db.execute(s_query ,(s_user_hash,)).fetchone()[0]
    
    # Get user id
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'logged in automatically')
    
    session['logged_in'] = True
    session['email'] = s_email
    return 'user1'
        
        
@app.route('/' ,methods=['GET' , 'POST'] )
def index():
    return render_template('index.html')


# When user want to signout the account
@app.route('/sign-out', methods=['GET'])
def _signout():
    # Get user id
    s_query = 'select id from users_info where email = ?'
    i_user_id = db.execute(s_query, (session['email'],)).fetchone()[0]
    
    log = Log(i_user_id, 'logged out')
    session['logged_in'] = False
    session['email']= False
    session.clear()
    resp = make_response('True')
    resp.set_cookie('user_hash', '', max_age=0)
    return resp



# Checks that the user's new album title is not the same as other albums
@User.user_required
def duplicate_title(title):
    s_user_hash = request.cookies.get('user_hash')
    
    # Get user id
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    # Get user albums title
    s_query = 'select title from users_photo where user_id = ? and title = ?'
    check_is_there = db.execute(s_query, (i_user_id,title,)).fetchone()
    
    # False if there is no album with this title
    if check_is_there is None:
        return False
    
    
    return True


# Add new album to user
@app.route('/add-album', methods=['GET','POST'])
@User.user_required
def _add_album():
    l_data_request = ['title' , 'info' , 'photo']
    
    # Get album info
    l_album_info = User.get_user_info(l_data_request)
    s_title = l_album_info[0]
    s_caption = l_album_info[1]
    s_photo = l_album_info[2]
    
    # All fields must be fill
    if s_title == '' or s_caption == '' or s_photo == '':
        return 'empty'
    
    # User's new album title must be unique
    if duplicate_title(s_title):
        return 'duplicate title'
    
    s_photo_src ='/static/images/' + l_album_info[2]
    s_user_hash = request.cookies.get('user_hash')
    
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'add album')
    # Add new album to database
    s_query = 'insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)'
    db.execute(s_query ,(i_user_id, s_photo_src, s_title,s_caption,))
    return 'True'


# Get user albums when signin was successful
@app.route('/albums', methods=['GET','POST'])
@User.user_required
def _albums():
    l_titles=[]
    l_albumsinfo=[]
    s_user_hash = request.cookies.get('user_hash')
    
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'get albums')
    
    # get title, info, photo src
    s_query = 'select title,info,src from users_photo where user_id = ?'
    l_albums_info = db.execute(s_query,(i_user_id,)).fetchall()
    for i in l_albums_info:
        
        # From each album, it takes only the first record stored in the database.        
        # Because it is defined in the structure of the database that
        # the first photo of each album is the album cover.
        if i[0] in l_titles:
            continue
        l_titles.append(i[0])        
        l_albumsinfo.append(list(i))
    return l_albumsinfo


# Add photo to user selected album
@app.route('/add_photo_to_album', methods=['GET','POST'])
@User.user_required
def _add_photo_to_album():
    s_user_hash = request.cookies.get('user_hash')
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
        
    log = Log(i_user_id, 'add photo to album')
    
    # Get album_title and photo_name(src)
    l_data_request = ['album_title' , 'photo_name']
    l_user_info = User.get_user_info(l_data_request)
    
    s_src = '/static/images/' + l_user_info[1]
    l_user_info = {'album_title':l_user_info[0] , 'photo_name':l_user_info[1] ,'src':s_src}
    
    s_query = 'select info from users_photo where user_id = ? and title = ?'
    s_album_info = db.execute(s_query , (i_user_id,l_user_info['album_title'],)).fetchall()[0][0]
    
    s_query = 'insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)'
    db.execute(s_query, (i_user_id, s_src, l_user_info['album_title'], s_album_info,))
    
    s_query = 'select src from users_photo where user_id = ? and title = ?'
    l_album_photos = db.execute(s_query , (i_user_id, l_user_info['album_title'] ,)).fetchall()
    
    l_album_photos = [i[0] for i in l_album_photos]
    
    # photos[0] is the album cover photo
    return l_album_photos[1:]



# Get user album photos
@app.route('/albumphotos', methods=['GET','POST'])
@User.user_required
def _albumphotos():
    l_photos=[]
    s_user_hash = request.cookies.get('user_hash')
    
    s_query = 'select id from users_info where user_hash = ?'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'get album photos')
    
    l_data_request = ['album_title']
    s_title = User.get_user_info(l_data_request)[0]
    
    s_query = 'select src from users_photo where user_id = ? and title = ?'
    l_album_photos = db.execute(s_query,(i_user_id,s_title,)).fetchall()
    
    l_photos = [i[0] for i in l_album_photos]

    return l_photos[1:]
    
    

# To accept the link confirmation request
@app.route('/confirm', methods=['GET'])
def _check_confirm():
    return Email.check_confirm_email()
	        
        
if __name__ == '__main__':
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])