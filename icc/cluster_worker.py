# coding=utf-8

from gearman import GearmanWorker
from FromMongo import data_cluster
import json

def task_callback(gearman_worker,job):
    a = json.loads(job.data)
    from_col = a['from_col']
    fill_type = a['fill_type']
    attr_weight = a['attr_weight']
    needtransfer = a['needtransfer']
    Parameters = a['Parameters']
    demo = data_cluster(from_col,fill_type,attr_weight,needtransfer,Parameters)
    return 'successful received'

new_worker = GearmanWorker(['192.168.5.41:4730'])
new_worker.register_task("data_cluster", task_callback)
new_worker.work()