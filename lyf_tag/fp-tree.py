# coding=utf-8
__author__ = 'Carry lee'
import fim
from config.db import ICCv1

lyf_tag_log = ICCv1['lyf_tag_log']
lyf_tag_list = ICCv1['lyf_tag_list']
items = [str(elem['_id']) for elem in lyf_tag_list.find()]
sample = [elem['tags'] for elem in lyf_tag_log.find()]

tag_dict = dict()
for elem in lyf_tag_list.find():
    tag_dict[str(elem['_id'])] = elem['tag']

all_tag = []
for elem in sample:
    all_tag.extend(elem)

diff = set(all_tag) - set(items)

for elem in diff:
    tag_dict[elem] = ''

res = fim.eclat(sample, supp=50)

# 根据tag_dict显示tag中文名称


def element(lis):
    for elem in lis:
        if isinstance(elem, unicode):
            print tag_dict[elem]
        elif isinstance(elem, int):
            print elem
        else:
            element(elem)
