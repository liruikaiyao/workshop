import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
hyd_events = client['schwarzkopf']['weixin']
hyd_users = client['schwarzkopf']['detail']
after_users = client['hyd']['after_users']