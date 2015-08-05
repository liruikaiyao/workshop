#coding=utf-8
__author__ = 'Carry lee'
import os
import time

path_ab = ['/home/ngx_proxy_logs/proxy01_old','/home/ngx_proxy_logs/proxy02_old']


for elem in path_ab:
    path_file = os.walk(elem).next()
    start = time.time()
    print len(path_file[2])
    path_big=[]
    for item in path_file[2]:
        if item.split('-')[-1]>'20150501' and 'schwarzkopf' in item:
            abs_path = elem+'/'+item
            path_big.append(abs_path)
    print len(path_big)
    print time.time()-start