#coding=utf-8
__author__ = 'Carry lee'
import datetime
from config.db import client,sh,utc,mapreduce

gender_config = mapreduce['gender_config']

para = dict()
para['__CREATE_TIME__'] = datetime.datetime.now(utc)
para['__REMOVED__'] = False
para['__MODIFY_TIME__'] = datetime.datetime.now(utc)
para['begin'] = datetime.datetime(2015,6,5,tzinfo=sh).astimezone(utc)
para['end'] = datetime.datetime(2015,6,17,tzinfo=sh).astimezone(utc)
para['collection_name'] = 'detail'
para['project'] = '施华蔻'
para['is_running'] = False

gender_config.insert(para)

para = dict()
kanjia_config = mapreduce['kanjia_config']
para['__CREATE_TIME__'] = datetime.datetime.now(utc)
para['__REMOVED__'] = False
para['__MODIFY_TIME__'] = datetime.datetime.now(utc)
para['begin'] = datetime.datetime(2015,6,5,tzinfo=sh).astimezone(utc)
para['end'] = datetime.datetime(2015,6,17,tzinfo=sh).astimezone(utc)
para['collection_name_kanjia'] = 'kanjia'
para['collection_name_kanjiawu'] = 'kanjiawu'
para['collection_name_yaoqing'] = 'yaoqing'
para['collection_name'] = 'detail'
para['project'] = '施华蔻'
para['is_running'] = False

kanjia_config.insert(para)

city_tag_config = mapreduce['city_tag_config']
para = dict()
para['__CREATE_TIME__'] = datetime.datetime.now(utc)
para['__REMOVED__'] = False
para['__MODIFY_TIME__'] = datetime.datetime.now(utc)
para['begin'] = datetime.datetime(2015,6,5,tzinfo=sh).astimezone(utc)
para['end'] = datetime.datetime(2015,6,17,tzinfo=sh).astimezone(utc)
para['collection_name'] = 'detail'
para['project'] = '施华蔻'
para['is_running'] = False

city_tag_config.insert(para)
