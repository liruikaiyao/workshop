#coding=utf-8
from __future__ import division
from sklearn.cluster import KMeans
from config.db import bda
import numpy as np
import pandas as pd
import datetime
import json


###############################################
def str2time(string):
    b = string.split(':')
    c=datetime.time(int(b[0]),int(b[1]))
    return c
##############################################

xls_file = pd.ExcelFile('G:\data\work_time.xlsx')
table = xls_file.parse('bigdata')

cluster_doc = bda['start_time']

a,b = table.shape
work_start = {}
for elem in np.arange(a):
    if work_start.has_key(table.ix[elem]['name']):
        pass
    else:
        work_start[table.ix[elem]['name']]={}
    day = table.ix[elem]['attendance_time'].split(' ')[0]
    time = table.ix[elem]['attendance_time'].split(' ')[1]
    time=str2time(time)
    minute = time.hour*60+time.minute
    if 420<minute<720:
        work_start[table.ix[elem]['name']][day] = minute

work_start = pd.DataFrame(work_start)
for elem in work_start.columns:
    if not isinstance(elem,unicode):
        work_start =  work_start.drop(elem,axis=1)
#start_time = datetime.date(2014,1,1)
#for elem in work_start.index:
    #if elem < start_time:
        #work_start =  work_start.drop(elem,axis=0)
a,b = work_start.shape
#work_end[work_end<720]=np.NaN    #丢弃加班时间
work_start = work_start.fillna(work_start.mean())
work_start = work_start.T


#将数据插入到数据库
alona = work_start
length=len(alona)
for i in np.arange(length):
    g={}
    h={}
    g=dict(alona.ix[i])
    for k,v in g.items():
        h[k]=v
    h['name']=alona.ix[i].name
    cluster_doc.insert(h)


#函数
def int2time(num):
    a,b=divmod(num,60)
    return datetime.time(a,b)

def matrix_int2time(matrix):
    a,b=matrix.shape
    g={}
    for i in np.arange(a):
        g[matrix.ix[i].name]={}
        g[matrix.ix[i].name] = dict(matrix.ix[matrix.index[i]])
    a=list(matrix.index)
    b=list(matrix.columns)
    for i in a:
        for j in b:
            g[i][j] = int2time(g[i][j])
    h=pd.DataFrame(g)
    h=h.T
    return h

def str2time(string):
    b = string.split(':')
    c=datetime.time(int(b[0]),int(b[1]))
    return c

def str2date(string):
    b = string.split('-')
    c=c=datetime.date(int(b[0]),int(b[1]),int(b[2]))
    return c

#数据库取数据，字符串转为datetime格式
def str2datetime(diction):
    c=dict()
    for k,v in diction.items():
        c[k]=dict()
        for i,j in v.items():
            c[k][str2date(i)]=str2time(j)
    return c
