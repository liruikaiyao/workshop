import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
events = client['gaojiesi']['event_list']
users = client['gaojiesi']['user_list']
user_clear = client['gaojiesi']['user_clear']
user_info = client['gaojiesi']['user_info']
hyd_events = client['hyd']['event_info']
hyd_users = client['hyd']['user_info']