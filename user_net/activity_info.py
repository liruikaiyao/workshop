#coding=utf-8
__author__ = 'Carry lee'

from config.db import ICCv1,mapreduce, sh, utc
from collections import OrderedDict, Counter, defaultdict
import time, datetime
import urllib2
import json

api_url = u'http://api.map.baidu.com/geocoder/v2/?ak='
parameter = u'&output=json&coordtype=wgs84ll&location='
ak = 'SIpMcORCSogM916QMOz5tx7S'

weixin = ICCv1['weixin']
detail = ICCv1['detail']

begin = datetime.datetime(year=2015, month=5, day=12, hour=0,minute=0,second=0, tzinfo=sh)
end = datetime.datetime(year=2015, month=5, day=19, hour=0,minute=0,second=0, tzinfo=sh)

begin_utc = begin.astimezone(utc)
end_utc = end.astimezone(utc)

gender={}
male = 0
female = 0
for elem in detail.find({'__REMOVED__': False,
                         '__CREATE_TIME__': {'$gt':begin_utc, '$lt':end_utc}}):
    if 'sex' in elem:
        if elem['sex'] == 1:
            male+=1
        elif elem['sex'] == 2:
            female+=1
        else:
            pass

gender['male'] = male
gender['female'] = female

# 根据lbs数据获取城市信息的函数
def getcity(one):
    location = one['Latitude'] + ',' + one['Longitude']

    try:
        res = urllib2.urlopen(api_url + ak + parameter + location, timeout=0.5)
        address = json.loads(res.read())['result']
    except Exception as e:
        print e
    else:
        city = address['addressComponent']['city']
        return city

city_list=[]

for elem in weixin.find({'Event': 'LOCATION',
                         '__REMOVED__': False,
                         '__CREATE_TIME__': {'$gt':begin_utc, '$lt':end_utc}}).add_option(16):
    city_name = getcity(elem)
    city_list.append(city_name)

city_info = Counter(city_list)
