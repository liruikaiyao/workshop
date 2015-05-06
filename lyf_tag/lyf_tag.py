#coding=utf-8
import urllib2,urllib
import json
import datetime,time
import os, sys
from collections import defaultdict, Counter
from config.db import bda,ICCv1,test



lyf = ICCv1['lyf']
lyf_clean = ICCv1['lyf_clean']
member = ICCv1['member']
order = ICCv1['order']
log = test['log']
failed_log = test['failed_log']

lyf.ensure_index('__CREATE_TIME__',-1)
lyf.ensure_index('FromUserName',1)
lyf.ensure_index("__REMOVED__", 1)
lyf_clean.ensure_index('FromUserName', 1)
lyf_clean.ensure_index('__CREATE_TIME__',-1)


#activity_dict={'yeartab':'羊年开运签',
                #'dream':'奢美逐梦',
                #'ec':'EC深透门店申领',
                #'ecv2':'EC深透修护系列新品首发'}

url='http://laiyifendemo.umaman.com/tag/index/mark'
#?__ENABLE_DEBUG__=1

user_dict=defaultdict(list)

time_start = time.time()

#会员

for elem in member.find():
    user_dict[elem['FromUserName']].append('普通会员')

print time.time()-time_start

#购买用户

for elem in order.find({'trade_state':0}):
    user_dict[elem['OpenId']].append('购买用户')

print time.time()-time_start

#重复购买

for elem in order.find({'trade_state':0}):
    count=order.find({'OpenId':elem['OpenId'],
                      'trade_state':0}).count()
    if count>1:
        user_dict[elem['OpenId']].append('重复购买')

print time.time()-time_start

#新用户

cursor=lyf.find({"__REMOVED__" : False}).sort('__CREATE_TIME__',-1)
time_max=cursor.next()['__CREATE_TIME__']
time_min=time_max-datetime.timedelta(5)
user_list=[elem['FromUserName'] for elem in lyf.find({'Event':'subscribe',
                                                      "__REMOVED__" : False,
                                                      '__CREATE_TIME__':{'$gt':time_min}})]
user_list = list(set(user_list))
for elem in user_list:
    user_dict[elem].append('新用户')

print time.time()-time_start

#沉睡用户

#all_user=[elem['FromUserName'] for elem in lyf_clean.find()]
#time_min=time_max-datetime.timedelta(60)
#late_user=[elem['FromUserName'] for elem in lyf_clean.find({'__CREATE_TIME__':{'$gt':time_min}})]
#old_user = set(all_user)-set(late_user)
#for elem in old_user:
    #user_dict[elem].append('睡眠用户')
    
#print time.time()-time_start


#user_time = dict()
#time_min=time_max-datetime.timedelta(60)
#for elem in lyf_clean.find().sort('__CREATE_TIME__',1):
    #user_time[elem['FromUserName']] = elem['__CREATE_TIME__']
#for k, v in user_time.items():
    #if v < time_min:
        #user_dict[k].append('睡眠用户')
        
#print time.time()-time_start

#活跃用户

begin = time_max-datetime.timedelta(30)
user_list=[elem['FromUserName'] for elem in lyf_clean.find({'__CREATE_TIME__':{'$gt':begin}})]
user_count = Counter(user_list)
user_count= sorted(user_count.iteritems(), key=lambda d:d[1], reverse = True)
for elem in user_count:
    if elem[1]> 0:
        user_dict[elem[0]].append('活跃用户')

print time.time()-time_start

#高积分用户

#for elem in points.find().sort('score_total',-1).limit(25):
    #user_dict[elem['user_id']].append('高积分用户')

#print time.time()-time_start

#商品名称

#for elem in order.find({"__REMOVED__" : False,'trade_state':0}):
    #good=elem['body'].encode('utf-8').split(',')
    #user_dict[elem['OpenId']].extend(good)

#print time.time()-time_start

#参与活动

#for elem in sch_server.find({'event':{'$in':activity_dict.keys()}}):
    #event = elem['event']
    #user_dict[elem['fromusername']].append(activity_dict[event])

#print time.time()-time_start


#test
print len(user_dict)
print user_dict.items()[0]
user_dict = {k: list(set(v)) for k, v in user_dict.items()}
tag=reduce(lambda x,y:x+y,user_dict.values())
tag_count=Counter(tag)
for k,v in tag_count.items():
    print k,v

#添加标签

#for k,v in user_dict.items():
    #two = urllib.urlencode({'identifyId': k, 'tags[]': list(set(v))},True)
    #try:
        #req = urllib2.Request(url, two)
        #response = urllib2.urlopen(req)
        #result = response.read()
        #result = json.loads(result)
        #result['FromUserName'] = k
        #log.insert(result)
    #except Exception as e:
        #print k
        #print e
        #print type(e)
        #a={'FromUserName':k, 'error':str(e)}
        #failed_log.insert(a)
        #continue

print time.time()-time_start

#关机操作
#o="c:\\windows\\system32\\shutdown -s"
#os.system(o)