# coding = utf-8

from gearman import GearmanWorker
from weibo_class import UserLbs
import json


def task_callback(job):
    print job.data
    a = json.loads(job.data)
    dist = a['dist']
    center = [a['center']['lng'], a['center']['lat']]
    start = a['time_start']
    end = a['time_end']
    klx = UserLbs(dist, center, start, end)
    return 'successful received'


new_worker = GearmanWorker(['192.168.5.41:4730'])
new_worker.register_task("user_lbs", task_callback)
new_worker.work()