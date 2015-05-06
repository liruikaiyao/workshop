from config.db import events,users,user_info
from datetime import datetime
import time


user_list = []
for elem in events.find({'Event':'subscribe'}):
    user_list.append(elem['FromUserName'])
user_list = list(set(user_list))
print len(user_list)
now_time = time.time()

#add subscribe time
#three tag: pic, text, event
#format: 'user_id':'', 'sub_time':'', 'unsub_time':'', 'event':''.

count = 0
for elem in user_list:
    user_dict = {}
    msg_time = events.find({'$and':[{'FromUserName':elem},{"Event":{"$ne": 'LOCATION'}}]}).count()
    curs = events.find_one({'$and':[{'FromUserName':elem},{'Event':'subscribe'}]})
    sub_time = int(curs['CreateTime'])
    curt = events.find_one({'$and':[{'FromUserName':elem},{'Event':'unsubscribe'}]})
    if curt == None:
        unsub_time = int(now_time)
        user_dict['observed'] = 0
    else:
        unsub_time = int(curt['CreateTime'])
        user_dict['observed'] = 1
    user_dict['user_id'] = elem
    user_dict['event_subscribe'] = sub_time
    user_dict['event_unsubscribe'] = unsub_time
    user_dict['event'] = msg_time

    try:
        user_dict['duration'] = abs(unsub_time-sub_time)
    except Exception,e:
        print e
        print unsub_time
        print sub_time
    check = user_info.find_one({'openid':elem})
    #if gender exists, set it, if not, set gender=0, which means gender unknow
    try:
        user_dict['gender'] = check['sex']
    except:
        user_dict['gender'] = 0
    try:
        users.insert(user_dict)
    except Exception,e:
        print e
