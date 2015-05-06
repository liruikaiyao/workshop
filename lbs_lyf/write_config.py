#coding=utf-8

from config.db import bda,ICCv1,umav3
import bson
source_db_info = bda['source_db_info']
d=bson.objectid.ObjectId('000000000000000000000000')
example=dict()
example['database']='ICCv1'
example['collection']='idatabase_collection_53eda5f8b1752ffe0b8b48f5'
example['last_id']=d
example['__REMOVED__']=False
example['ToUserName']='gh_60217269884e'
example['flag'] = False #False mean that no process is running
source_db_info.insert(example)