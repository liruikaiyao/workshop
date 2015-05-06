import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
hyd_events = client['hyd']['event_info']
hyd_users = client['hyd']['user_info']
after_users = client['hyd']['after_users']