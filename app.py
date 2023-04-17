import json
import secrets
from flask import Flask, request, redirect, render_template, session
import email_management as email_mng
import user_management as user_mng
import db_management as db


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex()


@user_mng.user_required
def duplicate_title(title):
    email = session['email']
    user_id = db.get_user_id(email)
    titles = db.get_titles(user_id)
    if titles == False:
        return False
    for tit in titles:            
        if title==tit[0]:                
            return True
    return False


@app.route('/add-album', methods=['GET','POST'])
@user_mng.user_required
def _add_album():
    album_info = request.data.decode('utf-8')
    album_info = json.loads(album_info)
    title = album_info["title"]
    caption = album_info["info"]
    photo = album_info["photo"]
    photo_src ='/static/images/' + photo
    try:
        user_email = session['email']        
        user_id = db.get_user_id(user_email)
    except:
        redirect('/signin')
    
    if title == '' or caption == '' or photo == '':
        return 'empty'
    if duplicate_title(title):
        return 'duplicate title'
    db.add_album(user_id, photo_src, title,caption)
    return 'True'


@app.route('/albums', methods=['POST'])
@user_mng.user_required
def _albums():
    titles=[' ']
    albumsinfo=[]
    email = session['email']
    user_id = db.get_user_id(email)
    albums_info = db.get_albums(user_id)
    for i in albums_info:
        if i[0] in titles:
            continue
        titles.append(i[0])        
        albumsinfo.append(list(i))
    return albumsinfo


@app.route('/add_photo_to_album', methods=['GET','POST'])
@user_mng.user_required
def _add_photo_to_album():
    photos=[]
    email = session['email']
    user_id = db.get_user_id(email)
    album_title = request.data.decode('utf-8')
    album_title = json.loads(album_title)
    title = album_title["album_title"]
    photo_name = album_title["photo_name"]
    src = '/static/images/' + photo_name
    album_photos = db.add_photo_to_album(user_id,title,src)
    for i in album_photos:
        photos.append(i[0])
    return photos[1:]


@app.route('/albumphotos', methods=['GET','POST'])
@user_mng.user_required
def _albumphotos():
    photos=[]
    email = session['email']
    user_id = db.get_user_id(email)
    album_title = request.data.decode('utf-8')
    album_title = json.loads(album_title)
    title = album_title["album_title"]    
    album_photos = db.get_album_photos(user_id,title)
    for i in album_photos:
        photos.append(i[0])
    return photos[1:]
    

@app.route('/sign-out', methods=['GET'])
def _signout():
    session['logged_in'] = False
    session['email']= False
    return 'True'


@app.route('/confirm', methods=['GET'])
def _check_confirm():
    return email_mng.check_confirm_email()
	

@app.route('/signup', methods=['GET','POST'])
def _signup():
    user_info = request.data.decode('utf-8')
    user_info = json.loads(user_info)
    fullname = user_info["fullname"]
    email = user_info["email"]
    password = user_info["password"]
    repassword = user_info["confirm_password"]
    info={
        'fullname':fullname,
        'email':email,
        'password':password,
        'repassword':repassword
    }
    return user_mng.signup(info)


@app.route('/signin' ,methods=['GET' , 'POST'])
@app.route('/' ,methods=['GET' , 'POST'] )
def _signin():
    try :
        user_info = request.data.decode('utf-8')
        user_info = json.loads(user_info)
        email = user_info["email"]
        password = user_info["password"]
        info={        
            'email':email,
            'password':password,        
        }
        return(user_mng.signin(info))  
    except:
        return render_template('index.html')
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000" , debug=True)
