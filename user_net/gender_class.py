# coding=utf-8
__author__ = 'Carry lee'
from collections import Counter
import datetime
import urllib2
import json

from config.db import ICCv1, sh, utc, mapreduce


# 获取用户性别数据


class Gender(object):
    def __init__(self, collection_name, begin_name, end_name):
        self.collection_name = collection_name
        self.begin = begin_name
        self.end = end_name
        self.detail = ICCv1[self.collection_name]
        self.begin_utc = self.begin.astimezone(utc)
        self.end_utc = self.end.astimezone(utc)
        self.activity_info_db = mapreduce['gender_info_db']

    def get_gender(self):
        gender_info = dict()
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
        gender_info['begin'] = self.begin_utc
        gender_info['end'] = self.end_utc
        gender_info['male'] = male
        gender_info['female'] = female
        gender_info['__CREATE_TIME__'] = datetime.datetime.now(utc)
        gender_info['__REMOVED__'] = False
        gender_info['__MODIFY_TIME__'] = datetime.datetime.now(utc)
        self.activity_info_db.insert(gender_info)

        return 'work finished'
