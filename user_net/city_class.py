# coding=utf-8
__author__ = 'Carry lee'

from collections import Counter
import datetime
import urllib2
import json

from config.db import ICCv1, sh, utc, mapreduce

# 百度地图API参数


api_url = u'http://api.map.baidu.com/geocoder/v2/?ak='
parameter = u'&output=json&coordtype=wgs84ll&location='
ak = 'SIpMcORCSogM916QMOz5tx7S'


# 获取用户城市信息


class CityTag(object):
    def __init__(self, collection_name, begin_name, end_name):
        self.collection_name = collection_name
        self.begin = begin_name
        self.end = end_name
        self.weixin = ICCv1['weixin']
        self.begin_utc = self.begin.astimezone(utc)
        self.end_utc = self.end.astimezone(utc)
        self.activity_info_db = mapreduce['city_info_db']

    def getcity(self, one):
        location = one['Latitude'] + ',' + one['Longitude']
        try:
            res = urllib2.urlopen(api_url + ak + parameter + location, timeout=0.5)
            address = json.loads(res.read())['result']
        except Exception as e:
            print e
        else:
            city = address['addressComponent']['city']
            return city

    def get_city_info(self):
        one = dict()
        city_list = []
        for elem in self.weixin.find({'Event': 'LOCATION',
                                      '__REMOVED__': False,
                                      '__CREATE_TIME__': {'$gt': self.begin_utc,
                                                          '$lt': self.end_utc}}).add_option(16):
            city_name = self.getcity(elem)
            city_list.append(city_name)

        city_info = Counter(city_list)
        one['begin'] = self.begin_utc
        one['end'] = self.end_utc
        one['city_info'] = city_info
        one['__CREATE_TIME__'] = datetime.datetime.now(utc)
        one['__REMOVED__'] = False
        one['__MODIFY_TIME__'] = datetime.datetime.now(utc)
        self.activity_info_db.insert(one)
        return 'work finished'
