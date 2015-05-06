#coding=utf-8

import sys
import os
from time import mktime
import pymongo
from bson.objectid import ObjectId
from config.db import bda,ICCv1,umav3

source_db_info = bda['source_db_info']
to_collection = bda['weixin']
query=dict()
query['$or'] = [ {'MsgType':'location'}, { 'Event': 'LOCATION'} ]
zero_id = ObjectId('000000000000000000000000')

for db_info in source_db_info.find({'__REMOVED__':False}):
    
    if db_info['database'] == 'ICCv1':
        db_name = ICCv1
        query['__REMOVED__']=False
    elif db_info['database'] == "umav3":
        db_name = umav3
    collection_name = db_info['collection']
    key_id = db_info['ToUserName']
    if db_info['last_id'] == '':
        last_id = zero_id
    else:
        last_id = ObjectId(db_info['last_id'])
    query['ToUserName']=key_id
    query['_id']={'$gt':last_id}
    from_collection = db_name[collection_name]
    flag = db_info['flag']
    if flag == True:
        continue
    else:
        source_db_info.update({'_id': db_info['_id']}, {"$set": {"flag": True}})
    count=0
    print db_info
    print query
    print from_collection.find().count()
    try:
        for elem in from_collection.find(query).sort('_id',pymongo.ASCENDING).add_option(16):
            a=dict()
            if 'Event' in elem and elem['Event'] == 'LOCATION':
                a['lbs'] = [float(elem['Longitude']),float(elem['Latitude'])]
            elif 'MsgType' in elem and elem['MsgType'] == 'location':
                a['lbs'] = [float(elem['Location_Y']),float(elem['Location_X'])]
            a['openid'] = elem['FromUserName']
            a['time'] = mktime(elem['__CREATE_TIME__'].timetuple())
            try:
                to_collection.insert(a)
            except Exception as e:
                print e
            last_id_new = elem['_id']
            count+=1
            
        print count
        source_db_info.update({'_id': db_info['_id']}, {"$set": {"last_id": str(last_id_new)}})
        source_db_info.update({'_id': db_info['_id']}, {"$set": {"flag": False}})
    except Exception as e:
        print e
    try:
        source_db_info.update({'_id': db_info['_id']}, {"$set": {"last_id": str(last_id_new)}})
    except Exception as e:
        print e
        source_db_info.update({'_id': db_info['_id']}, {"$set": {"flag": False}})        
        

to_collection.ensure_index([('lbs',pymongo.GEOSPHERE)])
to_collection.ensure_index('openid',1)
to_collection.ensure_index('time',1)

