#coding=utf-8

from __future__ import division
from config.db import store_lyf,lyf
import numpy as np
import pandas as pd
import datetime
from collections import OrderedDict
import time
import pymongo

store_block=lyf['store_area']
level_store=lyf['user_level']


storeId = [elem['store_id'] for elem in store_block.find()]
storeId = list(set(storeId))


time_step = datetime.timedelta(1)

def userLevel(index):
    loc_list=list()
    for elem in index:
        loc_list.append(elem)
    #timeList=list(set([elem['time'].date() for elem in loc_list]))
    #timeList=sorted(timeList)
    #time_range = (timeList[-1]-timeList[0]).days
    
    time_range = 60
    
    user_time=dict()
    for elem in loc_list:
        if elem['user_id'] in user_time:
            user_time[elem['user_id']].append(elem['time'])
        else:
            user_time[elem['user_id']]=list()
            user_time[elem['user_id']].append(elem['time'])
        user_time[elem['user_id']] = sorted(user_time[elem['user_id']])
    
    user_level=dict()
    for k,v in user_time.items():
        count=1
        pivot=v[0]
        for elem in v:
            if elem-pivot>=time_step:
                pivot=elem
                count+=1
            else:
                pass
        try:
            user_level[k]=count/time_range
        except:
            pass
    
    return user_level



storeUserLevel=dict()
for elem in storeId:
    cursor = store_block.find({'store_id':elem})
    storeUserLevel[elem] = userLevel(cursor)

for k,v in storeUserLevel.items():
    a=dict()
    a['store_id']=k
    a['level']=v
    level_store.insert(a)


level_store.ensureIndex(('store_id',pymongo.ASCENDING))

