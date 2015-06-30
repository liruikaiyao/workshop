# coding=utf-8
__author__ = 'Carry lee'
from collections import Counter, OrderedDict
import datetime
import urllib2
import json
import networkx as nx
import gridfs

from config.db import ICCv1, sh, utc, mapreduce


class UserNet:
    def __init__(self, kanjiawu_name, kanjia_name, yaoqing_name, detail_name):
        self.kanjia_name = kanjia_name
        self.kanjiawu_name = kanjiawu_name
        self.yaoqing_name = yaoqing_name
        self.detail_name = detail_name
        self.kanjia = ICCv1[self.kanjia_name]
        self.kanjiawu = ICCv1[self.kanjiawu_name]
        self.yaoqing = ICCv1[self.yaoqing_name]
        self.detail = ICCv1[self.detail_name]
        self.fs = gridfs.GridFS(mapreduce)

    def kanjia_net(self):
        kanjia_net = OrderedDict()
        identity_list = [elem['code'] for elem in self.kanjiawu.find().sort('__CREATE_TIME__', 1)]

        for elem in identity_list:
            kanjia_net[elem] = []

        for elem in self.kanjiawu.find().sort('__CREATE_TIME__', 1):
            every_key = []
            name = elem['name']
            cursor = self.kanjia.find({'memo.name': name})
            for item in cursor:
                every_key.append(item['identity_id'])
            kanjia_net[elem['code']] = list(set(every_key))

        self.draw_dot(kanjia_net)

    def yaoq(self):

        yaoq_dict = OrderedDict()
        identity_list = [elem['owner_FromUserName'] for elem in
                         self.yaoqing.find().sort('__CREATE_TIME__', 1)]

        for elem in identity_list:
            yaoq_dict[elem]=[]

        for elem in self.yaoqing.find().sort('__CREATE_TIME__', 1):
            if elem['owner_FromUserName']==elem['got_FromUserName']:
                pass
            else:
                yaoq_dict[elem['owner_FromUserName']].append(elem['got_FromUserName'])

        self.draw_dot(yaoq_dict)

    def draw_dot(self, net_dict):
        # 计算第一层用户
        level_num = dict()
        first_level = []
        all_user = []

        for k, v in net_dict.items():
            if k not in all_user:
                first_level.append(k)
                all_user.extend(v)
                all_user.append(k)
            else:
                all_user.extend(v)

        level_num["first level"] = len(set(first_level))

        second_level = []
        for elem in first_level:
            second_level.extend(net_dict[elem])

        level_num["second level"] = len(set(second_level) - set(first_level))

        thirt_level = []
        for elem in second_level:
            if elem in net_dict:
                thirt_level.extend(net_dict[elem])

        level_num["third level"] = len(set(thirt_level) - set(second_level) - set(first_level))
        level_num["all_user"] = len(set(all_user))

        # 获取全部用户昵称
        all_user_name = dict()
        for elem in all_user:
            cursor = self.detail.find_one({'openid': elem})
            all_user_name[elem] = cursor['nickname']

        # 输出前十名被砍最多的用户
        ten_key_user = []
        a = {k: len(set(v)) for k, v in net_dict.items()}
        b = sorted(a.iteritems(), key=lambda d: d[1], reverse=True)
        for elem in b[:10]:
            ten_key_user.append([elem[0].encode('utf-8'),
                                 elem[1],
                                 all_user_name[elem[0]].encode('utf-8')])

        # 生成网图
        # G = nx.Graph()
        # for k, v in kanjia_net.items():
        #     for elem in v:
        #         G.add_edge(k, elem)
        #
        # print(G.number_of_edges())
        # print(G.number_of_nodes())

        # 过滤出度大于15的节点

        new_net = {}
        for elem in ten_key_user:
            new_net[elem[0]] = net_dict[elem[0]]
        H = nx.Graph()
        for k, v in new_net.items():
            for elem in v:
                H.add_edge(all_user_name[k], all_user_name[elem])

        print(H.number_of_edges())
        print(H.number_of_nodes())

        nx.draw_graphviz(H)
        nx.write_dot(H, 'some_user.dot')
        file_dot = open('some_user.dot', 'rb')
        data = file_dot.read()
        self.fs.put(data, filename='some_user.dot')

        return level_num