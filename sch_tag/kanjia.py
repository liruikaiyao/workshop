# coding=utf-8
__author__ = 'Carry lee'

from config.db import sch, ICCv1, test
from collections import defaultdict, Counter, OrderedDict
import networkx as nx
import matplotlib.pyplot as plt

desc = u"553db17b4796197c7c58a84f"
kanjia = sch['kanjia']
kanjiawu = sch['kanjiawu']
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
    kanjia_net[elem['code']].extend(list(set(every_key)))

# 计算第一层用户


first_level = []
all_user = []

for k, v in kanjia_net.items():
    if k not in all_user:
        first_level.append(k)
        all_user.extend(v)
    else:
        all_user.extend(v)

print(len(set(first_level)))

second_level = []
for elem in first_level:
    second_level.extend(kanjia_net[elem])

print(len(set(second_level)-set(first_level)))

thirt_level = []
for elem in second_level:
    if elem in kanjia_net:
        thirt_level.extend(kanjia_net[elem])

print(len(set(thirt_level)-set(second_level)-set(first_level)))

print(len(set(all_user)))

# 生成网图
G=nx.Graph()
for k,v in kanjia_net.items():
    for elem in v:
        G.add_edge(k,elem)

print(G.number_of_edges())
print(G.number_of_nodes())

