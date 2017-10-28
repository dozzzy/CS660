temp="aa"
tag=[]
tag=temp.split(' ')
for i in range(len(tag)):
    if tag[i]:
        print(tag[i])
sql=[''for i in range(len(tag))]
if tag[0]:
    sql[0]="(select a.photo_id from associate a where a.tag='%s')" % (tag[0])
print (sql[0])
fsql=sql[0]
for i in range(1,len(tag)):
    if tag[i]:
        sql[i]="(select a.photo_id from associate a where a.tag='%s' and photo_id in %s )" % (tag[i],sql[i-1])
    else:
        sql[i]=sql[i-1]
    fsql=sql[i]
    print(fsql)
print(fsql)