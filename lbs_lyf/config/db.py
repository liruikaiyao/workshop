#coding=utf-8
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
bda = client['bda']
ICCv1 = client['ICCv1']
umav3 = client['umav3']
lyf = client['lyf']