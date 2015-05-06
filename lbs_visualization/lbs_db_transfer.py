import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
weibo_list = client['sina']['weibo']
lbs = client['sina']['sina_lbs']

for elem in weibo_list.find():
    lbs.insert({'time_stamp':elem['time_stamp'],'loc':elem['loc'],'uid':elem['user']['id']})