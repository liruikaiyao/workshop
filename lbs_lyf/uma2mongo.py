#coding=utf-8

from __future__ import division
from config.db import umav3,store_lyf,lyf,client
import numpy as np
import pandas as pd
import datetime
from collections import OrderedDict
import time
import pymongo

weixin_all = umav3['weixin']
lbs = lyf['lbs']
survival = lyf['survival']
weixin = lyf['weixin']

lyf_id = 'gh_60217269884e'

weixin_all.ensureIndex(('ToUserName',pymongo.ASCENDING))

for elem in weixin_all.find({'ToUserName':lyf_id}):
    weixin.insrt(elem)

weixin.ensureIndex([('FromUserName',pymongo.ASCENDING),('Event',pymongo.ASCENDING),('createTime',pymongo.DESCENDING)])

#user=[elem['FromUserName'] for elem in weixin.find()]
#user = list(set(user))


for elem in weixin.find({'Event':'LOCATION'},{'FromUserName':1,'Longitude':1,'Latitude':1,'createTime':1}):
    a=dict()
    a['lbs'] = [elem['Longitude'],elem['Latitude']]
    a['openid'] = elem['FromUserName']
    a['time'] = elem['createTime']
    lbs.insert(a)

lbs.ensureTndex([('lbs',pymongo.GEOSPHERE),('openid',pymongo.ASCENDING),('time',pymongo.ASCENDING)])


user_dict=OrderedDict()

for elem in weixin.find({},{'FromUserName':1,'createTime':1,'Event':1}).sort('createTime',-1):
    if elem['FromUserName'] in user_dict:
        user_dict[elem['FromUserName']].append(elem)
    else:
        user_dict[elem['FromUserName']]=list()
        user_dict[elem['FromUserName']].append(elem)




duration_dict={k:(v[0]-v[-1]).total_seconds() for k,v in user_dict.items()}




for k,v in user_dict.items():
    a=dict()
    a['openid'] = k
    a['duration'] = duration_dict[k]
    if 'Event' in v[0]:
        if v[0]['Event']=='unsubscribe':
            a['observed']=1
        else:
            a['observed']=0
    else:
        a['observed']=0
    survival.insert(a)


