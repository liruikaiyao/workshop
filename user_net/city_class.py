# coding=utf-8
__author__ = 'Carry lee'

from collections import Counter
import datetime
import urllib2
import json

from config.db import ICCv1, sh, utc

# 百度地图API参数


api_url = u'http://api.map.baidu.com/geocoder/v2/?ak='
parameter = u'&output=json&coordtype=wgs84ll&location='
ak = 'SIpMcORCSogM916QMOz5tx7S'


# 获取用户城市信息


class CityTag:
    def __init__(self, collection_name, begin, end):
        self.collection_name = collection_name
        self.begin = begin
        self.end = end
        self.weixin = ICCv1[self.collection_name]
        self.begin_utc = self.begin.astimezone(utc)
        self.end_utc = self.end.astimezone(utc)

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

        city_list = []
        for elem in self.weixin.find({'Event': 'LOCATION',
                                      '__REMOVED__': False,
                                      '__CREATE_TIME__': {'$gt': self.begin_utc,
                                                          '$lt': self.end_utc}}).add_option(16):
            city_name = self.getcity(elem)
            city_list.append(city_name)

        city_info = Counter(city_list)
        return city_info
