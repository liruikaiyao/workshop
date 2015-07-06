# coding=utf-8
__author__ = 'Carry lee'

from gearman import GearmanClient
import os
import cPickle as pickle
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httputil
import gridfs
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
        activity_info_config = mapreduce['gender_config']
        for elem in activity_info_config.find({"__REMOVED__": False,
                                               "is_running": False}):
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': True}})
            para = pickle.dumps(elem)
            current_request = new_client.submit_job('task_gender', para)
            new_result = current_request.result
            print new_result
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': False}})
        self.write('work finished')

class KanjiaHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        self.write('work received<br>')
        new_client = GearmanClient(['192.168.5.41:4730'])
        activity_info_config = mapreduce['kanjia_config']
        for elem in activity_info_config.find({"__REMOVED__": False,
                                               "is_running": False}):
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': True}})
            para = pickle.dumps(elem)
            current_request = new_client.submit_job('task_kanjia', para)
            new_result = current_request.result
            print new_result
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': False}})



class CityHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        self.write('work received<br>')
        new_client = GearmanClient(['192.168.5.41:4730'])
        activity_info_config = mapreduce['city_tag_config']
        for elem in activity_info_config.find({"__REMOVED__": False,
                                               "is_running": False}):
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': True}})
            para = pickle.dumps(elem)
            current_request = new_client.submit_job('task_invite', para)
            new_result = current_request.result
            print new_result
            activity_info_config.update({'_id': elem['_id']},
                                        {'$set':{'is_running': False}})
        self.write('work finished')

class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        self.deal()

    def post(self):
        self.deal()

    def deal(self):
        file_name = self.get_argument('file_name')
        print file_name
        test = client['test']
        self.fs = gridfs.GridFS(test)
        files = test['fs.files']
        some_id = files.find_one({'filename':file_name})['_id']
        some_one = self.fs.get(some_id)
        self.set_header('Content-Disposition', 'attachment; filename=some.dot')
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
    autoescape=None
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
