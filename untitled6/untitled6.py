from flask import Flask, render_template, request, session
import mysql.connector
import datetime
import base64

import os
import json

app = Flask(__name__)
db = mysql.connector.connect(user='root', host='127.0.0.1', password='1111', database='pa1')


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
    tag_n_count = findTop5Tags()
    user_n_contri = findTop10Contributor()
    if 'user_id' in session:
        user_id=session['user_id']
    else:
        user_id=0
    sql="select * from users u where u.user_id=%d " % (user_id)
    user=excuteQuery(sql)
    return render_template('homepage.html', top5tag=tag_n_count[:5], top10User=user_n_contri[:10],user=user)

@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.clear()
    tag_n_count = findTop5Tags()
    user_n_contri = findTop10Contributor()
    return render_template('homepage.html', top5tag=tag_n_count[:5], top10User=user_n_contri[:10])
@app.route('/logout/login/', methods=['POST', 'GET'])
@app.route('/login/', methods=['POST', 'GET'])
@app.route('/album/login', methods=['POST', 'GET'])
@app.route('/photo/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':  # If a post request is detected
        loginForm = request.form  # Get form from request
        print(loginForm)
        username = loginForm['userid']
        pwd = loginForm['pwd']
        sql = "select * from users u where u.email='" + username + "' and password='" + pwd + "'"
        print(sql)
        user = excuteQuery(sql)
        if user:
            session['user_id'] = user[0][0]
            tag_n_count = findTop5Tags()
            user_n_contri = findTop10Contributor()
            return render_template('homepage.html', user=user, top5tag=tag_n_count[:5],  top10User=user_n_contri[:10])
        else:
            return render_template('login.html', error=1)
    else:  # If a get request is detected
        return render_template('login.html')
@app.route('/photo/signup', methods=['POST', 'GET'])
@app.route('/album/signup', methods=['POST', 'GET'])
@app.route('/logout/signup', methods=['POST', 'GET'])
@app.route('/login/signup', methods=['POST', 'GET'])
@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        signupForm = request.form
        print(signupForm)
        pwd = signupForm['pwd']
        first_name = signupForm['firstname']
        last_name = signupForm['lastname']
        email = signupForm['email']
        date_of_birth = signupForm['birth']
        hometown = signupForm['hometown']
        gender = signupForm['gender']
        sql = "insert into users(first_name,last_name,email,date_of_birth,hometown,gender,password) values ( '%s','%s','%s','%s','%s',%s,'%s')" % \
              (first_name, last_name, email, date_of_birth, hometown, gender, pwd)
        print(sql)
        sql1 = "select * from users u where u.email='%s'" % (email)
        user = excuteQuery(sql1)
        if user:
            return render_template('registration.html', error=2)
        else:
            excuteQuery(sql)
            sql2 = "select * from users u where u.email= '%s'" % (email)
            user = excuteQuery(sql2)
            session['user_id']=user[0][0]
            print(user)
            tag_n_count = findTop5Tags()
            user_n_contri = findTop10Contributor()
            return render_template('homepage.html', user=user, top5tag=tag_n_count[:5],  top10User=user_n_contri[:10])
    else:
        return render_template('registration.html')

@app.route('/personal', methods=['POST', 'GET'])
@app.route('/photo/personal', methods=['POST', 'GET'])
@app.route('/album/personal', methods=['POST', 'GET'])
@app.route('/login/personal/', methods=['POST', 'GET'])
@app.route('/signup/personal/', methods=['POST', 'GET'])
def personal():
    print("personal")
    if request.method == 'GET':  # If a post request is detected
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id=0
        sql = "select * from friends f where f.user_id1=%d" % (user_id)
        sql1 = "select * from users u where u.user_id=%d" % (user_id)
        user = excuteQuery(sql1)
        friends = excuteQuery(sql)
        print(friends)
        sql2 = "select * from albums a where a.user_id=%d" % (user_id)
        albums = excuteQuery(sql2)
        print(albums)
        #rfriends = recommendFriends(user_id)
        sqlrf = "select f.user_id2,count(f.user_id2) from friends f WHERE \
                    user_id1 in (select f.user_id2 from friends f where f.user_id1='%d') \
                    and user_id2<>'%d' \
                    and user_id2 not in (select f.user_id2 from friends f where f.user_id1='%d') \
                    GROUP BY(f.user_id2) \
                    ORDER BY count(f.user_id2) DESC" % (user_id, user_id, user_id)
        rfriends = excuteQuery(sqlrf)

        #recommend photos
        rphotos = youMayLike(user_id)
        return render_template('personal.html', user=user, friends=friends, albums=albums,
                               rfriends=rfriends, rphotos=rphotos)


@app.route('/addAlbum', methods=['POST', 'GET'])
def addAlbum():
    print('enter addAlbum')
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        date_of_creation = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        addAlbumForm = request.form
        name = addAlbumForm['name']
        sql = "insert into albums(name,date_of_creation,user_id) values ('%s','%s','%d') ;" % (
        name, date_of_creation, user_id)
        excuteQuery(sql)
        sql1 = "SELECT @@IDENTITY as album_id"
        album_id = excuteQuery(sql1)
        print(album_id[0][0])
        sql2 = "select * from albums a where a.album_id= %d" % (album_id[0][0])
        album = excuteQuery(sql2)
        sql3 = "select * from photos p where p.album_id= %d" % (album_id[0][0])
        photo = excuteQuery(sql3)
        return render_template('album.html', user_id=user_id, album=album, photo=photo)


@app.route('/album/', methods=['POST', 'GET'])
def album():
    print("album start")
    album_id = request.args.get('album_id')
    print(album_id)
    if 'user_id' in session:
        user_id = int(session['user_id'])
    else:
        user_id = 0
    sql2 = "select * from albums a where a.album_id= %s" % (album_id)
    album = excuteQuery(sql2)
    sql3 = "select * from photos p where p.album_id= %s" % (album_id)
    photo = excuteQuery(sql3)
    return render_template('album.html', user_id=user_id, album=album, photo=photo, base64=base64)

@app.route('/deleteAlbum',methods=['POST','GET'])
def deleteAlbum():
    print('deleteAlbum start')
    album_id = request.args.get('album_id')
    if 'user_id' in session:
        user_id=session['user_id']
    sql0 = "delete from albums where album_id= %s" % (album_id)
    excuteQuery(sql0)
    sql = "select * from friends f where f.user_id1= %d" % (user_id)
    sql1 = "select * from users u where u.user_id= %d" % (user_id)
    user = excuteQuery(sql1)
    friends = excuteQuery(sql)
    sql2 = "select * from albums a where a.user_id= %d" % (user_id)
    albums = excuteQuery(sql2)
    return render_template('personal.html', user=user, friends=friends, albums=albums)

@app.route('/addPhoto', methods=['POST', 'GET'])
@app.route('/album/addPhoto', methods=['POST', 'GET'])
def addPhoto():
    if request.method=="POST":
        print('enter addPhoto post')
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
        print('photo added')
        for i in range(len(tag)):
            if tag[i]:
                tagsql0="select * from tags t where t.tag='%s'" % (tag[i])
                tt=excuteQuery(tagsql0)
                if tt==[]:
                    print('add tag')
                    tagsql1="insert into tags(tag) values ('%s')" % (tag[i])
                    excuteQuery(tagsql1)
                sql = 'select photo_id from photos where path=\'{0}\''.format(path)
                photo_id = excuteQuery(sql)[0][0]
                print('inserted photo id = '+str(photo_id))
                tagsql="insert into associate(tag,photo_id) values('%s',%d)" % (tag[i],photo_id)
                print(tagsql)
                excuteQuery(tagsql)

        sql2="select * from albums a where a.album_id= %s" % (album_id)
        album=excuteQuery(sql2)
        sql3="select * from photos p where p.album_id= %s" % (album_id)
        photo=excuteQuery(sql3)
        return render_template('album.html',user_id=user_id,album=album,photo=photo)
    else: # request.method =="GET":
        toprint="/album/addPhoto"
        return render_template('tmp.html', toprint=toprint)

@app.route('/userProfile',methods=['GET'])
def userProfile():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id=0
    ouser_id=request.args.get('ouser_id')
    sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
    ouser = excuteQuery(sql1)
    sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
    albums = excuteQuery(sql2)
    sql3 = "select * from friends f where (f.user_id1= '%d' and f.user_id2= '%s')" % (user_id,ouser_id)
    print(sql3)
    addf=excuteQuery(sql3)
    return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)


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

