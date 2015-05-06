#coding:utf-8

from config.db import bda

all_cluster=bda['all_cluster']
db_list=bda.collection_names()
a=db_list
db_list=[]
for elem in a:
    if len(elem)==32:
        db_list.append(elem)

for elem in db_list:
    db=bda[elem]
    for item in db.find():
        all_cluster.insert(item)
