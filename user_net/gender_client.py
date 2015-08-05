# coding=utf-8
__author__ = 'Carry lee'

from gearman import GearmanClient
import os
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httputil
import gridfs
import logging
import mrjob
import bson
from config.db import ICCv1, mapreduce,client


class StaticFile(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")


class GenderHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        self.write('work received<br>')
        new_client = GearmanClient(['192.168.5.41:4730'])
        current_request = new_client.submit_job('task_gender','heal the world')
        new_result = current_request.result
        print new_result
        self.write('work finished')

class KanjiaHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        self.write('work received<br>')
        new_client = GearmanClient(['192.168.5.41:4730'])
        current_request = new_client.submit_job('task_kanjia','heal the world')
        new_result = current_request.result
        print new_result
        self.write('work finished')



class CityHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        self.write('work received<br>')
        new_client = GearmanClient(['192.168.5.41:4730'])
        current_request = new_client.submit_job('task_city','heal the world',
                                                wait_until_complete=False)
        new_result = current_request.result
        print new_result
        self.write('work finished')

class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        test = client['test']
        file_id = self.get_argument('file_id')
        some_id = bson.ObjectId(file_id)
        self.fs = gridfs.GridFS(test)
        some_one = self.fs.get(some_id)
        self.set_header('Content-Disposition', 'attachment; filename=someone.dot')
        self.write(some_one.read())
        some_one.close()

application = tornado.web.Application(
    autoreload=True,
    handlers=[
        (r"/kanjia", KanjiaHandler),
        (r"/gender", GenderHandler),
        (r"/city", CityHandler),
        (r"/download", DownloadHandler),
        (r'/static/(.*)', StaticFile,
         {"path": os.path.join(os.path.dirname(__file__), "templates/static")})],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

if __name__ == "__main__":
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
