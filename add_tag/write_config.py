# coding=utf-8
__author__ = 'Carry lee'
import datetime
from config.db import mapreduce

active_user_tag_config = mapreduce['active_user_tag_config']
active_user_tag_config.remove({})
example = dict()
example['host'] = 'laiyifendemo.umaman.com'
example['remark'] = '最近30天内互动次数超过2次'
example['day'] = 30
example['database'] = 'ICCv1'
example['collection'] = '55078670b1752fad378b4742'
example['__REMOVED__'] = False
example['activities'] = 2
example['__CREATE_TIME__'] = datetime.datetime.now()
example['__MODIFY_TIME__'] = datetime.datetime.now()

active_user_tag_config.insert(example)