# coding=utf-8
import urllib2
import urllib
import json
import datetime
import time
from collections import defaultdict, Counter

# from config.db_server import sch_server
from config.db import ICCv1, test, sch, sh, utc

# points = ICCv1['points']
order = sch['order']
# member = ICCv1['member']
# first_shop = ICCv1['first_shop']
kjw = sch['kanjiawu']
hongbao = sch['hongbao']
log = test['log']
failed_log = test['failed_log']

activity_dict = {'yeartab': '羊年开运签',
                 'dream': '奢美逐梦',
                 'ec': 'EC深透门店申领',
                 'ecv2': 'EC深透修护系列新品首发'}

url = 'http://weixin.schwarzkopfclub.com.cn/tag/index/mark'
# ?__ENABLE_DEBUG__=1

user_dict = defaultdict(list)

time_start = time.time()

# 会员

# for elem in member.find({"__REMOVED__": False}):
#     user_dict[elem['FromUserName']].append('会员')
#
# print time.time() - time_start

# 红包领取用户

# for elem in hongbao.find({"__REMOVED__": False}):
#     user_dict[elem['re_openid']].append('领取红包')
#
# print time.time() - time_start

# 核心用户

for elem in kjw.find({"__REMOVED__": False, 'total_bargain_num': {'$gte': 10}}):
    user_dict[elem['code']].append('核心用户')

# # 购买用户
#
# for elem in order.find({"__REMOVED__": False, 'trade_state': 0}):
#     user_dict[elem['OpenId']].append('购买用户')
#
# print time.time() - time_start
#
# # 重复购买
#
# for elem in order.find({"__REMOVED__": False, 'trade_state': 0}):
#     count = order.find({'OpenId': elem['OpenId'], "__REMOVED__": False,
#                         'trade_state': 0}).count()
#     if count > 1:
#         user_dict[elem['OpenId']].append('重复购买')
#
# print time.time() - time_start
#
# # 新用户
#
# cursor = sch.find({"__REMOVED__": False}).sort('__CREATE_TIME__', -1)
# time_max = cursor.next()['__CREATE_TIME__']
# time_min = time_max - datetime.timedelta(5)
# user_list = [elem['FromUserName'] for elem in sch.find({'Event': 'subscribe',
#                                                         "__REMOVED__": False,
#                                                         '__CREATE_TIME__': {'$gt': time_min}})]
# user_list = list(set(user_list))
# for elem in user_list:
#     user_dict[elem].append('新用户')
#
# print time.time() - time_start
#
# # 沉睡用户
#
# all_user = [elem['FromUserName'] for elem in sch.find({"__REMOVED__": False, 'FromUserName': {'$exists': True}})]
# time_min = time_max - datetime.timedelta(60)
# late_user = [elem['FromUserName'] for elem in sch.find({"__REMOVED__": False,
#                                                         '__CREATE_TIME__': {'$gt': time_min},
#                                                         'FromUserName': {'$exists': True}})]
# old_user = set(all_user) - set(late_user)
# for elem in old_user:
#     user_dict[elem].append('睡眠用户')
#
# print time.time() - time_start
#
# # 活跃用户
#
# begin = time_max - datetime.timedelta(30)
# user_list = [elem['FromUserName'] for elem in sch.find({"__REMOVED__": False,
#                                                         '__CREATE_TIME__': {'$gt': begin},
#                                                         'FromUserName': {'$exists': True}})]
# user_count = Counter(user_list)
# user_count = sorted(user_count.iteritems(), key=lambda d: d[1], reverse=True)
# for elem in user_count:
#     if elem[1] > 2:
#         user_dict[elem[0]].append('活跃用户')
#
# print time.time() - time_start
#
# # 高积分用户
#
# for elem in points.find().sort('score_total', -1).limit(25):
#     user_dict[elem['user_id']].append('高积分用户')
#
# print time.time() - time_start

# 商品名称

# for elem in order.find({"__REMOVED__": False, 'trade_state': 0}):
#     good = elem['body'].encode('utf-8').split(',')
#     user_dict[elem['OpenId']].extend(good)
#
# print time.time() - time_start

# 参与活动

# for elem in sch_server.find({'event': {'$in': activity_dict.keys()}}):
#     event = elem['event']
#     user_dict[elem['fromusername']].append(activity_dict[event])

# print time.time()-time_start


# test
print len(user_dict)
print user_dict.items()[0]
user_dict = {k: list(set(v)) for k, v in user_dict.items()}
tag = reduce(lambda x, y: x + y, user_dict.values())
tag_count = Counter(tag)
for k, v in tag_count.items():
    print k, v

# 添加标签

for k, v in user_dict.items():
    two = urllib.urlencode({'identifyId': k, 'tags[]': list(set(v))}, True)
    try:
        req = urllib2.Request(url, two)
        response = urllib2.urlopen(req)
        result = response.read()
        result = json.loads(result)
        result['FromUserName'] = k
        result['__CREATE_TIME__'] = datetime.datetime.now(tz=sh)
        log.insert(result)
    except Exception as e:
        print k
        print e
        print type(e)
        a = {'FromUserName': k, 'error': str(e)}
        a['__CREATE_TIME__'] = datetime.datetime.now(tz=sh)
        failed_log.insert(a)
        continue

print time.time() - time_start
