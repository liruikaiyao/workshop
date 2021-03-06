# coding=utf-8

from __future__ import division
from config.db import bda
# import numpy as np
# import pandas as pd
# import datetime
from collections import OrderedDict
import time
import pymongo
from bson.objectid import ObjectId
import sys
# import os

zero_id = ObjectId('000000000000000000000000')

query = dict()
# import sys
# sys.path.append('F:\workshop')
# from lbs_visualization.weibo_class import UserLbs
store_area = bda['store_area']
weixin_lyf = bda['weixin']
store_lyf = bda['store']
transfer_db = bda['transfer_db']

flag_list = [elem for elem in transfer_db.find()][0]
flag_id = flag_list['flag_id']
key_id = flag_list['_id']
if flag_id == '':
    flag_id = zero_id
else:
    pass
query['_id'] = {'$gt': flag_id}
if flag_list['flag']:
    sys.exit()
else:
    transfer_db.update({'_id': key_id}, {"$set": {"flag": True}})

begin = time.time()
# 删除lbs为空的数据
# count = 0
# for elem in weixin_lyf.find():
# if elem['precision'] == '0.000000':
# count += 1
# weixin_lyf.remove({'_id': elem['_id']})
# print(count)

# count=0
# for elem in weixin_lyf.find():
# if elem['lbs'][0]<-180 or elem['lbs'][0] >180 or elem['lbs'][1]<-90 or elem['lbs'][1]>90:
# count+=1
# weixin_lyf.remove({'_id':elem['_id']})
# print(count)

radius = 6371

# time_start = datetime.datetime(2014,9,8,0,0)
# time_end = datetime.datetime(2014,12,8,0,0)


# 处理模块
# cursor = weixin_lyf.aggregate([{'$geoNear':{'near':[121.435101153,31.1952376167],
# 'distanceField':'dist',
# 'num':100000,
# 'maxDistance':1000/radius,
# 'query':{'to':'gh_60217269884e'},    #,'time':{'$gte':time_start,'$lte':time_end}
# 'spherical':'true',
# 'distanceMultiplier': 6371 }},
# {'$sort': {'time': 1}}])    # 6371 Km

# within_lbs = cursor['result']
within_lbs = list()

for elem in weixin_lyf.find(query).sort('time', 1).add_option(16):
    within_lbs.append(elem)
    flag_id_new = elem['_id']
if not within_lbs:
    transfer_db.update({'_id': key_id}, {"$set": {"flag": False}})
    sys.exit()
else:
    pass
transfer_db.update({'_id': key_id}, {"$set": {"flag_id": flag_id_new}})
print(time.time() - begin)

user = OrderedDict()
# lbs_list=[]

time_step = 3600  # 选定时间间隔

for elem in within_lbs:
    if elem['openid'] in user:
        user[elem['openid']][elem['time']] = elem['lbs']
    else:
        user[elem['openid']] = OrderedDict()
        user[elem['openid']][elem['time']] = elem['lbs']

print(time.time() - begin)

# 用户字典
user_dict = OrderedDict()
# 时间因子的数据清洗
for k, v in user.items():
    user_dict[k] = OrderedDict()
    user_dict[k][v.keys()[0]] = v.values()[0]
    pivot = v.keys()[0]
    for i, j in v.items():
        if i - pivot >= time_step:
            user_dict[k][i] = j
            pivot = i
        else:
            pass

print(time.time() - begin)

# 以点为center实现KNN算法，K=1


def point2store(point):
    cursor = store_lyf.aggregate([{'$geoNear': {'near': point,
                                                'distanceField': 'dist',
                                                'num': 2,
                                                'maxDistance': 5 / radius,
                                                'spherical': 'true',
                                                'distanceMultiplier': 6371}},
                                  {'$sort': {'dist': 1}}])

    unique_store = cursor['result'][1]
    return unique_store

# store_area=dict()

for k, v in user_dict.items():
    for i, j in v.items():
        try:
            store = point2store(j)
            a = dict()
            a['store_id'] = store['store_id']
            a['user_id'] = k
            a['time'] = i
            a['lbs'] = j
            a['dist'] = store['dist']
            store_area.insert(a)
        except Exception as e:
            print e

store_area.ensure_index([('lbs', pymongo.GEOSPHERE)])
store_area.ensure_index('user_id', 1)
store_area.ensure_index('time', 1)
store_area.ensure_index('dist', 1)
store_area.ensure_index('store_id', 1)

transfer_db.update({'_id': key_id}, {"$set": {"flag": False}})
# if store in store_area:
# if k in store_area[store]:
# store_area[store][k][i]=j
# else:
# store_area[store][k]=dict()
# store_area[store][k][i]=j
# else:
# store_area[store]=dict()
# store_area[store][k]=dict()
# store_area[store][k][i]=j

# print time.time()-begin

# 将数据存储到数据库
# for k,v in store_area.items():
# for i,j in v.items():
# for m,n in j.items():
# a=dict()
# a['store_id']=k
# a['user_id']=i
# a['time']=m
# a['lbs']=n
# store_block.insert(a)


# for elem in weixin_lyf.find():
# if user_dict.has_key(elem['openid']):
# user_dict[elem['openid']].append(elem['lbs'])
# else:
# user_dict[elem['openid']]=list()

# 店铺字典
# store_dict=OrderedDict()
# for elem in store_lyf.find():
# store_dict[elem['store_id']]=elem['loc']

# print(time.time()-begin)


# dist_dict=dict()

# 计算店铺与用户的距离矩阵
# dist_dict结构dist_dict[用户id][店铺id]=平均距离

# for k,v in user_dict.items():
# dist_dict[k]=dict()
# for i,j in store_dict.items():
# dist=[]
# for elem in v:
# dist.append(np.linalg.norm(np.array(elem)-np.array(j)))
# dist_dict[k][i]=np.average(dist)


# 取最近的一家店铺id
# dist_min结构dist_min[用户id][店铺id]=最小距离
# 用户id对应到唯一的店铺id

# dist_min = dict()
# for k,v in dist_dict.items():
# a,b=sorted(v.iteritems(), key=lambda d:d[1], reverse = False)[0]
# if dist_min.has_key(a):
# dist_min[a][k]=b
# else:
# dist_min[a]=dict()
# dist_min[a][k]=b


# 计算店铺覆盖的有效范围
# store_area格式store_area[店铺id]=距离的中位数
# store_area=dict()
# for k,v in dist_min.items():
# a=pd.Series(v.values())
# store_area[k]=a.median()


# dist_df = pd.DataFrame(dist_dict)

# print(time.time()-begin)
# 将距离矩阵存储到MongoDB
# dist_df=dist_df.T
# b=len(dist_df.index)
# for i in xrange(b):
# a=dict()
# a[dist_df.index[i]]=dict(dist_df.ix[i])
# dist_lyf.insert(a)


# 画图

# store_list = store_area.keys()

# kml = simplekml.Kml()
# for elem in store_list:
# check = store_lyf.find_one({'store_id':elem})
# n = check[u'store_name']
# loc = check[u'loc']
# pnt = kml.newpoint(
# name=n,coords=[tuple(loc)])
# pnt.style.iconstyle.icon.href='E:\\Udisk\\icatholic\\green_dot.png'

# kml.save('key_store.kml')
