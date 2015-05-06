#coding=utf-8
from __future__ import division
from config.db import bda
import time
import datetime
import hashlib
import json
import numpy as np
import pandas as pd
from xlwt import Workbook


all_cluster=bda['all_cluster']
alldb = bda.collection_names()
onlydb = []
for elem in alldb:
    if len(elem) == 32:
        onlydb.append(elem)
print len(onlydb)


for elem in onlydb:
    cluster_doc = bda[elem]
    label=[]
    for item in cluster_doc.find():
        label.append(item['label'])
    cluster = len(set(label))
    for item in cluster_doc.find():
        cluster_doc.update({'_id': item['_id']}, {"$set": {"cluster": cluster}})

cluster_central=bda['cluster_central']
time=[]
for elem in cluster_central.find():
    time.append(elem['time'])
for elem in onlydb:
    cluster_doc=bda[elem]
    for item in cluster_doc.find():
        label=item['label']
        cluster=item['cluster']
        checker=cluster_central.find_one({'time':time[cluster-1]})
        cluster_attr=checker[str(label)]
        cluster_doc.update({'_id': item['_id']}, {"$set": {"cluster_attr": cluster_attr}})


for elem in onlydb:
    cluster_doc=bda[elem]
    for item in cluster_doc.find():
        all_cluster.insert(item)