#coding=utf-8

from __future__ import division,unicode_literals
import urllib2
import json


########################################################################

########################################################################

def transfer(point):
    if isinstance(point[0],float):
        return oneTrans(point)
    else:
        return bigTrans(point)



def oneTrans(point):
    api_url = u'http://api.map.baidu.com/geoconv/v1/?'
    ak='SIpMcORCSogM916QMOz5tx7S'
    coords=''
    coords=coords+str(point[0])+','+str(point[1])
    result = urllib2.urlopen(api_url + 'coords='+ coords +'&ak='+ ak)
    b=result.read()
    c=json.loads(b)
    b=c['result'][0].values()[::-1]
    return b

def bigTrans(point):
    deal,remain = divmod(len(point),100)
    f=[]
    if remain==0:
        point = [point[i*100:i*100+100] for i in range(deal)]
    else:
        point = [point[i*100:i*100+100] for i in range(deal+1)]
    for elem in point:
        b=pointsTrans(elem)
        f.append(b)
    b=[item for elem in f for item in elem]
    return b

def pointsTrans(points):
    api_url = u'http://api.map.baidu.com/geoconv/v1/?'
    ak='SIpMcORCSogM916QMOz5tx7S'
    f=[]
    coords=''
    for elem in points:
        coords=coords+str(elem[0])+','+str(elem[1])+';'
    coords=coords.strip(';')
    result = urllib2.urlopen(api_url + 'coords='+ coords +'&ak='+ ak)
    b=result.read()
    c=json.loads(b)
    b=[elem.values()[::-1] for elem in c['result']]
    return b

