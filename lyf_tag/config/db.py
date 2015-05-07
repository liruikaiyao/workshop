from pymongo import MongoClient

client = MongoClient('localhost', 27017)
ICCv1 = client['ICCv1']
umav3 = client['umav3']
bda = client['bda']
test = client['test']
mapreduce = client['mapreduce']