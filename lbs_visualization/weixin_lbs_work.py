# coding = utf-8
import os
import gearman
import math
from gearman import GearmanWorker
from lbs_class import user_lbs
import json

def task_callback(gearman_worker, job):    
    print job.data
    a = json.loads(job.data)
    store = a['store']
    dist = a['dist']
    center = [a['center']['lng'],a['center']['lat']]
    start = a['time_start']
    end = a['time_end']
    klx = user_lbs(store,dist,center,start,end)
    return 'successful received'

new_worker = GearmanWorker(['192.168.5.41:4730'])
new_worker.register_task("user_lbs", task_callback)
new_worker.work()