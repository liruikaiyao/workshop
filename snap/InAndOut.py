# coding=utf-8
from __future__ import division
from config.db import lyf_net
from pandas import DataFrame

name=[]
for elem in lyf_net.find():
    name.append(elem['got_FromUserName'])
    name.append(elem['owner_FromUserName'])
name=list(set(name))
lyf_net_dict=DataFrame(0,index=['in','out'],columns=name)

for item in lyf_net.find():
    lyf_net_dict[item['owner_FromUserName']]['out']+=1
    lyf_net_dict[item['got_FromUserName']]['in']+=1

#关于排序
lyf_net_dict.ix['in'].order(ascending=False)
lyf_net_dict.ix['out'].order(ascending=False)