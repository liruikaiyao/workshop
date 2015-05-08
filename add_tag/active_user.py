# coding=utf-8
__author__ = 'Carry lee'

# import urllib
# import urllib2
# import json
import datetime
import time
from collections import defaultdict, Counter
from config.db import ICCv1, mapreduce

log = mapreduce['log']
failed_log = mapreduce['failed_log']
active_user_tag_config = mapreduce['active_user_tag_config']

for item in active_user_tag_config.find({'__REMOVED__': False}):
    collection_name = 'idatabase_collection_' + item['collection']
    target_collection = ICCv1[collection_name]
    print target_collection.count()
    url = 'http://' + item['host'] + '/tag/index/mark'
    day = item['day']
    activities = item['activities']
    target_collection.ensure_index('__CREATE_TIME__', -1)
    target_collection.ensure_index('FromUserName', 1)
    target_collection.ensure_index("__REMOVED__", 1)

    user_dict = defaultdict(list)
    time_start = time.time()
    cursor = target_collection.find({"__REMOVED__": False}).sort('__CREATE_TIME__', -1)
    time_max = cursor.next()['__CREATE_TIME__']
    begin = time_max - datetime.timedelta(day)
    user_list = [elem['FromUserName'] for elem in target_collection.find({"__REMOVED__": False,
                                                                          '__CREATE_TIME__': {'$gt': begin},
                                                                          'FromUserName': {'$exists': True}})]

    user_count = Counter(user_list)
    user_count = sorted(user_count.iteritems(), key=lambda d: d[1], reverse=True)
    for elem in user_count:
        if elem[1] > activities:
            user_dict[elem[0]].append('活跃用户')

    print time.time() - time_start

    # test
    print len(user_dict)
    print user_dict.items()[0]
    user_dict = {k: list(set(v)) for k, v in user_dict.items()}
    tag = []
    for elem in user_dict.values():
        tag.extend(elem)
    tag_count = Counter(tag)
    for k, v in tag_count.items():
        print k, v

    # 添加标签

    # for k, v in user_dict.items():
    # two = urllib.urlencode({'identifyId': k, 'tags[]': list(set(v))}, True)
    # try:
    #         req = urllib2.Request(url, two)
    #         response = urllib2.urlopen(req)
    #         result = response.read()
    #         result = json.loads(result)
    #         result['FromUserName'] = k
    #         log.insert(result)
    #     except Exception as e:
    #         print k
    #         print e
    #         print type(e)
    #         a = {'FromUserName': k, 'error': str(e)}
    #         failed_log.insert(a)
    #         continue

    print time.time() - time_start
