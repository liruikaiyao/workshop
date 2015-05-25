# coding=utf-8
__author__ = 'Carry lee'

import datetime
import time
from collections import defaultdict, Counter
from config.db import ICCv1, mapreduce
import urllib
import urllib2
import json
import threading
import multiprocessing

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

begin = time.time()
if __name__ == '__main__':
    multiprocessing.freeze_support()
    p = multiprocessing.Pool(processes=3)
    result = []
    for elem in lyf.find({'Event': 'LOCATION'}).limit(1000):
        result.append(p.apply_async(getcity, (elem, )))
    p.close()
    p.join()
    # for res in result:
    #     print res.get()
    print "all task finished"

print time.time() - begin

