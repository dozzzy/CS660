import mysql.connector

db = mysql.connector.connect(user='root', host='127.0.0.1', password='jerry791201', database='new_proj1')

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

def youMayLike(user_id):
    #used_id is the login user
    tag_n_count, all_my_photos = getMyMostUsedTags(user_id) #format:(tag, count)
    all_my_photos = [x[0] for x in all_my_photos]
    tag_n_count= sorted(tag_n_count, key=lambda x: x[1], reverse=True) #ties break as python impl
    target_tags = tag_n_count[0:min(len(tag_n_count),5)-1]

    # query candidate photos
    where_condition = str()
    for tag in target_tags:
        where_condition += ' or a.tag=\'{0}\''.format(tag[0])
    where_condition = where_condition[4:]
    sql = 'select distinct a.photo_id ' \
          'from associate a ' \
          'where {0} '.format(where_condition)
    candidate_photos = excuteQuery(sql)
    candidate_photos = [x[0] for x in candidate_photos if x[0] not in all_my_photos]

    tagMatchResult = tagMatch(candidate_photos, target_tags)
    sorted_tagMatch = sorted(tagMatchResult, key=lambda y: (y[1],y[2]), reverse=True)
    return sorted_tagMatch

def getMyMostUsedTags(user_id):
    sql = 'select a.album_id ' \
          'from albums a ' \
          'where a.user_id = \'{0}\''.format(user_id)
    all_my_albums = excuteQuery(sql)
    # generate where condition to find all my photos
    where_condition = str()
    for album_id in all_my_albums:
        where_condition += ' or p.album_id={0}'.format(album_id[0])
    where_condition = where_condition[4:]
    sql = 'select p.photo_id ' \
          'from photos p ' \
          'where {0}'.format(where_condition)

    all_my_photos = excuteQuery(sql)
    # generate where condition to find all my tags and # of usages
    where_condition = str()
    for photo_id in all_my_photos:
        where_condition += ' or a.photo_id={0}'.format(photo_id[0])
    where_condition = where_condition[4:]
    sql = 'select a.tag, count(*) ' \
          'from associate a ' \
          'where {0} ' \
          'group by a.tag '.format(where_condition)
    my_tags_n_count = excuteQuery(sql)
    return my_tags_n_count, all_my_photos

def tagMatch(candidate_photo_id, target_tags):
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

if __name__ == '__main__':
    youMayLike(12)