import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', password='1111', database='test')

def excuteQuery(sql):
    cursor=db.cursor()
    query=(sql)
    cursor.execute(query)
    data=[]
    for info in cursor:
        data.append(info)
    cursor.close()

    return data

#db.close()