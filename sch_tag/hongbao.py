# coding=utf-8
__author__ = 'Carry lee'

import datetime
import time

from config.db import sh, utc, sch

end = datetime.datetime(year=2015, month=5, day=23, tzinfo=sh)
begin = datetime.datetime(year=2015, month=5, day=19, tzinfo=sh)
utc_begin = begin.astimezone(tz=utc)
utc_end = end.astimezone(tz=utc)
time_span = datetime.timedelta(days=1)

order = sch['order']
hbao = sch['hongbao']
weixin = sch['weixin']

date_people = dict()
for i in range(1, 8):
    date_people[str(begin + time_span * i)] = hbao.find(
        {'__CREATE_TIME__': {'$gte': utc_begin + time_span * i,
                             '$lte': utc_begin + time_span * (i + 1)}}).count()

hbao_user = [elem['re_openid'] for elem in hbao.find()]
hbao_user = list(set(hbao_user))

activate_user = []
start = time.time()
for item in hbao_user:
    try:
        last_time = max([elem['__CREATE_TIME__'] for elem in weixin.find(
            {'FromUserName': item,
             "__REMOVED__": False,
             '__CREATE_TIME__': {'$lte': utc_begin}})])
    except ValueError as e:
        print e
    except:
        print "Unexpected error!"
    else:
        if (utc_begin-last_time).days > 60:
            activate_user.append(item)
else:
    print time.time() - start
