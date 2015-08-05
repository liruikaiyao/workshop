# coding=utf-8
__author__ = 'Carry lee'
import pandas as pd
from config.db import pattern, mapreduce, utc
import os
import pygrok
import time
import datetime
from multiprocessing import Pool

finished_nginx_log = mapreduce['finished_nginx_log']

key_order = ['source_ip', '', 'remote_user', 'timestamp', 'request', 'status', 'http_referer',
             'http_user_agent', 'request_length', 'body_bytes_sent', 'bytes_sent', 'upstream_addr',
             'upstream_response_time', 'request_time', 'phpsessid', 'urm_id', '']

def parse_file(path):
    files = open(path)
    new_files = open(path.replace('_old',''), mode='w')
    for elem in files:
        fields= []
        nginx_dict = pygrok.grok_match(elem, pattern['nginx'])
        for item in key_order:
            if item=='':
                fields.append('-')
            else:
                fields.append(nginx_dict[item])
        fields = '\t'.join(fields)+'\n'
        new_files.write(fields)
    files.close()
    new_files.close()
    one = {'log_name': path, '__CREATE_TIME__':datetime.datetime.now(utc)}
    finished_nginx_log.insert_one(one)


path_ab = ['/home/ngx_proxy_logs/proxy01_old','/home/ngx_proxy_logs/proxy02_old']

pool = Pool(8)

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
    pool.map(parse_file, path_big)
    print time.time()-start

pool.close()
pool.join()
