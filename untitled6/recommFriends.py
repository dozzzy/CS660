import mysql.connector

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

def getFriendList(user_id):
    sql = 'select ' \
          'case f.user_id1 ' \
          '  when {0} then f.user_id2 ' \
          '  else f.user_id1 ' \
          'end ' \
          'from friends f ' \
          'where f.user_id1 = {1} or f.user_id2 = {2}'.format(
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

if __name__== '__main__':
    user_id = 3
    result_dict = recommendFriends(user_id)
