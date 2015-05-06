import pymongo
from pymongo import MongoClient

client_server = MongoClient('192.168.5.41', 37017)
test_server= client_server['test']
sch_server = test_server['schwarzkopf']