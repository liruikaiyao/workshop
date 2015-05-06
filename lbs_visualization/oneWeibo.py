# coding=utf-8
from __future__ import division
from time import mktime
from random import randint

from weibo import APIClient

from config.db import token,user,tweet_test


APP_KEY = '893013673'  # app key
APP_SECRET = 'd5e5ea7694fc8e63e6f348abb31104cb'  # app secret
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'  # callback url



# 获取uid
uid_list = []
user_list = user.find().limit(5)
for elem in user_list:
    uid = elem['uid']
    uid_list.append(uid)

# about access_token
access = []
cursor = token.find({'projectId': '52f98c664a961923478b4b37'}).sort('expireTime', -1).limit(150)
for elem in cursor:
    a = elem['access_token']
    b = elem['expireTime']
    b = b.timetuple()
    b = mktime(b)
    access.append(tuple([a, b]))

count = 0
for elem in uid_list:
    num = randint(1, 100)

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(access[num][0], access[num][1])
    try:
        status = client.place.user_timeline.get(uid=elem)
        a = status['statuses']
        for elem in a:
            tweet_test.insert(elem)
    except Exception, e:
        print e
        count += 1

print count



