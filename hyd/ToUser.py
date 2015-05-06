from config.db import hyd_events,hyd_users,after_users
import time


user_list = []
hyd_events.create_index('FromUserName')
hyd_events.create_index('Event')
hyd_users.create_index('openid')
for elem in hyd_events.find({'Event':'subscribe'}):
    user_list.append(elem['FromUserName'])
user_list = list(set(user_list))
print len(user_list)
now_time = time.time()

#add subscribe time
#three tag: pic, text, event
#format: 'user_id':'', 'sub_time':'', 'unsub_time':'', 'event':''.

count = 0
time_block = []
for elem in user_list:
    user_dict = {}
    msg_time = hyd_events.find({'$and':[{'FromUserName':elem},{"Event":{"$ne": 'LOCATION'}}]}).count()
    cursor = hyd_events.find({'FromUserName':elem})
    for item in cursor:
        time_block.append(item['CreateTime'])
    earlist = min(time_block)
    latest = max(time_block)
    sub_time = int(earlist)
    curt = hyd_events.find_one({'$and':[{'FromUserName':elem},{'Event':'unsubscribe'}]})
    if curt == None:
        unsub_time = int(now_time)
        user_dict['observed'] = 0
    else:
        unsub_time = int(latest)
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
    check = hyd_users.find_one({'openid':elem})
    #if gender exists, set it, if not, set gender=0, which means gender unknow
    try:
        user_dict['gender'] = check['sex']
    except:
        user_dict['gender'] = 0
    try:
        after_users.insert(user_dict)
    except Exception,e:
        print e
