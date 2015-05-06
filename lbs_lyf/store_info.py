#coding=utf-8

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import numpy as np
from config.db import bda
import json


StoreArea = bda['store_area']

#cursor = StoreArea.find({'store_id':"106Z",
                         #'timestamp': {'$gte':1202351318,'$lte':1502351318},
                         #'dist':{'$gt':0,'$lt':4}})

#a=[elem for elem in cursor]

#pipeline = [
    #{"$match": {'store_id':"106Z"}},
    #{"$match": {'timestamp': {'$gt':1202351318,'$lt':1502351318}}},
    #{'$match':{'dist':{'$gt':0,'$lt':4}}},
    #{"$sort": SON([('timestamp',-1)])}]

#result=StoreArea.aggregate(pipeline)




 
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()
    
    def post(self):
        self.deal()
        
    def deal(self):
        storeID = self.get_argument('storeID',default='[]')
        print storeID
        print type(storeID)
        storeID = json.loads(storeID)
        print storeID
        print type(storeID)
        all_user = self.get_argument('all_user',default='[]')
        all_user = json.loads(all_user)
        time_begin = self.get_argument('time_begin',default=0)
        time_begin = float(time_begin)
        time_end = self.get_argument('time_end',default=2422318061)
        time_end = float(time_end)
        distance_min = self.get_argument('distance_min',default=0)
        distance_min = float(distance_min)
        distance_max = self.get_argument('distance_max',default=10)
        distance_max = float(distance_max)
        item_count = self.get_argument('item_count',default=10)
        print item_count
        print type(item_count)
        item_count = int(item_count)
        print item_count
        print type(item_count)
        skip_item = self.get_argument('skip_item',default=0)
        skip_item = int(skip_item)
        sort_key = self.get_argument('sort_key',default='time')
        
        #response={
        #'storeID':storeID,
        #'time_begin':time_begin,
        #'time_end':time_end,
        #'distance_min':distance_min,
        #'distance_max':distance_max}
        if storeID==[] and all_user!=[]:
            cursor = StoreArea.find({'user_id':{'$in':all_user},
                                     'time': {'$gte':time_begin,'$lte':time_end},
                                     'dist':{'$gte':distance_min,'$lte':distance_max}})
        elif all_user==[] and storeID!=[]:
            cursor = StoreArea.find({'store_id':{'$in':storeID},
                                     'time': {'$gte':time_begin,'$lte':time_end},
                                     'dist':{'$gte':distance_min,'$lte':distance_max}})
        elif all_user==[] and storeID==[]:
            cursor = StoreArea.find({'time': {'$gte':time_begin,'$lte':time_end},
                                     'dist':{'$gte':distance_min,'$lte':distance_max}})
        else:
            cursor = StoreArea.find({'store_id':{'$in':storeID},
                                     'user_id':{'$in':all_user},
                                     'time': {'$gte':time_begin,'$lte':time_end},
                                     'dist':{'$gte':distance_min,'$lte':distance_max}})
        
        a=[elem for elem in cursor]
        user_list=[elem['user_id'] for elem in a]
        user_list = set(user_list)
        b={}
        for elem in user_list:
            b[elem]=list()
        for elem in a:
            b[elem['user_id']].append(elem)
        user_list=[]
        for k,v in b.items():
            one_user={}
            one_user['user_id']=k
            one_user['trace']=[{'time':elem['time'],'store_id':elem['store_id'],
                                'distance':elem['dist']} for elem in v]
            one_user['distance'] = np.mean([elem['dist'] for elem in v])
            one=max([item['time'] for item in v])
            one_user['last_time']=one
            one_user['store_id']=v[0]['store_id']
            user_list.append(one_user)
        
        if sort_key == u'time':
            user_list = sorted(user_list,key = lambda x:x['last_time'],reverse=True)
        elif sort_key == u'distance':
            user_list = sorted(user_list,key = lambda x:x['distance'])
        
        responce=dict()
        responce['total']=len(user_list)
        if responce['total'] < item_count:
            item_count = responce['total']
        if responce['total'] < skip_item:
            skip_item=0
        responce['data']=user_list[skip_item:skip_item+item_count]
        responce['item_count'] = item_count
        responce['skip_item'] = skip_item
        self.write(responce)
 
 
application = tornado.web.Application([
    (r"/", VersionHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
    
