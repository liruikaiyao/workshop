# coding=utf-8
from pymongo import MongoClient

data_ip = '127.0.0.1'
client = MongoClient(data_ip, 27017)
ICCv1 = client['ICCv1']
mapreduce = client['mapreduce']