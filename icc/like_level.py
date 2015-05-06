from __future__ import division
import pandas as pd
import numpy as np
from config.db import bda,attribute


#if a、b is list
def distance(a,b):
    dis=np.linalg.norm(b-a)
    return dis

def name2array(name):
    name_data={}
    name_data[name]=all_cluster.find_one({'key':name})
    name_data=pd.DataFrame(name_data)
    name_data=name_data.T
    name_data=name_data.drop(['label','key','_id','cluster','gender'],axis=1)
    a=np.array(name_data)
    return a

def level_dict(name,name_list):
    list_level={}
    a=name2array(name)
    for elem in name_list:
        b=name2array(elem)
        list_level[elem]=distance(a, b)
    b= sorted(list_level.iteritems(), key=lambda d:d[1])
    return b

########################################################################
all_cluster=bda['all_cluster']
name='李瑞凯'
cluster_type=56
name_list_male=[]
name_list_female=[]
cursor=all_cluster.find_one({'key':name,'cluster':cluster_type})
label=cursor['label']
cursor=all_cluster.find({'cluster':cluster_type,'label':label})
for elem in cursor:
    if elem['gender']==u'男':
        name_list_male.append(elem['key'])
    else:
        name_list_female.append(elem['key'])

male_list=level_dict(name, name_list_male)
female_list=level_dict(name, name_list_female)

for elem in male_list:
    for k,v in elem:
        print k+':'+v

