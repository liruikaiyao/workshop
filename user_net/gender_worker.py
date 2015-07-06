#coding=utf-8
__author__ = 'Carry lee'


from gearman import GearmanWorker
from gender_class import Gender
from city_class import CityTag
from net_class import UserNet
import cPickle as pickle


def task_gender(GermanWorker, job):
    print 'hello!'
    para = pickle.loads(job.data)
    print para
    collection = para['collection_name']
    begin = para['begin']
    end = para['end']
    one = Gender(collection_name=collection, begin_name=begin, end_name=end)
    result=one.get_gender()
    print result
    return 'successful received gender'

def task_kanjia(GermanWorker, job):
    print 'hello!'
    para = pickle.loads(job.data)
    print para
    kanjia = para['kanjia']
    kanjiawu = para['kanjiawu']
    yaoqing = para['yaoqing']
    detail = para['detail']
    one = UserNet(kanjia_name=kanjia,kanjiawu_name=kanjiawu,yaoqing_name=yaoqing,detail_name=detail)
    if yaoqing is 'yaoqing':
        one.kanjia_net()
    else:
        one.yaoq()
    return 'successful received kanjia'

def task_city_tag(GermanWorker, job):
    print 'hello!'
    para = pickle.loads(job.data)
    print para
    collection = para['collection_name']
    begin = para['begin']
    end = para['end']
    one = CityTag(collection_name=collection, begin_name=begin, end_name=end)
    result=one.get_city_info()
    print result
    return 'successful received invite'


new_worker = GearmanWorker(['192.168.5.41:4730'])
new_worker.register_task("task_city", task_city_tag)
new_worker.register_task("task_kanjia", task_kanjia)
new_worker.register_task("task_gender", task_gender)
new_worker.work()