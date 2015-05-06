import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
lbs = client['weixin_lbs']['weixin_lbs']
db = client['file_store']
token = client['sina']['soa.sina.oauth']
weibo_list = client['sina']['weibo']
js = client['test']['json']
user = client['sina']['uid']
tweet_test = client['sina']['tweet']
weibo_lbs = client['sina']['sina_lbs']
lyf_net = client['network']['lyf_network']