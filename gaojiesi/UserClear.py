from config.db import events,users
from datetime import datetime

user_list = []
#for elem in events.find({'Event':'subscribe'}):
    #user_list.append(elem['FromUserName'])
#user_list = list(set(user_list))
#print len(user_list)
for elem in users.find():
    user_list.append(elem['user_id'])
user_list = list(set(user_list))
print len(user_list)
count = 0
for elem in user_list:
    curs = events.find({'FromUserName':elem,'Event':'subscribe'}).count()
    curt = events.find({'FromUserName':elem,'Event':'unsubscribe'}).count()
    #if curt > 1 or curs > 1:
        #users.remove({'user_id':elem})
    if curt > curs:
        count += 1
print count