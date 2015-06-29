#coding=utf-8
__author__ = 'Carry lee'
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from config.db import ICCv1, mapreduce
from collections import defaultdict, Counter, OrderedDict
import networkx as nx
import json


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class static_file(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        kanjiawu_str = self.get_argument('kanjiawu')
        kanjia_str = self.get_argument('kanjia')
        detail_str = self.get_argument('detail')
        kanjia = ICCv1[kanjia_str]
        kanjiawu = ICCv1[kanjiawu_str]
        detail = ICCv1[detail_str]

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

        level_num = dict()
        first_level = []
        all_user = []

        for k, v in kanjia_net.items():
            if k not in all_user:
                first_level.append(k)
                all_user.extend(v)
            else:
                all_user.extend(v)

        level_num["first level"] = len(set(first_level))

        second_level = []
        for elem in first_level:
            second_level.extend(kanjia_net[elem])

        level_num["second level"] = len(set(second_level)-set(first_level))

        thirt_level = []
        for elem in second_level:
            if elem in kanjia_net:
                thirt_level.extend(kanjia_net[elem])

        level_num["third level"] = len(set(thirt_level)-set(second_level)-set(first_level))
        level_num["all_user"] = len(set(all_user))

        # 获取全部用户昵称
        all_user_name=dict()
        for elem in all_user:
            cursor = detail.find_one({'openid':elem})
            all_user_name[elem] = cursor['nickname']

        # 输出前十名被砍最多的用户
        ten_key_user=[]
        a={k:len(set(v)) for k,v in kanjia_net.items()}
        b= sorted(a.iteritems(), key=lambda d:d[1], reverse = True)
        for elem in b[:10]:
            ten_key_user.append([elem[0].encode('utf-8'), elem[1], all_user_name[elem[0]].encode('utf-8')])


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
            new_net[elem[0]] = kanjia_net[elem[0]]
        H = nx.Graph()
        for k, v in new_net.items():
            for elem in v:
                H.add_edge(all_user_name[k], all_user_name[elem])

        print(H.number_of_edges())
        print(H.number_of_nodes())

        nx.draw_graphviz(H)
        nx.write_dot(H, 'templates/static/some_user.dot')

        self.render('poem.html', level_num=level_num, ten_key_user=ten_key_user)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        autoreload=True,
        handlers=[(r'/', IndexHandler),
                  (r'/poem', PoemPageHandler),
                  (r'/static/(.*)',static_file,
                   {"path":os.path.join(os.path.dirname(__file__), "templates/static")})],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()