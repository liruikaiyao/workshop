import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
bda = client['bda']
lyf = client['lyf']
umav3 = client['umav3']
network = client['network']