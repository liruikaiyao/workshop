from pymongo import MongoClient
from pytz import timezone

sh = timezone("Asia/Shanghai")
utc = timezone('UTC')
client = MongoClient('localhost', 27017, tz_aware=True)
ICCv1 = client['ICCv1']
sch = client['schwarzkopf']
test = client['test']
mapreduce = client['mapreduce']