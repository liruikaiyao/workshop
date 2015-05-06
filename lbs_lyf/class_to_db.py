from config.db import client
import pymongo


class ClassName(object):

    """docstring for ClassName

    from_db = 源数据库
    to_db = 目的数据库
    to_id = 选择关键字



    """

    def __init__(self, *args, **kwargs):
        self.from_db = kwargs['from_db']
        self.to_db = kwargs['to_db']
        self.to_id = kwargs['to_id']

    def data_clean(self):
        #定义文档
        weixin_all = client[self.from_db]['weixin']
        weixin = client[self.to_db]['weixin']
        # 建立索引
        weixin_all.ensureIndex(('ToUserName', pymongo.ASCENDING))
        # 转存指定ToUserName的微信内容
        for elem in weixin_all.find({'ToUserName': self.to_id}):
            weixin.insert(elem)
    # 建立索引
        weixin.ensureIndex([('FromUserName', pymongo.ASCENDING),
                            ('Event', pymongo.ASCENDING), ('createTime', pymongo.DESCENDING)])
        
        return 'cleaned data'
