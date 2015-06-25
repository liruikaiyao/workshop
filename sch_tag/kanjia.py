# coding=utf-8
__author__ = 'Carry lee'

from config.db import sch, ICCv1, test
from collections import defaultdict, Counter, OrderedDict
import networkx as nx
import matplotlib.pyplot as plt

desc = u"553db17b4796197c7c58a84f"
kanjia = sch['kanjia']
kanjiawu = sch['kanjiawu']
detail=sch['detail']
kanjia_net = OrderedDict()
identity_list = [elem['code'] for elem in kanjiawu.find().sort('__CREATE_TIME__', 1)]

for elem in identity_list:
    kanjia_net[elem] = []

for elem in kanjiawu.find().sort('__CREATE_TIME__', 1):
    every_key = []
    name = elem['name']
    cursor = kanjia.find({'memo.name':name})
    for item in cursor:
        every_key.append(item['identity_id'])
    kanjia_net[elem['code']] = list(set(every_key))


# 计算第一层用户

first_level = []
all_user = []

for k, v in kanjia_net.items():
    if k not in all_user:
        first_level.append(k)
        all_user.extend(v)
    else:
        all_user.extend(v)

print("first level: ",len(set(first_level)))

second_level = []
for elem in first_level:
    second_level.extend(kanjia_net[elem])

print("second level: ",len(set(second_level)-set(first_level)))

thirt_level = []
for elem in second_level:
    if elem in kanjia_net:
        thirt_level.extend(kanjia_net[elem])

print("third level: ",len(set(thirt_level)-set(second_level)-set(first_level)))

print("all_user: ",len(set(all_user)))

# 获取全部用户昵称
all_user_name=dict()
for elem in all_user:
    cursor = detail.find_one({'openid':elem})
    all_user_name[elem] = cursor['nickname']

# 输出前五名被砍最多的用户
a={k:len(set(v)) for k,v in kanjia_net.items()}
b= sorted(a.iteritems(), key=lambda d:d[1], reverse = True)
for elem in b[:5]:
    print elem[0], elem[1], all_user_name[elem[0]]


# 生成网图
G = nx.Graph()
for k, v in kanjia_net.items():
    for elem in v:
        G.add_edge(k, elem)

print(G.number_of_edges())
print(G.number_of_nodes())

# 过滤出度大于15的节点

new_net = {k: v for k, v in kanjia_net.items() if len(set(v)) > 15}
H = nx.Graph()
for k, v in new_net.items():
    for elem in v:
        H.add_edge(all_user_name[k], all_user_name[elem])

print(H.number_of_edges())
print(H.number_of_nodes())

nx.draw_graphviz(H)
nx.write_dot(H, 'some_user.dot')