@app.route('/photo/', methods=['POST', 'GET'])
def photo():
    if request.method == "GET":
        if 'user_id' in session:
            user_id=session['user_id']
        else:
            user_id=0
        photo_id = request.args.get('photo_id')
        sql="select a.tag from associate a where a.photo_id=%s" % (photo_id)
        tags=excuteQuery(sql)
        info_dict = getPhotoRequire(photo_id)
        #return render_template('tmp.html', toprint='called to photo')
        return render_template('photo.html', photo_id=photo_id,
                                img_path=info_dict['img_path'],
                               comments=info_dict['all_comments'],
                                likes=info_dict['likes'],
                               user_id=user_id,tags=tags)

def getPhotoRequire(photo_id):
    sql = 'select user_id, content, date_of_comment from comments where photo_id = {0}'.format(photo_id)
    all_comments = excuteQuery(sql)
    #for que in all_comments:
    #    print(que[0], ' says: ', que[1])
    sql = 'select path from photos where photo_id = {0}'.format(photo_id)
    img_path = excuteQuery(sql)
    img_path = img_path[0][0]
    sql = 'select user_id from likes where photo_id = {0}'.format(photo_id)
    likes = excuteQuery(sql)
    return {'img_path':img_path, 'all_comments':all_comments,'likes':likes}


