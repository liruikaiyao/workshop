# coding=utf-8
from __future__ import division
from config.db import lyf_net
str_len=len #复制len函数以防止被snap中的函数占用
from snap import TNGraph,TIntStrH,SaveGViz
from binascii import crc32
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os


#删除数据中自邀请数据
count=0
for elem in lyf_net.find():
    if elem['owner_FromUserName'] == elem['got_FromUserName']:
        lyf_net.remove({'_id':elem['_id']})
        count+=1
print count
#网络
graph_lyf = TNGraph.New()
NIdLabelH = TIntStrH()
node=[]
name_dict={}
for elem in lyf_net.find():
    node.append(crc32(elem['owner_FromUserName']))
    name_dict[crc32(elem['owner_FromUserName'])]=elem['memo']['owner_nickname']
    node.append(crc32(elem['got_FromUserName']))
    name_dict[crc32(elem['got_FromUserName'])]=elem['memo']['friend_nickname']
    
node=list(set(node))
for item in node:
    graph_lyf.AddNode(item)
    NIdLabelH.AddDat(item, str(name_dict[item]))
    
for elem in lyf_net.find():
    graph_lyf.AddEdge(crc32(elem['owner_FromUserName']),crc32(elem['got_FromUserName']))

        
SaveGViz(graph_lyf, "g1.dot", "Graph file", NIdLabelH)

#修改为中文显示
newline='  node  [shape=ellipse, fontname="FangSong", width=0.3, height=0.3]\n'
data=open('g1.dot','r+')
f=data.readlines()
f[6]=newline
#print str_len(f)
#for i in range(0,str_len(f)):
    #f[i]=f[i].replace('dtype: object','')
data=open('g1.dot','w+')
data.writelines(f)
data.close()
#生成图片
os.system('dot -Tpng g1.dot -o g1.png')

