from pymongo import MongoClient

data_ip = '127.0.0.1'
client = MongoClient(data_ip, 27017)
ICCv1 = client['ICCv1']
mapreduce = client['mapreduce']
github_token = '7b0414b1b1c87528ee3e16ac4b97fcc351f6062b'