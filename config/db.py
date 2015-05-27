import pymongo
from pymongo import MongoClient
from pytz import timezone

tz = timezone("Asia/Shanghai")
client = MongoClient('localhost', 27017, tz_aware=True)
mapreduce = client['mapreduce']
ICCv1 = client['ICCv1']
test = client['test']