@app.route('/addFriend',methods=['GET'])
def addFriend():
    if 'user_id' in session:
        user_id = session['user_id']
    ouser_id=request.args.get('ouser_id')
    sql="insert into friends(user_id1,user_id2) value('%d','%s')" % (user_id,ouser_id)
    sqlt="insert into friends(user_id1,user_id2) value('%s','%d')" % (ouser_id,user_id)
    excuteQuery(sql)
    excuteQuery(sqlt)
    sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
    ouser = excuteQuery(sql1)
    sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
    albums = excuteQuery(sql2)
    addf=1
    return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)

@app.route('/addComment', methods=['POST', 'GET'])
def addComment():
    if request.method == "POST":
        print('enter addComment post')
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = 0
        req_form = request.form
        photo_id = req_form['photo_id']
        print(photo_id)
        sql = 'select album_id from photos where photo_id={0}'.format(photo_id)
        album_id = excuteQuery(sql)[0][0]
        sql = 'select user_id from albums where album_id={0}'.format(album_id)
        owner_id = excuteQuery(sql)[0][0]
        sql1 = "select a.tag from associate a where a.photo_id=%s" % (photo_id)
        tags = excuteQuery(sql1)
        print(owner_id)
        print(user_id)
        if owner_id != user_id:
            print('start insert comment')
            content = req_form['content']
            date_of_comment = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if user_id==0:
                user_id=''
            sql = 'insert into comments(content,date_of_comment,user_id,photo_id) ' \
                  'values (\'{0}\',\'{1}\',\'{2}\',\'{3}\');'.format(content, date_of_comment, user_id,
                   photo_id)
            print(sql)
            excuteQuery(sql)
            info_dict = getPhotoRequire(photo_id)

            # return render_template('tmp.html', toprint='called to photo')
            return render_template('photo.html', photo_id=photo_id,
                                   img_path=info_dict['img_path'],
                                   comments=info_dict['all_comments'],
                                   likes=info_dict['likes'],tags=tags,user_id=user_id)
        else:
            message = 'not allowed to comment on your own photo'
            info_dict = getPhotoRequire(photo_id)
            return render_template('photo.html', photo_id=photo_id,
                                   img_path=info_dict['img_path'],
                                   comments=info_dict['all_comments'],
                                   likes=info_dict['likes'], comment_message=message,tags=tags,user_id=user_id)

