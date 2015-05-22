# coding=utf-8
__author__ = 'Carry lee'

import datetime
import time
from collections import defaultdict, Counter
from config.db import ICCv1, mapreduce
import urllib
import urllib2
import json

lyf = ICCv1['lyf']
user_info = mapreduce['user_info']
api_url = u'http://api.map.baidu.com/geocoder/v2/?ak='
parameter = u'&output=json&coordtype=wgs84ll&location='
ak = 'SIpMcORCSogM916QMOz5tx7S'


# 根据lbs数据获取城市信息的函数
def getcity(one):
    location = one['Latitude'] + ',' + one['Longitude']
    result = urllib2.urlopen(api_url + ak + parameter + location)
    try:
        address = json.loads(result.read())['result']
        city = address['addressComponent']['city']
        two = dict()
        two['FromUserName'] = one['FromUserName']
        two['city'] = city
        user_info.insert_one(two)
    except Exception as e:
        print e


for elem in lyf.find({'Event': 'LOCATION'}):
    getcity(elem)
