#coding=utf-8

from __future__ import division
from config.db import store_lyf, lyf
from customer_churn import surAnalysis
import numpy as np
import pandas as pd
import datetime
from collections import OrderedDict
import time
import pymongo

user_level = lyf['user_level']
store_area = lyf['store_area']

storeId = [elem['store_id'] for elem in user_level.find()]

for elem in storeId:
    dist=list()
    a=dict()
    cursor = store_area.find({'store_id':elem})
    for item in cursor:
        dist.append(item['dist'])
    dist = pd.Series(dist)
    user_level.update({'store_id':elem},{"$set":{'max_dist':dist.max()}})
    user_level.update({'store_id':elem},{"$set":{'min_dist':dist.min()}})
    user_level.update({'store_id':elem},{"$set":{'median_dist':dist.median()}})
    user_level.update({'store_id':elem},{"$set":{'mean_dist':dist.mean()}})
    a=store_lyf.find_one({'store_id':elem})['store_name']
    user_level.update({'store_id':elem},{"$set":{'store_name':a}})

user_level.ensureIndex(('store_name',pymongo.ASCENDING))

for elem in storeId:
    surAnalysis(elem)