@app.route('/addLike', methods=['POST', 'GET'])
def addLike():
    if request.method == "POST":
        print('enter addLike post')
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id=0
        print('in addlike ur id = '+str(user_id))
        req_form = request.form
        photo_id = req_form['photo_id']
        sql = 'select user_id from likes where photo_id={0}'.format(photo_id)
        print(sql)
        like_users = excuteQuery(sql)
        like_users = [x[0] for x in like_users]
        print('user like this photo:',like_users)
        sql = 'select album_id from photos where photo_id={0}'.format(photo_id)
        album_id = excuteQuery(sql)[0][0]
        sql = 'select user_id from albums where album_id={0}'.format(album_id)
        owner_id = excuteQuery(sql)[0][0]
        sql1 = "select a.tag from associate a where a.photo_id=%s" % (photo_id)
        tags = excuteQuery(sql1)
        if user_id in like_users:
            message = 'You already liked this photo'
        elif user_id == owner_id:
            message = 'You cannot like your own photo'
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
                               likes=info_dict['likes'], like_message=message,tags=tags,user_id=user_id)


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=='POST':
        if 'user_id' in session:
            user_id=session['user_id']
        else:
            user_id =0
        searchForm=request.form
        searchType=searchForm['searchType']
        searchContent=searchForm['searchContent']

        if searchType=='users':
            ouser_id=searchContent
            sql1 = "select * from users u where u.user_id='" + ouser_id + "'"
            ouser = excuteQuery(sql1)
            sql2 = "select * from albums a where a.user_id='" + ouser_id + "'"
            albums = excuteQuery(sql2)
            sql3 = "select * from friends f where (f.user_id1= '%d' and f.user_id2= '%s') or (f.user_id1= '%s' and f.user_id2= '%d')" % (
            user_id, ouser_id, ouser_id, user_id)
            print(sql3)
            addf = excuteQuery(sql3)
            if ouser:
                return render_template('userProfile.html', ouser=ouser, user_id=user_id, albums=albums, addf=addf)
            else:
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
            return render_template('tagsSearchResult.html', photo_ids=photo_ids,tags=tags,user_id=user_id)
        if searchType=='comments':
            comments = searchContent
            print(comments)
            sql = 'select c.user_id, count(c.user_id) ' \
                  'from comments c ' \
                  'where c.content=\'{0}\' ' \
                  'group by c.user_id ' \
                  'order by count(c.user_id) DESC;'.format(comments)
            print(sql)
            match = excuteQuery(sql)
            print(match)
            return render_template('commentsSearchResult.html', match=match,comments=comments,user_id=user_id)
@app.route('/tagSearch',methods=['POST','GET'])
def tagSearch():
    if request.method=='GET':
        if 'user_id' in session:
            user_id=session['user_id']
        else:
            user_id =0
        tag = request.args.get('tag')
        sql = "(select a.photo_id from associate a where a.tag='%s')" % (tag)
        photo_ids = excuteQuery(sql)
        return render_template('tagsSearchResult.html', photo_ids=photo_ids,tags=tag,user_id=user_id)

@app.route('/myPhotoSearch',methods=['POST','GET'])
def myPhotoSearch():
    if request.method=='POST':
        if 'user_id' in session:
            user_id=session['user_id']
        else:
            user_id=0
        mySearchForm=request.form
        tags=mySearchForm['tags']
        ouser_id=mySearchForm['ouser_id']
        tag = []
        tag = tags.split(' ')
        sql = ['' for i in range(len(tag))]
        if tag[0]:
            sql[0] = "(select a.photo_id FROM albums aa,photos p,associate a WHERE aa.album_id=p.album_id and p.photo_id=a.photo_id and aa.user_id='%s' and a.tag='%s')" % (ouser_id,tag[0])
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
        return render_template('myPhoto.html', photo_ids=photo_ids,tags=tags,ouser_id=ouser_id,user_id=user_id)



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


