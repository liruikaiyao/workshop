# coding=utf-8
__author__ = 'Carry lee'
from collections import Counter
import datetime
import urllib2
import json

from config.db import ICCv1, sh, utc


# 获取用户性别数据


class Gender:
    def __init__(self, collection_name, begin, end):
        self.collection_name = collection_name
        self.begin = begin
        self.end = end
        self.detail = ICCv1[self.collection_name]
        self.begin_utc = begin.astimezone(utc)
        self.end_utc = end.astimezone(utc)

    def get_gender(self):
        gender_info = {}
        male = 0
        female = 0
        for elem in self.detail.find({'__REMOVED__': False,
                                      '__CREATE_TIME__': {'$gt': self.begin_utc,
                                                          '$lt': self.end_utc}}):
            if 'sex' in elem:
                if elem['sex'] == 1:
                    male += 1
                elif elem['sex'] == 2:
                    female += 1
                else:
                    pass

        gender_info['male'] = male
        gender_info['female'] = female

        return gender_info
