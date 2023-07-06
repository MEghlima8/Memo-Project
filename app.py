from App import config
from flask import Flask, request, render_template, make_response, abort
from App.Controller.email_controller import Email
from App.Controller.user_controller import User
from App.Controller import db_controller as db
from App.logs import Log
from functools import wraps
import redis
import uuid
import os


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

rd = redis.Redis(host=config.configs['REDIS_HOST'], port=config.configs['REDIS_PORT'],
                 password=config.configs['REDIS_PASSWORD'], db=config.configs['REDIS_DB_NUMBER'])

user_email = None

# This will check user is logged in or not.if not getback error 403
@staticmethod
def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            if rd.hget(user_email, 'logged_in').decode() == 'True':
                return func(*args, **kwargs)
            abort(403)
                
        except:
            s_user_hash = request.cookies.get('user_hash')
            s_query = 'select email,id from users_info where user_hash = %s'
            s_user_info = db.execute(s_query ,(s_user_hash,)).fetchone()
            
            if s_user_hash is not None and rd.hget(s_user_info[0], 'logged_in').decode() is not True:
                rd.hset(s_user_info[0], 'id' , str(s_user_info[1]))
                rd.hset(s_user_info[0], 'logged_in' , 'True')
                return func(*args, **kwargs)            
            abort(403)
            
    return wrapper


@app.route('/signin' ,methods=['GET' , 'POST'])
def _signin():
        
    s_user_hash = request.cookies.get('user_hash')    
    try:        

        # Get email
        s_query = 'select email from users_info where user_hash = %s'
        s_email = db.execute(s_query ,(s_user_hash,)).fetchone()[0]         
        # Get user id
        s_query = 'select id from users_info where user_hash = %s'
        i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]    

        Log(i_user_id, 'logged in automatically')    
        rd.hset(s_email, 'id' , str(i_user_id))
        rd.hset(s_email, 'logged_in' , 'True')
        
        # session['logged_in'] = True
        # session['email'] = s_email            
        

        return 'user'
    
    except:
                
        try:          
            l_info=['email' , 'password' ]            
            l_user_info = User.get_user_info(l_info)            
            o_user = User(email=l_user_info[0] , password=l_user_info[1])            
            o_user = o_user.signin()                        
            

            if o_user != 'False' and o_user != 'noactive':                
                global user_email
                user_email = l_user_info[0]                
                s_query = 'select id from users_info where email = %s'
                s_id = str(db.execute(s_query ,(user_email,)).fetchone()[0])
                                                
                rd.hset(user_email,'id',s_id)                
                rd.hset(user_email,'logged_in','True')                

                return o_user
                        
            return o_user
        except:            
            return render_template('index.html') 
    
    
        
@app.route('/' ,methods=['GET' , 'POST'] )
def index():  
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    # user_email = 'eghlima.mohammad@gmail.com'
    # s_query = "select * from users_info where email = %s"
    s_query = 'select * from users_info'
    # s_query = 'CREATE TABLE users_info (id CHAR(255) NOT NULL UNIQUE ,fullname CHAR(255) NOT NULL ,email CHAR(255) NOT NULL UNIQUE ,password CHAR(255) NOT NULL ,active INTEGER NOT NULL ,link CHAR(255) ,user_hash CHAR(255),PRIMARY KEY("id"))'
    # s_query = "insert into users_info (id,fullname,email,password,active,link,user_hash) values ('1','Mohammad','eghlima.mohammad@gmail.com','49ea22d96c948eb5543980e27ad51f0b',1,'sfsfsfdfs','hashahshashhsashshahs')"
    s_id = db.execute(s_query ,()).fetchall()    
    return 'test'


@app.route('/signup', methods=['GET','POST'])
def _signup():
    l_data_request = ['fullname' , 'email' , 'password' , 'confirm_password']
    l_user_info = User.get_user_info(l_data_request)
    o_user = User(l_user_info[0] , l_user_info[1] , l_user_info[2] , l_user_info[3])
    l_user_info = { 'fullname':l_user_info[0] , 'email':l_user_info[1] , 'password':l_user_info[2] , 'confirm_password':l_user_info[3]}
    s_user = o_user.signup()
    return s_user


# When user want to signout the account
@app.route('/sign-out', methods=['GET'])
def _signout():
    
    s_user_hash = request.cookies.get('user_hash')
    
    s_query = 'select email from users_info where user_hash = %s'
    s_user_email = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    # Get user id
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    Log(i_user_id, 'logged out')
    
    rd.delete(s_user_email)

    resp = make_response('True')
    resp.set_cookie('user_hash', '', max_age=0)
    return resp



# Checks that the user's new album title is not the same as other albums
@user_required
def duplicate_title(title):
    s_user_hash = request.cookies.get('user_hash')
    
    # Get user id
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    # Get user albums title
    s_query = 'select title from users_photo where user_id = %s and title = %s'
    check_is_there = db.execute(s_query, (i_user_id,title,)).fetchone()
    
    # False if there is no album with this title
    if check_is_there is None:
        return False
    
    
    return True


