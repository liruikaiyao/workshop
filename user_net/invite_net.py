#coding=utf-8
__author__ = 'Carry lee'

from config.db import ICCv1, mapreduce
from collections import defaultdict, Counter, OrderedDict
import networkx as nx

invite_collection_name = 'yaoqing'
invite = ICCv1[invite_collection_name]
detail_collection_name = 'detail'
detail = ICCv1[detail_collection_name]

owner=[]
got=[]
for elem in invite.find():
    owner.append(elem['owner_FromUserName'])
    got.append(elem['got_FromUserName'])

all_user = list(set(got+owner))

all_user_name = dict()

for elem in all_user:
    cursor = detail.find_one({'openid':elem})
    all_user_name[elem] = cursor['nickname']

H = nx.DiGraph()

for elem in invite.find():
    if elem['got_FromUserName'] == elem['owner_FromUserName']:
        pass
    else:
        H.add_edge(all_user_name[elem['owner_FromUserName']], all_user_name[elem['got_FromUserName']])

nx.draw_graphviz(H)
nx.write_dot(H, 'yaoq.dot')