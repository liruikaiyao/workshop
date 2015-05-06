#coding=utf-8

from __future__ import division
from config.db import lyf,store_lyf
from config.CoordTransfer import transfer
import numpy as np
import pandas as pd
import simplekml
import datetime
from collections import OrderedDict
import time
import json
import urllib2
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

store_area = lyf['store_area']
user_level=lyf['user_level']

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class static_file(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MapHandler(tornado.web.RequestHandler):
    def post(self):
        StoreName= self.get_argument('name')
        cursor= user_level.find_one({'store_name':StoreName})
        storeId=cursor['store_id']
        store_info=cursor
        store_info['loc']=transfer(store_lyf.find_one({'store_name':StoreName})['loc'])
        store_info.pop('level')
        store_info.pop('_id')
        store_info = json.dumps(store_info)
        pointList=list()
        cursor = store_area.find({'store_id':storeId})
        for elem in cursor:
            pointList.append(elem['lbs'])
        pointList=json.dumps(transfer(pointList))
        self.render('map.html', store_info = store_info,pointList=pointList)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        autoreload=True,
        handlers=[(r'/', IndexHandler),
                  (r'/map', MapHandler),
                  (r'/images/(.*)',static_file,{"path":os.path.join(os.path.dirname(__file__), "templates/static/images")}),
                  (r'/static/(.*)',static_file,{"path":os.path.join(os.path.dirname(__file__), "templates/static")})],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()