# Add new album to user
@app.route('/add-album', methods=['GET','POST'])
@user_required
def _add_album():
    
    try:
        s_photo = request.files['AddNewAlbum']
    except:
        return 'fileSize'
    s_title = request.form['title']
    s_caption = request.form['info']
    
    # All fields must be fill
    if s_title == '' or s_caption == '' or s_photo == '':
        return 'empty'
    
    # User's new album title must be unique
    if duplicate_title(s_title):
        return 'duplicate title'
    
    addAlbumPhotoUUID = uuid.uuid4().hex
    addAlbumPhotoSrc = addAlbumPhotoUUID + '.' + s_photo.mimetype.split('/')[1]
    s_photo.save(os.path.join(config.configs["UPLOAD_USERS_PHOTOS"], addAlbumPhotoSrc))
    
    s_user_hash = request.cookies.get('user_hash')
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'add album')
    
    # Add new album to database
    s_query = 'insert into users_photo (user_id,photo_name,title,info) values(%s , %s , %s , %s)'
    db.execute(s_query ,(i_user_id, addAlbumPhotoSrc, s_title,s_caption,))
    
    return 'True'


# Add photo to user selected album
@app.route('/add_photo_to_album', methods=['GET','POST'])
@user_required
def _add_photo_to_album():
    
    s_user_hash = request.cookies.get('user_hash')
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
        
    Log(i_user_id, 'add photo to album')
    
    try:
        AddPhotoToAlbum = request.files['AddPhotoToAlbum']
    except:
        return 'fileSize'
    
    album_title = request.form['album_title']
    
    addPhotoToAlbumUUID = uuid.uuid4().hex
    addPhotoToAlbumSrc = addPhotoToAlbumUUID + '.' + AddPhotoToAlbum.mimetype.split('/')[1]
    
    AddPhotoToAlbum.save(os.path.join(config.configs["UPLOAD_USERS_PHOTOS"], addPhotoToAlbumSrc))
    
    
    # Get album_title and photo_name(src)
    
    s_query = 'select info from users_photo where user_id = %s and title = %s'
    s_album_info = db.execute(s_query , (i_user_id,album_title,)).fetchall()[0][0]
    
    s_query = 'insert into users_photo (user_id,photo_name,title,info) values(%s , %s , %s , %s)'
    db.execute(s_query, (i_user_id, addPhotoToAlbumSrc, album_title, s_album_info,))
    
    s_query = 'select photo_name from users_photo where user_id = %s and title = %s'
    l_album_photos = db.execute(s_query , (i_user_id, album_title ,)).fetchall()
    
    l_album_photos = [i[0] for i in l_album_photos]    
    
    for i in range(len(l_album_photos)):        
        l_album_photos[i] = './static/images/' + l_album_photos[i]        
        
    # photos[0] is the album cover photo
    return l_album_photos[1:]


# Get user albums when signin was successful
@app.route('/albums', methods=['GET','POST'])
@user_required
def _albums():
        

    l_titles=[]
    l_albumsinfo=[]
    s_user_hash = request.cookies.get('user_hash')
    
    
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
        

    Log(i_user_id, 'get albums')
    
    # get title, info, photo src
    s_query = 'select title,info,photo_name from users_photo where user_id = %s'
    l_albums_info = db.execute(s_query,(i_user_id,)).fetchall()
    l_albums_info = [list(i) for i in l_albums_info]
        

    for i in l_albums_info:
        i[2] = './static/images/' + i[2]
        
        # From each album, it takes only the first record stored in the database.        
        # Because it is defined in the structure of the database that
        # the first photo of each album is the album cover.
        if i[0] in l_titles:
            continue
        l_titles.append(i[0])
        l_albumsinfo.append(list(i))
    

    return l_albumsinfo



# Get user album photos
@app.route('/albumphotos', methods=['GET','POST'])
@user_required
def _albumphotos():
    l_photos=[]
    s_user_hash = request.cookies.get('user_hash')
    
    s_query = 'select id from users_info where user_hash = %s'
    i_user_id = db.execute(s_query, (s_user_hash,)).fetchone()[0]
    
    log = Log(i_user_id, 'get album photos')
    
    l_data_request = ['album_title']
    s_title = User.get_user_info(l_data_request)[0]
    
    s_query = 'select photo_name from users_photo where user_id = %s and title = %s'
    l_album_photos = db.execute(s_query,(i_user_id,s_title,)).fetchall()
    
    l_photos = [ './static/images/' + i[0] for i in l_album_photos]    

    return l_photos[1:]
    
    

# To accept the link confirmation request
@app.route('/confirm', methods=['GET'])
def _check_confirm():
    return Email.check_confirm_email()
	        
        
if __name__ == '__main__':
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])