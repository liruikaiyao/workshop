#coding=utf-8
import numpy as np
import pandas as pd
#from config.db_server import sch_server
#from config.db import sch,bda,ICCv1
#import time
import datetime
import pytz
#from collections import Counter
#import matplotlib.pyplot as plt
import requests
import urllib2,urllib
#from bs4 import BeautifulSoup


#def post(url, data): 
    #req = urllib2.Request(url) 
    #data = urllib.urlencode(data) 
    ##enable cookie 
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
    #response = opener.open(req, data) 
    #return response.read() 
   
#def main(): 
    #url='http://urmdemo.umaman.com/tag/index/mark'
    #one={'identifyId': 'laste', 'tags[]': ['会员', '单品']}
    #print post(url, one) 
   
#if __name__ == '__main__': 
    #main() 


#points = ICCv1['points']
#order = ICCv1['order']
#cart = ICCv1['cart']
#sch_info = bda['schwarzkopf_tag']
#sch_act = bda['schwarzkopf_activity']

##各活动参与人数
#a=[elem['event'] for elem in sch_server.find()]
#c=Counter(a)

##产品详情页
#count=0
#user=[]
#activity=[]
#for elem in sch_server.find():
    #if u'gid=' in elem['request'] or u'gid=' in elem['referer']:
        #count+=1
        #user.append(elem['fromusername'])
        #activity.append(elem['event'])

#user_count=len(set(user))
#activity_count=Counter(activity)

##加购物车
#a=[elem['openid'] for elem in cart.find()]
#a=list(set(a))


##生成订单人数
#a=[elem['OpenId'] for elem in order.find()]
#a=list(set(a))
#order.count()

##付款人数
#a=[elem['OpenId'] for elem in order.find({'trade_state':0})]
#len(set(a))

##重复购买人数
#c=Counter(a)


##首页访问来源
#a=[elem['timestamp'] for elem in sch_server.find({'event':u'/weixinshop'})]
#b=[(datetime.datetime.fromtimestamp(elem)).date() for elem in a]
#c=Counter(b)
#d= sorted(c.iteritems(), key=lambda c:c[0], reverse = False)
#x=[elem[0] for elem in d]
#y=[elem[1] for elem in d]
#plt.plot(x,y)
#plt.savefig('time_activity')

#x_dict=dict()
#for elem in x:
    #x_dict[elem]=list()

#for elem in sch_server.find({'event':u'/weixinshop'}):
    #x_dict[(datetime.datetime.fromtimestamp(elem['timestamp'])).date()].append(elem['fromusername'])

#x_dict_new={k:len(set(v)) for k,v in x_dict.items()}
#f=sorted(x_dict_new.iteritems(), key=lambda x_dict_new:x_dict_new[0], reverse = False)
#z=[elem[1] for elem in f]



#user_year=[]
#user_ecv2=[]
#user_shop=[]
#for elem in sch_server.find({'event':u'/weixinshop'}):
    #user_shop.append(elem['fromusername'])

    #for elem in sch_server.find({'event':u'/yeartab'}):
        #user_year.append(elem['fromusername'])

        #for elem in sch_server.find({'event':u'/ecv2'}):
            #user_ecv2.append(elem['fromusername'])

#len(set(user_shop))
#len(set(user_year)&set(user_shop))


url='http://urmdemo.umaman.com/tag/index/mark?__ENABLE_DEBUG__=1'
one={'identifyId': 'laste', 'tags[]': ['会员']}

two = urllib.urlencode(one,True)
#r=requests.post(url,data=two)
#print r.content
req = urllib2.Request(url, two)
response = urllib2.urlopen(req)
print req
the_page = response.read()
print the_page

#full_url = url + u'?' + two
#response = urllib2.urlopen(full_url)
#the_page = response.read()
#print the_page

#a=[]
#for elem in order.find({'trade_state':0}):
    #if 'coupons_name' in elem['coupons']:
        #a.append(elem['body']+':'+elem['coupons']['coupons_name'])
#c=Counter(a)
#for k,v in c.items():
    #print k,v


