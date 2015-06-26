from pymongo import MongoClient
from pytz import timezone

sh = timezone("Asia/Shanghai")
utc = timezone("utc")
data_ip = '127.0.0.1'
client = MongoClient(data_ip, 27017, tz_aware=True)
ICCv1 = client['schwarzkopf']
mapreduce = client['mapreduce']