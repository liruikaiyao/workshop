#coding=utf-8
__author__ = 'Carry lee'


from gearman import GearmanWorker
from gender_class import Gender
from city_class import CityTag
from net_class import UserNet
import pickle
import datetime
from config.db import mapreduce,utc


def task_gender(germanWorker,job):
    print 'hello!'
    para = pickle.loads(job.data)
    print para
    # collection = para['collection_name']
    # begin = para['begin']
    # end = para['end']
    # one = Gender(collection_name=collection, begin_name=begin, end_name=end)
    # result=one.get_gender()
    # print result
    return 'successful received gender'

def task_kanjia(GermanWorker, job):
    print 'hello!'
    print job.data
    activity_info_config = mapreduce['kanjia_config']
    print (activity_info_config.find_one())
    for elem in activity_info_config.find({"__REMOVED__": False,
                                           "is_running": False}):
        activity_info_config.update({'_id': elem['_id']},
                                    {'$set': {'is_running': True,
                                              '__MODIFY_TIME__': datetime.datetime.now(utc)}})

        kanjia = elem['collection_name_kanjia']
        kanjiawu = elem['collection_name_kanjiawu']
        yaoqing = elem['collection_name_yaoqing']
        detail = elem['collection_name']
        print kanjia,kanjiawu,yaoqing,detail
        one = UserNet(kanjia_name=kanjia, kanjiawu_name=kanjiawu,
                      yaoqing_name=yaoqing,detail_name=detail)
        if yaoqing == u'yaoqing':
            one.kanjia_net()
        else:
            one.yaoq()
        activity_info_config.update({'_id': elem['_id']},
                            {'$set': {'is_running': False,
                                      '__MODIFY_TIME__': datetime.datetime.now(utc)}})

    return 'successful received kanjia'

def task_city_tag(GermanWorker, job):
    print ('city_tag work received')
    print job.data
    activity_info_config = mapreduce['city_tag_config']
    print (activity_info_config.find_one())
    for elem in activity_info_config.find({"__REMOVED__": False,
                                           "is_running": False}):
        activity_info_config.update({'_id': elem['_id']},
                                    {'$set': {'is_running': True,
                                              '__MODIFY_TIME__': datetime.datetime.now(utc)}})

        begin = elem['begin']
        end = elem['end']
        detail = elem['collection_name']
        one = CityTag(begin_name=begin,end_name=end,collection_name=detail)
        result = one.get_city_info()
        print result
    return 'successful finished city_tag job'


new_worker = GearmanWorker(['192.168.5.41:4730'])
new_worker.register_task("task_city", task_city_tag)
new_worker.register_task("task_kanjia", task_kanjia)
new_worker.register_task("task_gender", task_gender)
new_worker.work()