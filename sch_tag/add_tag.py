#coding=utf-8
import numpy as np
from config.db_server import sch_server
from config.db import sch,bda,ICCv1
import time
import datetime
from collections import Counter

time_bigin=time.time()
points = ICCv1['points']
order = ICCv1['order']
cart = ICCv1['cart']
member = ICCv1['member']
sch_info = bda['schwarzkopf_tag']
first_shop = ICCv1['first_shop']

#清洗event
#count=0
#for elem in sch_server.find():
    #if elem['event'] in remove_event:
        #sch_server.remove({'_id':elem['_id']})
        #count+=1


user_list=[elem['FromUserName'] for elem in sch.find({"__REMOVED__" : False})]
user_list_ser=[elem['fromusername'] for elem in sch_server.find()]
user_list_points=[elem['user_id'] for elem in points.find({"__REMOVED__" : False})]
user_list_member=[elem['FromUserName'] for elem in member.find({"__REMOVED__" : False})]
user_list_order=[elem['OpenId'] for elem in order.find({"__REMOVED__" : False})]
user_list_shop=[elem['FromUserName'] for elem in first_shop.find({"__REMOVED__" : False})]
user_list_cart=[elem['openid'] for elem in cart.find({"__REMOVED__" : False})]


unique_list=list(set(user_list)|set(user_list_ser)|set(user_list_points)|set(user_list_member))

time_max=max([elem['__CREATE_TIME__'] for elem in sch.find({"__REMOVED__" : False})])

time_min=min(np.array([elem['timestamp'] for elem in sch_server.find()]))

user_dict=dict()
for elem in unique_list:
    user_dict[elem]=dict()

print time.time()-time_bigin

#会员
for elem in member.find({"__REMOVED__": False}):
    user_dict[elem['FromUserName']].append('会员')

#最近五天内关注的新用户
for item in unique_list:
    try:
        sub_time=max(np.array([elem['__CREATE_TIME__'] for elem in sch.find({'FromUserName':item,'Event':'subscribe',"__REMOVED__" : False})]))
        if (time_max-sub_time).days<5:
            user_dict[item]['new']=True
        else:
            user_dict[item]['new']=False
    except:
        user_dict[item]['new']=False

print time.time()-time_bigin
#近三个月没活动的沉睡用户
for item in unique_list:
    try:
        last_time=max(np.array([elem['__CREATE_TIME__'] for elem in sch.find({'FromUserName':item,"__REMOVED__" : False})]))
        if (time_max-last_time).days>60:
            user_dict[item]['sleep']=True
        else:
            user_dict[item]['sleep']=False
    except:
        user_dict[item]['sleep']=False

print time.time()-time_bigin
#参加过的活动
for item in unique_list:
    event_list=[elem['event'] for elem in sch_server.find({'fromusername':item})]
    user_dict[item]['event']=list(set(event_list))
    user_dict[item]['activity_num']=len(set(event_list))

print time.time()-time_bigin
#会员积分
for item in unique_list:
    score_total = points.find_one({'user_id':item,"__REMOVED__" : False})
    if score_total==None:
        user_dict[item]['score']=0
    else:
        user_dict[item]['score']=score_total['score_total']

print time.time()-time_bigin
#购买行为
for item in unique_list:
    bought_num=order.find({'OpenId':item,"__REMOVED__" : False,'trade_state':0}).count()
    user_dict[item]['bought']=bought_num


print time.time()-time_bigin

#最近三十天交互天数
begin = time_max-datetime.timedelta(30)
event_dict=dict()
for elem in unique_list:
    event_dict[elem]=list()
for elem in sch.find({'__CREATE_TIME__':{'$gt':begin}}):
    event_dict[elem['FromUserName']].append(elem['__CREATE_TIME__'].date())

for k,v in event_dict.items():
    user_dict[k]['event_num']=len(set(v))

print time.time()-time_bigin

#insert to MongoDB
for k,v in user_dict.items():
    a=v
    a['user_id']=k
    sch_info.insert(a)

sch_info.ensure_index('user_id',1)

print time.time()-time_bigin


#清洗一种tag
#for elem in sch_info.find():
    #a=elem['event']
    #b=[]
    #for item in a:
        #if '/coupons/index' in item:
            #b.append(u'/coupons/index')
        #else:
            #b.append(item)
    #b=list(set(b))
    #sch_info.update({'_id': elem['_id']}, {"$set": {"event":b}})

#for elem in sch_info.find():
    #a=elem['event']
    #if u'/weixin/page/index/id/54a3c3b5499619f76b8b4607' in a:
        #a.remove(u'/weixin/page/index/id/54a3c3b5499619f76b8b4607')
        #a.append(u'/weixin/page/index/id/')
    #else:
        #pass
    #sch_info.update({'_id': elem['_id']}, {"$set": {"event":a}})

    #for elem in sch_info.find():
        #a=elem['event']
        #a=list(set(a))
        #sch_info.update({'_id': elem['_id']}, {"$set": {"event":a}})


#用户参加活动数
#event={elem[u'活动']:elem['activity'] for elem in sch_act.find()}
#user_count=dict()
#for elem in sch_info.find():
    #a=elem['event']
    #count=[]
    #for item in a:
        #for k,v in event.items():
            #if item in v:
                #count.append(k)
    #count=len(set(count))
    #user_count[elem['user_id']]=count


#各个活动参与人数
#activity_list=[]
#for elem in sch_info.find():
    #a=elem['event']
    #for item in a:
        #for k,v in event.items():
            #if item in v:
                #activity_list.append(k)
                
#activity_count=Counter(activity_list)


#weixinshop:7493人
#生成订单:1755

#right_event = [u'ecv2',
 #u'ultime',
 #u'weixinshop',
 #u'ec',
 #u'members',
 #u'yeartab',
 #u'dream',
 #u'coupons']

#remove_event = [u'member', u'weixin', u'mp', u'html', u'trial']