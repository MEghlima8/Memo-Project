import sqlite3
from flask import session

# Get confirmation link and confirm it
def confirm_email(link):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()    
    cur.execute("UPDATE users_info SET active=?  where link=?",
                (1,link))
    x = cur.fetchone()
    conn.commit()
    return 'True'


# Getback users info
def get_users():
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    tuple_of_users = cur.execute("select email,password,active from users_info")
    conn.commit()
    return tuple_of_users
    
    
# Signup user
def do_signup(info):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute('insert into users_info (fullname,email,password,active,link) values(? , ? , ? , 0 , ?)',
                (info['fullname'], info['email'], info['password'], info['link']))
    conn.commit()
    return 'True'


# Getback user is using user email
def get_user_id():
    email = session['email']
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    user_id = cur.execute(
        "select id from users_info where email = ?", (email,)).fetchone()[0]
    conn.commit()
    return (user_id)


# Getback confirm links
def get_all_confirm_links():
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    links = cur.execute("select link from users_info")
    conn.commit()
    return links


# Check the user email is duplicate or not
def check_email_exist(email):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute("select email from users_info where email=?", (email,))
    x = cur.fetchone()
    conn.commit()
    return (x)


# Getback user album titles using user id
def get_titles(user_id):
    try:
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()
        titles = cur.execute(
            "select title from users_photo where user_id = ?", (user_id,)).fetchall()
        conn.commit()
        return titles
    except:
        conn.commit()
        return False
    
    
# Create new album to user
def add_album(user_id, photo_src, title,caption):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()    
    cur.execute('insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)',
                (user_id, photo_src, title,caption))
    conn.commit()
    return True


# Getback user album info
def get_albums(user_id):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    albums_info = cur.execute(
        "select title,info,src from users_photo where user_id = ?", (user_id,)).fetchall()
    conn.commit()
    return albums_info


# Add photo to define album 
def add_photo_to_album(user_id,title,src):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    album_info = cur.execute(
        "select info from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    
    # album caption
    album_info = album_info[0][0]
    
    album_photos = cur.execute('insert into users_photo (user_id,src,title,info) values(? , ? , ? , ?)',
                (user_id, src, title,album_info))
    
    album_photos = cur.execute(
        "select src from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    conn.commit()
    return album_photos
    

# Getback define album photos
def get_album_photos(user_id,title):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    album_photos = cur.execute(
        "select src from users_photo where user_id = ? and title = ?", (user_id,title)).fetchall()
    conn.commit()
    return album_photos
