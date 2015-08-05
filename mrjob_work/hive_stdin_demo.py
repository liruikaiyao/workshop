# coding=utf-8
__author__ = 'Carry lee'
import sys
import re
from user_agents import parse
from collections import OrderedDict

log_file = open('G:\demo.log')

for log in log_file:
    line = log.split('\t')[7]
    event_date = log.split('\t')[-1]
    log = '\t'.join(log.split('\t')[:-1])
    ua_parse = parse(line)
    ua_parse_str = str(ua_parse)
    ua_parse_list = ua_parse_str.strip().split('/')
    ua_parse_list = [elem.strip() for elem in ua_parse_list]
    tags = OrderedDict()

    MicroMessenger = re.search(r'MicroMessenger/[\d,.]*', line)
    try:
        tags['MicroMessenger'] = MicroMessenger.group().split('/')[1]
    except AttributeError:
        tags['MicroMessenger'] = '-'
    NetType = re.search(r'NetType/[\w]*', line)
    try:
        tags['NetType'] = NetType.group().split('/')[1]
    except AttributeError:
        tags['NetType'] = '-'

    for k, v in tags.items():
        if v == '':
            tags[k] = '-'
    new_tags = ['MicroMessenger '+tags['MicroMessenger'], 'NetType '+tags['NetType'], event_date]
    new_tags = [elem.strip() for elem in new_tags]
    result =  log+'\t'+'\t'.join(ua_parse_list) + '\t' + '\t'.join(new_tags)
    if len(result.split('\t'))!=23:
        print result
