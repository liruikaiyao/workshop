# coding=utf-8
__author__ = 'Carry lee'

import datetime
import time
from collections import defaultdict, Counter
from config.db import ICCv1, mapreduce, tz
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

    try:
        res = urllib2.urlopen(api_url + ak + parameter + location, timeout=0.5)
        address = json.loads(res.read())['result']
    except Exception as e:
        print e
    else:
        city = address['addressComponent']['city']
        two = dict()
        two['FromUserName'] = one['FromUserName']
        two['city'] = city
        user_info.insert_one(two)

begin = time.time()
# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     p = multiprocessing.Pool(processes=2)
#     result = []
#     for elem in lyf.find({'Event': 'LOCATION'}).add_option(16):
#         result.append(p.apply_async(getcity, (elem, )))
#     p.close()
#     p.join()
#     # for res in result:
#     #     print res.get()
#     print "all task finished"
for elem in lyf.find({'Event': 'LOCATION'}).add_option(16):
    getcity(elem)

print time.time() - begin
