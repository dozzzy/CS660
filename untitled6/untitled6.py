
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
        sqlrf="select f.user_id2,count(f.user_id2) from friends f WHERE \
            user_id1 in (select f.user_id2 from friends f where f.user_id1='%s') \
            and user_id2<>'%s' \
            and user_id2 not in (select f.user_id2 from friends f where f.user_id1='%s') \
            GROUP BY(f.user_id2) \
            ORDER BY count(f.user_id2) DESC" % (user_id,user_id,user_id)
        rfriends=excuteQuery(sqlrf)
        return render_template('personal.html', user=user, friends=friends, albums=albums, rfriends=rfriends)

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

@app.route('/deleteAlbum/',methods=['POST','GET'])
def deleteAlbum():
    print('deleteAlbum start')
    album_id = request.args.get('album_id')
    if 'user_id' in session:
        user_id=session['user_id']
    sql0 = "delete from albums where album_id= %s" % (album_id)
    excuteQuery(sql0)
    sql = "select * from friends f where f.user_id1='" + user_id + "' or f.user_id2='" + user_id + "'"
    sql1 = "select * from users u where u.user_id='" + user_id + "'"
    user = excuteQuery(sql1)
    friends = excuteQuery(sql)
    sql2 = "select * from albums a where a.user_id='" + user_id + "'"
    albums = excuteQuery(sql2)
    return render_template('personal.html', user=user, friends=friends, albums=albums)

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
        tags=photoForm['tags']
        print(tags)
        tag=[]
        tag=tags.split(' ')
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

        for i in range(len(tag)):
            if tag[i]:
                tagsql0="select * from tags t where t.tag='%s'" % (tag[i])
                tt=excuteQuery(tagsql0)
                if tt==[]:
                    print('add tag')
                    tagsql1="insert into tags(tag) values ('%s')" % (tag[i])
                    excuteQuery(tagsql1)
                tagsql="insert into associate(tag,photo_id) values('%s',%d)" % (tag[i],fn)
                print(tagsql)
                excuteQuery(tagsql)

        sql2="select * from albums a where a.album_id= %s" % (album_id)
        album=excuteQuery(sql2)
        sql3="select * from photos p where p.album_id= %s" % (album_id)
        photo=excuteQuery(sql3)
        return render_template('album.html',user_id=user_id,album=album,photo=photo)

@app.route('/deletePhoto', methods=['POST','GET'])
def deletePhoto():
    if request.method=="GET":
        print('deleteAlbum start')
        photo_id = request.args.get('photo_id')
        sql="select * from photos p where p.photo_id= %s" % (photo_id)
        album_id=excuteQuery(sql)[0][2]
        if 'user_id' in session:
            user_id = session['user_id']
        sql0 = "delete from photos where photo_id= %s" % (photo_id)
        excuteQuery(sql0)
        sql2="select * from albums a where a.album_id= %s" % (album_id)
        album=excuteQuery(sql2)
        sql3="select * from photos p where p.album_id= %s" % (album_id)
        photo=excuteQuery(sql3)
        return render_template('album.html',user_id=user_id,album=album,photo=photo)

@app.route('/userProfile',methods=['GET'])
def userProfile():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id=''
    ouser_id=request.args.get('ouser_id')
    sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
    ouser = excuteQuery(sql1)
    sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
    albums = excuteQuery(sql2)
    sql3 = "select * from friends f where (f.user_id1= '%s' and f.user_id2= '%s') or (f.user_id1= '%s' and f.user_id2= '%s')" % (user_id,ouser_id,ouser_id,user_id)
    print(sql3)
    addf=excuteQuery(sql3)
    return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)

@app.route('/addFriend',methods=['GET'])
def addfriend():
    if 'user_id' in session:
        user_id = session['user_id']
    ouser_id=request.args.get('ouser_id')
    sql="insert into friends(user_id1,user_id2) value('%s','%s')" % (user_id,ouser_id)
    sqlt="insert into friends(user_id1,user_id2) value('%s','%s')" % (ouser_id,user_id)
    excuteQuery(sql)
    excuteQuery(sqlt)
    sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
    ouser = excuteQuery(sql1)
    sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
    albums = excuteQuery(sql2)
    addf=1
    return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)
@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=='POST':
        if 'user_id' in session:
            user_id=session['user_id']
        searchForm=request.form
        searchType=searchForm['searchType']
        searchContent=searchForm['searchContent']
        if searchType=='users':
            ouser_id=searchContent
            sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
            ouser = excuteQuery(sql1)
            sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
            albums = excuteQuery(sql2)
            sql3 = "select * from friends f where (f.user_id1= '%s' and f.user_id2= '%s') or (f.user_id1= '%s' and f.user_id2= '%s')" % (
            user_id, ouser_id, ouser_id, user_id)
            print(sql3)
            addf = excuteQuery(sql3)
            return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)
        if searchType=='tags':
            tags=searchContent
            tag=[]
            tag=tags.split(' ')
            sql=['' for i in range(len(tag))]
            if tag[0]:
                sql[0] = "(select a.photo_id from associate a where a.tag='%s')" % (tag[0])
            print(sql[0])
            fsql = sql[0]
            for i in range(1, len(tag)):
                if tag[i]:
                    sql[i] = "(select a.photo_id from associate a where a.tag='%s' and photo_id in %s )" % (tag[i], sql[i - 1])
                else:
                    sql[i] = sql[i - 1]
                fsql = sql[i]
                #print(fsql)
            print(fsql)
            photo_ids=excuteQuery(fsql)
            return render_template('tagsSearchResult.html', photo_ids=photo_ids)
        if searchType=='comments':
            print('comments undone')

@app.route('/myPhotoSearch/',methods=['POST','GET'])
def myPhotoSearch():
    if request.method=='POST':
        if 'user_id' in session:
            user_id=session['user_id']
        mySearchForm=request.form
        tags=mySearchForm['tags']
        tag = []
        tag = tags.split(' ')
        sql = ['' for i in range(len(tag))]
        if tag[0]:
            sql[0] = "(select a.photo_id FROM albums aa,photos p,associate a WHERE aa.album_id=p.album_id and p.photo_id=a.photo_id and aa.user_id='%s' and a.tag='%s')" % (user_id,tag[0])
        print(sql[0])
        fsql = sql[0]
        for i in range(1, len(tag)):
            if tag[i]:
                sql[i] = "(select a.photo_id from associate a where a.tag='%s' and photo_id in %s )" % (
                tag[i], sql[i - 1])
            else:
                sql[i] = sql[i - 1]
            fsql = sql[i]
            # print(fsql)
        print(fsql)
        photo_ids = excuteQuery(fsql)
        return render_template('myPhoto.html', photo_ids=photo_ids)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run()
