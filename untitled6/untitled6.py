from flask import Flask, render_template, request, session
import mysql.connector
import datetime
import base64

import os
import json

app = Flask(__name__)
db = mysql.connector.connect(user='root', host='127.0.0.1', password='jerry791201', database='proj1')


def excuteQuery(sql):
    cursor = db.cursor()
    query = (sql)
    cursor.execute(query)
    data = []
    for info in cursor:
        data.append(info)
    db.commit()
    cursor.close()

    return data


@app.route('/')
def homepage():
    print(os.path.abspath('.'))
    return render_template('homepage.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':  # If a post request is detected
        loginForm = request.form  # Get form from request
        print(loginForm)
        username = loginForm['userid']
        pwd = loginForm['pwd']
        sql = "select * from users u where u.user_id='" + username + "' and password='" + pwd + "'"
        print(sql)
        user = excuteQuery(sql)
        if user:
            session['user_id'] = username
            return render_template('homepage.html', user=user)
        else:
            return render_template('error.html', error=1)
    else:  # If a get request is detected
        return render_template('login.html')


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        signupForm = request.form
        print(signupForm)
        user_id = signupForm['userid']
        pwd = signupForm['pwd']
        first_name = signupForm['firstname']
        last_name = signupForm['lastname']
        email = signupForm['email']
        date_of_birth = signupForm['birth']
        hometown = signupForm['hometown']
        gender = signupForm['gender']
        sql = "insert into users(user_id, first_name,last_name,email,date_of_birth,hometown,gender,password) values ('%s', '%s','%s','%s','%s','%s',%s,'%s')" % \
              (user_id, first_name, last_name, email, date_of_birth, hometown, gender, pwd)
        print(sql)
        sql1 = "select * from users u where u.user_id='" + user_id + "'"
        user = excuteQuery(sql1)
        if user:
            return render_template('error.html', error=2)
        else:
            excuteQuery(sql)
            sql2 = "select * from users u where u.user_id='" + user_id + "' and password='" + pwd + "'"
            user = excuteQuery(sql2)
            print(user)
            return render_template('homepage.html', user=user)
    else:
        return render_template('registration.html')


@app.route('/login/personal/', methods=['POST', 'GET'])
def personal():
    print("personal")
    if request.method == 'GET':  # If a post request is detected
        if 'user_id' in session:
            user_id = session['user_id']
        sql = "select * from friends f where f.user_id1='" + user_id + "' or f.user_id2='" + user_id + "'"
        sql1 = "select * from users u where u.user_id='" + user_id + "'"
        user = excuteQuery(sql1)
        friends = excuteQuery(sql)
        print(friends)
        sql2 = "select * from albums a where a.user_id='" + user_id + "'"
        albums = excuteQuery(sql2)
        print(albums)
        suggest_friend = recommendFriends(user_id)
        return render_template('personal.html', user=user, friends=friends, albums=albums,
                               suggest_fri_list=suggest_friend)


@app.route('/addAlbum/', methods=['POST', 'GET'])
def addAlbum():
    print('enter addAlbum')
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        date_of_creation = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addAlbumForm = request.form
        name = addAlbumForm['name']
        sql = "insert into albums(name,date_of_creation,user_id) values ('%s','%s','%s') ;" % (
        name, date_of_creation, user_id)
        excuteQuery(sql)
        sql1 = "SELECT @@IDENTITY as album_id"
        album_id = excuteQuery(sql1)
        print(album_id[0][0])
        sql2 = "select * from albums a where a.album_id= %d" % (album_id[0][0])
        album = excuteQuery(sql2)
        sql3 = "select * from photos p where p.album_id= %d" % (album_id[0][0])
        photo = excuteQuery(sql3)
        return render_template('album.html', user_id=user_id, album=album, photo=photo, base64=base64)


@app.route('/album/', methods=['POST', 'GET'])
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


@app.route('/album/addPhoto', methods=['POST', 'GET'])
def addPhoto():
    print('enter addPhoto')
    if request.method == "POST":
        if 'user_id' in session:
            user_id = session['user_id']
        photoForm = request.form
        album_id = photoForm['album_id']
        print(album_id)
        caption = photoForm['caption']
        print(caption)
        photoFile = request.files['photo']
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        dir = ROOT_DIR + '\static\img'
        sql0 = "select max(p.photo_id) from photos p"
        pp = excuteQuery(sql0)
        fn = pp[0][0] + 1
        print(fn)
        if photoFile:
            filename = str(fn) + '.' + photoFile.filename.rsplit('.', 1)[1]
            print(filename)
            path = '/static/img/' + filename
            photoFile.save(dir + '\\' + filename)
        sql = "insert into photos(caption,path,album_id) values ('%s','%s','%s') ;" % (
            caption, path, album_id)
        print(sql)
        excuteQuery(sql)
        sql2 = "select * from albums a where a.album_id= %s" % (album_id)
        album = excuteQuery(sql2)
        sql3 = "select * from photos p where p.album_id= %s" % (album_id)
        photo = excuteQuery(sql3)
        return render_template('album.html', user_id=user_id, album=album, photo=photo)
    else: # request.method =="GET":
        toprint="/album/addPhoto"
        return render_template('tmp.html', toprint=toprint)

@app.route('/photo/', methods=['POST', 'GET'])
def photo():
    if request.method == "GET":
        photo_id = request.args.get('photo_id')

        info_dict = getPhotoRequire(photo_id)
        #return render_template('tmp.html', toprint='called to photo')
        return render_template('photo.html', photo_id=photo_id,
                                img_path=info_dict['img_path'],
                               comments=info_dict['all_comments'],
                                likes=info_dict['likes'])

def getPhotoRequire(photo_id):
    sql = 'select user_id, content from comments where photo_id = {0}'.format(photo_id)
    all_comments = excuteQuery(sql)
    for que in all_comments:
        print(que[0], ' says: ', que[1])
    sql = 'select path from photos where photo_id = {0}'.format(photo_id)
    img_path = excuteQuery(sql)
    img_path = img_path[0][0]
    sql = 'select user_id from likes where photo_id = {0}'.format(photo_id)
    likes = excuteQuery(sql)
    return {'img_path':img_path, 'all_comments':all_comments,'likes':likes}


@app.route('/addComment/', methods=['POST', 'GET'])
def addComment():
    if request.method == "POST":
        print('enter addComment post')
        if 'user_id' in session:
            user_id = session['user_id']
        req_form = request.form
        photo_id = req_form['photo_id']
        sql = 'select album_id from photos where photo_id={0}'.format(photo_id)
        album_id = excuteQuery(sql)[0][0]
        sql = 'select user_id from albums where album_id={0}'.format(album_id)
        owner_id = excuteQuery(sql)[0][0]
        if owner_id != user_id:
            content = req_form['content']
            date_of_comment = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'insert into comments(content,date_of_comment,user_id,photo_id) ' \
                  'values (\'{0}\',\'{1}\',\'{2}\',\'{3}\');'.format(content, date_of_comment, user_id,
                   photo_id)
            excuteQuery(sql)
            info_dict = getPhotoRequire(photo_id)
            # return render_template('tmp.html', toprint='called to photo')
            return render_template('photo.html', photo_id=photo_id,
                                   img_path=info_dict['img_path'],
                                   comments=info_dict['all_comments'],
                                   likes=info_dict['likes'])
        else: #TODO, user cannot leave comment on his own photo
            #do something
            print('not allowed to comment on your own photo')

@app.route('/addLike/', methods=['POST', 'GET'])
def addLike():
    if request.method == "POST":
        print('enter addLike post')
        if 'user_id' in session:
            user_id = session['user_id']
        req_form = request.form
        photo_id = req_form['photo_id']
        sql = 'select user_id from likes where photo_id={0}'.format(photo_id)
        print(sql)
        like_users = excuteQuery(sql)[0][0]
        sql = 'select album_id from photos where photo_id={0}'.format(photo_id)
        album_id = excuteQuery(sql)[0][0]
        sql = 'select user_id from albums where album_id={0}'.format(album_id)
        owner_id = excuteQuery(sql)[0][0]
        if user_id in like_users:
            message = 'You already liked this photo'
        elif user_id == owner_id:
            message = 'Owner cannot likes their own photo'
        else:
            sql = 'insert into likes(user_id,photo_id) values (' \
                  '\'{0}\',\'{1}\');'.format(user_id, photo_id)
            excuteQuery(sql)
            message = ''

        info_dict = getPhotoRequire(photo_id)
        # return render_template('tmp.html', toprint='called to photo')
        return render_template('photo.html', photo_id=photo_id,
                               img_path=info_dict['img_path'],
                               comments=info_dict['all_comments'],
                               likes=info_dict['likes'], message=message)


def getFriendList(user_id):
    sql = 'select ' \
          'case f.user_id1 ' \
          '  when \'{0}\' then f.user_id2 ' \
          '  else f.user_id1 ' \
          'end ' \
          'from friends f ' \
          'where f.user_id1 = \'{1}\' or f.user_id2 = \'{2}\''.format(
        user_id, user_id, user_id)
    print(sql)
    friend_list = excuteQuery(sql)
    friend_list = [x[0] for x in friend_list]
    return friend_list

def recommendFriends(user_id):
    user_friend_list = getFriendList(user_id)
    hash_cnt = {}
    for f1 in user_friend_list:
        fri_of_friend = getFriendList(f1)
        for f2 in fri_of_friend:
            if f2 not in user_friend_list and f2 != str(user_id):
                if f2 in hash_cnt:
                    hash_cnt[f2]=hash_cnt[f2]+1
                else:
                    hash_cnt[f2]=1

    suggest_fri_list = list(hash_cnt.items())
    suggest_fri_list = sorted(suggest_fri_list, key=lambda x: x[1], reverse=True)
    suggest_fri_list = [x for x in suggest_fri_list if x[1]>=2]
    return suggest_fri_list


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True, use_debugger=False)
