import json
import secrets
from flask import Flask, request, redirect, render_template, session, make_response
import email_controller as email_mng
import user_management as user_mng
import db_controller as db


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex()

# Checks that the user's new album title is not the same as other albums
@user_mng.user_required
def duplicate_title(title):
    
    # Get user id and all user's album titles
    user_hash = request.cookies.get('user_hash')
    
    query = "select id from users_info where user_hash = ?"
    user_id = db.execute(query, (user_hash,)).fetchone()[0]
    
    query = "select title from users_photo where user_id = ?"
    titles = db.execute(query, (user_id,)).fetchall()
    
    # False if there is no album for user
    if titles == False:
        return False
    
    for tit in titles:
        # True if title is duplicate                
        if title==tit[0]:
            return True
    return False


# Add new album to user
@app.route('/add-album', methods=['GET','POST'])
@user_mng.user_required
def _add_album():
    data_request = ["title" , "info" , "photo"]
    
    # Get album info
    album_info = user_mng.get_user_info(data_request)
    title = album_info[0]
    caption = album_info[1]
    photo = album_info[2]
    
    # All fields must be fill
    if title == '' or caption == '' or photo == '':
        return 'empty'
    
    # User's new album title must be unique
    if duplicate_title(title):
        return 'duplicate title'
    
    photo_src ='/static/images/' + album_info[2]
    user_hash = request.cookies.get('user_hash')
    query = "select id from users_info where user_hash = ?"
    user_id = db.execute(query, (user_hash,)).fetchone()[0]
    
    # Add new album to database
    query = 'insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)'
    db.execute(query ,(user_id, photo_src, title,caption,))
    return 'True'


# Get user albums when login was successful
@app.route('/albums', methods=['GET','POST'])
@user_mng.user_required
def _albums():
    titles=[]
    albumsinfo=[]
    user_hash = request.cookies.get('user_hash')
    
    query = "select id from users_info where user_hash = ?"
    user_id = db.execute(query, (user_hash,)).fetchone()[0]
    
    # get title, info, photo src
    query = "select title,info,src from users_photo where user_id = ?"
    albums_info = db.execute(query,(user_id,)).fetchall()
    for i in albums_info:
        
        # From each album, it takes only the first record stored in the database.        
        # Because it is defined in the structure of the database that
        # the first photo of each album is the album cover.
        if i[0] in titles:
            continue
        titles.append(i[0])        
        albumsinfo.append(list(i))
    return albumsinfo


# Add photo to user selected album
@app.route('/add_photo_to_album', methods=['GET','POST'])
@user_mng.user_required
def _add_photo_to_album():
    user_hash = request.cookies.get('user_hash')
    query = "select id from users_info where user_hash = ?"
    user_id = db.execute(query, (user_hash,)).fetchone()[0]
    
    # Get album_title and photo_name(src)
    data_request = ["album_title" , "photo_name"]
    user_info = user_mng.get_user_info(data_request)
    
    src = '/static/images/' + user_info[1]
    user_info = {"album_title":user_info[0] , "photo_name":user_info[1] ,"src":src}
    
    query = "select title,info,src fr   om users_photo where user_id = ?"
    album_photos = db.execute(query , (user_id,user_info["album_title"],user_info["src"],)).fetchall()
    
    # Add photos to the album
    photos=[]
    for i in album_photos:
        photos.append(i[0])
    
    # photos[0] is the album cover photo
    return photos[1:]

# Get user album photos
@app.route('/albumphotos', methods=['GET','POST'])
@user_mng.user_required
def _albumphotos():
    photos=[]
    user_hash = request.cookies.get('user_hash')
    
    query = "select id from users_info where user_hash = ?"
    user_id = db.execute(query, (user_hash,)).fetchone()[0]
    
    data_request = ["album_title"]
    title = user_mng.get_user_info(data_request)[0]
    
    query = "select src from users_photo where user_id = ? and title = ?"
    album_photos = db.execute(query,(user_id,title,)).fetchall()
    for i in album_photos:
        photos.append(i[0])
    return photos[1:]
    
# When user want to signout the account
@app.route('/sign-out', methods=['GET'])
def _signout():
    session['logged_in'] = False
    session['email']= False
    resp = make_response('True')
    resp.set_cookie('user_hash', '', max_age=0)
    return resp

# To accept the link confirmation request
@app.route('/confirm', methods=['GET'])
def _check_confirm():
    return email_mng.check_confirm_email()
	

@app.route('/signup', methods=['GET','POST'])
def _signup():
    data_request = ["fullname" , "email" , "password" , "confirm_password"]
    user_info = user_mng.get_user_info(data_request)
    user_info = { "fullname":user_info[0] , "email":user_info[1] , "password":user_info[2] , "confirm_password":user_info[3]}
    return user_mng.signup(user_info)


@app.route('/signin' ,methods=['GET' , 'POST'])
# @app.route('/' ,methods=['GET' , 'POST'] )
def _signin():
    user_hash = request.cookies.get('user_hash')
    if user_hash is None:
        try:
            info=["email","password"]
            user_info = user_mng.get_user_info(info)
            user_info = {"email":user_info[0] , "password":user_info[1]}
            return(user_mng.signin(user_info))
        except:
            return render_template('index.html')
    query = "select email from users_info where user_hash = ?"
    email = db.execute(query ,(user_hash,)).fetchone()[0]
    session['logged_in'] = True
    session['email'] = email
    return 'user1'
        
        
@app.route('/' ,methods=['GET' , 'POST'] )
def index():
    return render_template('index.html')

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000" , debug=True)