def youMayLike(user_id):
    #used_id is the login user
    tag_n_count, all_my_photos = getMyMostUsedTags(user_id) #format:(tag, count)
    target_tags = tag_n_count[0:min(len(tag_n_count),5)] # tags might less than 5

    if tag_n_count:
        # query candidate photos with at least 1 most used tags
        where_condition = str()
        for tag in target_tags:
            where_condition += ' or a.tag=\'{0}\''.format(tag[0])
        where_condition = where_condition[4:]
        sql = 'select distinct a.photo_id ' \
              'from associate a ' \
              'where {0} '.format(where_condition)
        candidate_photos = excuteQuery(sql)
        # remove those photos of mine (no need to recommend your own photos)
        candidate_photos = [x[0] for x in candidate_photos if x[0] not in all_my_photos]
    else:
        candidate_photos = []

    # sorted_tagMatch format:{photo_id, # of matched tag, -(# of unmatched )}
    if not candidate_photos:
        sorted_tagMatch = []
    else:
        tagMatchResult = tagMatch(candidate_photos, target_tags)
        sorted_tagMatch = sorted(tagMatchResult, key=lambda y: (y[1],y[2]), reverse=True)
    return sorted_tagMatch

def getMyMostUsedTags(user_id):
    # first get all my photo, and then find most used tags in all my photos
    sql = 'select DISTINCT p.photo_id ' \
          'from albums a, users u, photos p ' \
          'where a.user_id = {0} and a.album_id = p.album_id'.format(user_id)
    all_my_photos = excuteQuery(sql)
    # generate where condition to find all my tags and # of usages
    where_condition = str()
    if not all_my_photos:
        my_tags_n_count = []
        all_my_photos = []
    else :
        for photo_id in all_my_photos:
            where_condition += ' or a.photo_id={0}'.format(photo_id[0])
        where_condition = where_condition[4:]
        sql = 'select a.tag, count(*) ' \
          'from associate a ' \
          'where {0} ' \
          'group by a.tag '.format(where_condition)
        my_tags_n_count = excuteQuery(sql)
        all_my_photos = [x[0] for x in all_my_photos]
        my_tags_n_count = sorted(my_tags_n_count, key=lambda x: x[1], reverse=True)  # ties break as python impl
    return my_tags_n_count, all_my_photos

def tagMatch(candidate_photo_id, target_tags):
    # query all tags related to candidate photo
    # and match each of them to the target_tag
    target_tags = [x[0] for x in target_tags]
    tagMatchResult = [] # save in tuple (photo_id,# matched tag, # mismatched)
    query_template = 'select a.tag from associate a where a.photo_id={0}'
    for photo_id in candidate_photo_id:
        sql = query_template.format(photo_id)
        candidate_photo_tags = excuteQuery(sql)
        match_cnt = 0
        mismatch_cnt = 0
        for tag in candidate_photo_tags:
            if tag[0] in target_tags:
                match_cnt += 1
            else:
                mismatch_cnt += 1;
        mismatch_cnt = -mismatch_cnt
        tagMatchResult.append((photo_id,match_cnt,mismatch_cnt))
    return tagMatchResult

def findTop5Tags():
    sql =  'select a.tag, count(*)' \
           'from associate a ' \
           'group by a.tag ' \
           'order by count(*) desc;'
    print(sql)
    tag_n_count = excuteQuery(sql)
    return tag_n_count

def findTop10Contributor():
    # first contribution # of comments of every user
    sql = 'select u.user_id, count(*) ' \
          'from users u, comments c ' \
          'where u.user_id = c.user_id ' \
          'group by u.user_id ';
    comm_contri = excuteQuery(sql)
    sql = 'select u.user_id, count(*) ' \
          'from albums a, users u, photos p ' \
          'where a.user_id = u.user_id and ' \
          ' p.album_id = a.album_id ' \
          'group by u.user_id'
    upload_contri = excuteQuery(sql)

    # build necessary vars.
    user_with_comm = {x[0] for x in comm_contri}
    user_with_photo = {x[0] for x in upload_contri}
    all_user_with_contri = user_with_comm | user_with_photo
    user_n_contri = []
    for user in all_user_with_contri:
        user_n_contri.append([user,0])

    # add contribution together
    for x in comm_contri:
        for y in user_n_contri:
            if y[0] == x[0]:
                y[1] = y[1]+x[1]
                continue
    for x in upload_contri:
        for y in user_n_contri:
            if y[0] == x[0]:
                y[1] = y[1] + x[1]
                continue
    user_n_contri = sorted(user_n_contri, key=lambda x:x[1], reverse=True)
    print(user_n_contri)
    return user_n_contri


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True, use_debugger=False)
