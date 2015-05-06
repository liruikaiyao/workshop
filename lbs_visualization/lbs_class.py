# coding=utf-8
from __future__ import division
import heatmap
import pymongo
from pymongo import MongoClient
import datetime
import time
import gridfs
import tempfile
from config.db import lbs,db


fs = gridfs.GridFS(db)
hm = heatmap.Heatmap()
result = tempfile.gettempdir()

# 传入时间为时间戳格式
class user_lbs:
    def __init__(self,a_store,a_dist,a_center,a_time_start,a_time_end):
        self.store = a_store           #str
        self.dist = a_dist              #float
        self.center = a_center          #[float,float]
        self.time_start = datetime.datetime.fromtimestamp(a_time_start)
        self.time_end = datetime.datetime.fromtimestamp(a_time_end)
        
        radius = 6371


        cursor = lbs.aggregate([{'$geoNear':{'near':self.center,
                                     'distanceField':'dist',
                                     'num':100000,
                                     'maxDistance':self.dist/radius,
                                     'query':{'to':self.store,'time':{'$gte':self.time_start,'$lte':self.time_end}},
                                     'spherical':'true',
                                     'distanceMultiplier': 6371 }},
                                    {'$sort':{'time':-1}}])    #6371 Km
        within_lbs = cursor['result']
        print len(within_lbs)
        user = {}
        f =[]
        for elem in within_lbs:
            if user.has_key(elem['openid']):
                if len(user[elem['openid']])==3:
                    pass
                else:
                    user[elem['openid']].append(tuple(elem['lbs']))
            else:
                user[elem['openid']]=[tuple(elem['lbs'])]
        for item in user.keys():
            if len(user[item])==1:
                for i in range(0,3):
                    f.extend(user[item])
            elif len(user[item])==2:
                f.extend(user[item])
                f.append(user[item][0])
            else:
                f.extend(user[item])
            

        hm.heatmap(f,10,128,size=(4096, 4096))
        hm.saveKML(result+self.store+'.kml')


        #存入MongoDB
        f = open(result+self.store+'.kml')
        a = f.read()
        f.close()
        file_kml = fs.put(a,filename = self.store+'.kml',center = self.center,dist = self.dist,
                  time_start = self.time_start,time_end = self.time_end)
        g = open(result+self.store+'.png','rb')
        b = g.read()
        g.close()
        file_png = fs.put(b,filename = self.store+'.png',center = self.center,dist = self.dist,
                  time_start = self.time_start,time_end = self.time_end)
        
if __name__ == '__main__':
    klx = user_lbs('gh_33cc91076a66',20,[121.435101153,31.1952376167],1398873600,1405995856)