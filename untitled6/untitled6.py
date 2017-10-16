
from flask import Flask, render_template, request, session
import mysql.connector
import datetime
import base64

import os
import json
app = Flask(__name__)
db = mysql.connector.connect(user='root', host='127.0.0.1', password='1111', database='test')

def excuteQuery(sql):
    cursor=db.cursor()
    query=(sql)
    cursor.execute(query)
    data=[]
    for info in cursor:
        data.append(info)
    db.commit()
    cursor.close()

    return data


@app.route('/')
def homepage():
	print(os.path.abspath('.'))
	return render_template('homepage.html')

@app.route('/login/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':  # If a post request is detected
        loginForm = request.form  # Get form from request
        print(loginForm)
        username=loginForm['userid']
        pwd=loginForm['pwd']
        sql="select * from users u where u.user_id='"+username+"' and password='"+pwd+"'"
        print(sql)
        user=excuteQuery(sql)
        if user:
            session['user_id']=username
            return render_template('homepage.html', user=user)
        else:
            return render_template('error.html' , error=1)
    else:  # If a get request is detected
        return render_template('login.html')

@app.route('/signup/', methods = ['POST', 'GET'])
def signup():
    if request.method=='POST':
        signupForm=request.form
        print(signupForm)
        user_id=signupForm['userid']
        pwd=signupForm['pwd']
        first_name=signupForm['firstname']
        last_name=signupForm['lastname']
        email=signupForm['email']
        date_of_birth=signupForm['birth']
        hometown=signupForm['hometown']
        gender=signupForm['gender']
        sql = "insert into users(user_id, first_name,last_name,email,date_of_birth,hometown,gender,password) values ('%s', '%s','%s','%s','%s','%s',%s,'%s')" % \
              (user_id,first_name,last_name,email,date_of_birth,hometown,gender,pwd)
        print(sql)
        sql1="select * from users u where u.user_id='"+user_id+"'"
        user=excuteQuery(sql1)
        if user:
            return render_template('error.html', error=2)
        else:
            excuteQuery(sql)
            sql2 = "select * from users u where u.user_id='" + user_id + "' and password='" + pwd + "'"
            user=excuteQuery(sql2)
            print(user)
            return render_template('homepage.html', user=user)
    else:
        return render_template('registration.html')

@app.route('/login/personal/', methods = ['POST', 'GET'])
def personal():
    print("personal")
    if request.method == 'GET':  # If a post request is detected
        if 'user_id' in session:
            user_id=session['user_id']
        sql="select * from friends f where f.user_id1='"+user_id+"' or f.user_id2='"+user_id+"'"
        sql1 = "select * from users u where u.user_id='" + user_id + "'"
        user=excuteQuery(sql1)
        friends=excuteQuery(sql)
        print(friends)
        sql2="select * from albums a where a.user_id='"+user_id+"'"
        albums=excuteQuery(sql2)
        print(albums)
        return render_template('personal.html', user=user, friends=friends, albums=albums)

@app.route('/addAlbum/', methods=['POST','GET'])
def addAlbum():
    if request.method == 'POST':

        if 'user_id' in session:
            user_id=session['user_id']
        date_of_creation=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addAlbumForm=request.form
        name=addAlbumForm['name']
        sql="insert into albums(name,date_of_creation,user_id) values ('%s','%s','%s') ;" % (name,date_of_creation,user_id)
        excuteQuery(sql)
        sql1="SELECT @@IDENTITY as album_id"
        album_id=excuteQuery(sql1)
        print(album_id[0][0])
        sql2="select * from albums a where a.album_id= %d" % (album_id[0][0])
        album=excuteQuery(sql2)
        sql3="select * from photos p where p.album_id= %d" % (album_id[0][0])
        photo=excuteQuery(sql3)
        return render_template('album.html',user_id=user_id,album=album,photo=photo,base64=base64)

@app.route('/album/', methods=['POST','GET'])
def album():
    print("album start")
    album_id = request.args.get('album_id')
    print(album_id)
    if 'user_id' in session:
        user_id = session['user_id']
    sql2 = "select * from albums a where a.album_id= %s" % (album_id)
    album = excuteQuery(sql2)
    sql3 = "select * from photos p where p.album_id= %s" % (album_id)
    photo = excuteQuery(sql3)
    return render_template('album.html', user_id=user_id, album=album, photo=photo, base64=base64)

@app.route('/album/addPhoto', methods=['POST','GET'])
def addPhoto():
    if request.method=="POST":
        if 'user_id' in session:
            user_id=session['user_id']
        photoForm=request.form
        album_id=photoForm['album_id']
        print(album_id)
        caption=photoForm['caption']
        print(caption)
        photoFile=request.files['photo']
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        dir=ROOT_DIR+'\static\img'
        sql0="select max(p.photo_id) from photos p"
        pp=excuteQuery(sql0)
        fn=pp[0][0]+1
        print(fn)
        if photoFile:
            filename=str(fn)+ '.'+photoFile.filename.rsplit('.', 1)[1]
            print(filename)
            path='/static/img/'+filename
            photoFile.save(dir+'\\'+filename)
        sql = "insert into photos(caption,path,album_id) values ('%s','%s','%s') ;" % (
        caption, path, album_id)
        print(sql)
        excuteQuery(sql)
        sql2="select * from albums a where a.album_id= %s" % (album_id)
        album=excuteQuery(sql2)
        sql3="select * from photos p where p.album_id= %s" % (album_id)
        photo=excuteQuery(sql3)
        return render_template('album.html',user_id=user_id,album=album,photo=photo)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run()
