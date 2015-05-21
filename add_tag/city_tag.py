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
api_url = u'http://api.map.baidu.com/geocoder/v2/?ak='
parameter = u'&output=json&coordtype=wgs84ll&location='
ak = 'SIpMcORCSogM916QMOz5tx7S'

for elem in lyf.find({'Event': 'LOCATION'}):
    location = elem['Latitude'] + ',' + elem['Longitude']
    result = urllib2.urlopen(api_url + ak + parameter + location)
    try:
        address = json.loads(result.read())['result']
        city = address['addressComponent']['city']
    except Exception as e:
        print e
        continue
