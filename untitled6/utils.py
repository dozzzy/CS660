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
    target_tags = tag_n_count[0:min(len(tag_n_count),5)] # tags might less than 5

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

    # sorted_tagMatch format:{photo_id, # of matched tag, -(# of unmatched )}
    if not candidate_photos:
        sorted_tagMatch = []
        print('no photo to recommend')
    else:
        tagMatchResult = tagMatch(candidate_photos, target_tags)
        sorted_tagMatch = sorted(tagMatchResult, key=lambda y: (y[1],y[2]), reverse=True)
    return sorted_tagMatch

def getMyMostUsedTags(user_id):
    # first get all my photo, and then find most used tags in all my photos
    sql = 'select DISTINCT p.photo_id ' \
          'from albums a, users u, photos p ' \
          'where a.user_id = {0} and a.album_id = p.album_id'.format(user_id)
    print(sql)
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

if __name__ == '__main__':
    youMayLike(12)