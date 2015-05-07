__author__ = 'Carry lee'
# coding=utf-8
import datetime
from config.db import mapreduce

new_user_tag_config = mapreduce['new_user_tag_config']
new_user_tag_config.remove({})
example = dict()
example['host'] = 'laiyifendemo.umaman.com'
example['remark'] = '最近关注5天内'
example['day'] = 5
example['database'] = 'ICCv1'
example['collection'] = '55078670b1752fad378b4742'
example['__REMOVED__'] = False
example['__CREATE_TIME__'] = datetime.datetime.now()
example['__MODIFY_TIME__'] = datetime.datetime.now()

new_user_tag_config.insert(example)