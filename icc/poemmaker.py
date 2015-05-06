#coding:utf-8

from __future__ import division
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pandas as pd
import numpy as np
from config.db import bda,attribute

all_cluster=bda['all_cluster']

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DefaultHandler(tornado.web.RequestHandler):
    def get(self,name):
        self.render('%s.html'%(name,))

class static_file(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

class PoemPageHandler(tornado.web.RequestHandler):
    
    def post(self):
        name = self.get_argument('name')
        cluster_type = self.get_argument('cluster_type')
        cluster_type=int(cluster_type)
        name_list_male=[]
        name_list_female=[]
        cursor=all_cluster.find_one({'key':name,'cluster':cluster_type})
        label=cursor['label']
        cursor=all_cluster.find({'cluster':cluster_type,'label':label})
        for elem in cursor:
            if elem['gender']==u'男':
                name_list_male.append(elem['key'])
            else:
                name_list_female.append(elem['key'])
        if name in name_list_female:
            name_list_female.remove(name)
        if name in name_list_male:
            name_list_male.remove(name)
        male_list=level_dict(name, name_list_male)
        female_list=level_dict(name, name_list_female)
        self.render('poem.html', male=male_list,female=female_list)

################################################################################

#if a、b is list
def getname(a):
    b=list()
    for elem in a:
        a=elem[0]+':'+'%.2f' %elem[1]
        b.append(a)
    return b

def distance(a,b):
    dis=np.linalg.norm(b-a)
    return dis

def name2array(name):
    name_data={}
    name_data[name]=all_cluster.find_one({'key':name})
    name_data=pd.DataFrame(name_data)
    name_data=name_data.T
    name_data=name_data.drop(['label','key','_id','cluster','gender'],axis=1)
    a=np.array(name_data)
    return a

def level_dict(name,name_list):
    list_level={}
    hg={}
    a=name2array(name)
    for elem in name_list:
        b=name2array(elem)
        list_level[elem]=distance(a, b)
    max_value=np.array(list_level.values()).max()
    min_value=np.array(list_level.values()).min()
    dump=max_value-min_value
    for k,v in list_level.items():
        hg[k]=(max_value-v)/dump*100
    c= sorted(hg.iteritems(), key=lambda d:d[1],reverse=True)
    e=getname(c)
    return e

###################################################################################    



if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        autoreload=True,
        handlers=[(r'/', IndexHandler),
                  (r'/poem', PoemPageHandler),
                  (r'/css/(.*)',static_file,{"path":os.path.join(os.path.dirname(__file__), "templates/css")}),
                  (r'/js/(.*)',static_file,{"path":os.path.join(os.path.dirname(__file__), "templates/js")}),
                  (r'/images/(.*)',static_file,{"path":os.path.join(os.path.dirname(__file__), "templates/images")}),
                  (r'/(.*).html',DefaultHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()