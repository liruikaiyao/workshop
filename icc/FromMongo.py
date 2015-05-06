#coding=utf-8
from __future__ import division
from config.db import bda
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import hashlib
import time
import datetime
import calendar




########################################################################
class data_cluster:
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self,from_col,fill_type,attr_weight,needtransfer,Parameters):
        """Constructor"""
        self.from_col = from_col    #源数据集合
        self.fill_type = fill_type    #填充缺失值类型
        self.attr_weight = attr_weight    #权重
        self.needtransfer = needtransfer    #时间转换
        self.Parameters = Parameters    #聚类参数
        data = str(self.from_col)+str(self.fill_type)+str(self.attr_weight)+str(self.needtransfer)+str(self.Parameters)
        new_db = hashlib.md5(data).hexdigest()
        print new_db
        cluster_doc = bda[new_db]
        g = dict()
        for elem in self.from_col:
            col = elem['col']
            key = elem['key']
            attribute = elem['attribute']
            col2 = bda[col]
            for elem in col2.find():
                if elem.has_key(key) and elem[key] != '':
                    g[elem[key]]=dict()
                    for item in attribute:
                        if elem.has_key(item):
                            if isinstance(elem[item],bool):
                                g[elem[key]][item] = elem[item] and 1 or 0
                            elif isinstance(elem[item], (int, float, long)):
                                g[elem[key]][item] = elem[item]
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
        #print g.items()[1]
#将合并好的数据写入新集合
        for elem in g.items():
            h = elem[1]
            h['key'] = elem[0]
            cluster_doc.insert(h)
        #print g.items()[1]
            #将datetime obj转换为 UNIX 时间戳
        #standard = datetime.datetime(1970, 1, 1, 0, 0)
        #for item in g.keys():
            #for elem in self.needtransfer:
                #if g[item].has_key(elem):
                    #if g[item][elem] == standard:
                        #g[item][elem] = 0
                    #elif isinstance(g[item][elem],datetime.datetime):
                        #g[item][elem] = time.mktime(g[item][elem].timetuple())
        
        c_mat = pd.DataFrame(g)
        c_mat = c_mat.T
        c_mat = c_mat.drop('_id',axis=1)
        c_mat = c_mat.drop('key',axis=1)
        #print c_mat.columns
        #print c_mat.ix[1]
        #填补缺失值
        #for elem in self.needtransfer:
        #c_mat[elem] = c_mat[elem].fillna(0)
        if self.fill_type is not {}:
            for k,v in self.fill_type.items():
                if isinstance(v, (int, float, long)):
                    c_mat[k] = c_mat[k].fillna(v)
                elif v==u'mean':
                    c_mat[k] = c_mat[k].fillna(c_mat[k].mean())
                elif v==u'median':
                    c_mat[k] = c_mat[k].fillna(c_mat[k].median())
                else:
                    pass
        c_mat = c_mat.fillna(0)
        #数据归一化
        #print c_mat.ix[0]
        #for elem in c_mat.columns:
            #print c_mat.columns
            #if c_mat[elem].max()-c_mat[elem].min() == 0:
                #pass
            #else :
                #c_mat[elem] = c_mat[elem]/(c_mat[elem].max()-c_mat[elem].min())
        
        #特征加权处理
        if self.attr_weight is not {}:
            for k,v in self.attr_weight.items():
                c_mat[k] = c_mat[k] * v
        
        #初始化聚类核心
        init_para = self.Parameters['init']
        if isinstance(init_para,dict):
            for elem in init_para.keys():
                for item in self.needtransfer:
                    if init_para.has_key(item):
                        if isinstance(init_para[elem][item], datetime.datetime):
                            init_para[elem][item] = time.mktime(init_para[elem][item].timetuple())
                        else:
                            pass
                    else:
                        pass
            init_para = pd.DataFrame(init_para)
            init_para = init_para.T
            init_para = np.array(init_para)
        else:
            pass
        
        #聚类
        c_mat = pd.DataFrame(c_mat,dtype=np.float64)
        est = KMeans(n_clusters = self.Parameters['n_clusters'],init = init_para,
                     max_iter = self.Parameters['max_iter'],n_init = self.Parameters['n_init'],
                     precompute_distances = self.Parameters['precompute_distances'],
                     tol = self.Parameters['tol'],n_jobs = self.Parameters['n_jobs'])
        est.fit(c_mat)

        #est.cluster_centers_   聚类中心点数组
        #est.labels_    聚类结果标签
        #将分类结果返回到数据结合中
        _labels = list(est.labels_)[::-1]
        for elem in c_mat.index:
            a = _labels.pop()
            cluster_doc.update({'key': elem}, {"$set": {"label": a}})
            cluster_doc.update({'key': elem}, {"$set": {"cluster": self.Parameters['n_clusters']}})

        #讲分类中心点插入新的集合
        cluster_central = bda['cluster_central']
        h=pd.DataFrame(est.cluster_centers_,columns=c_mat.columns)
        a=len(list(h.index))
        b=dict()
        ti = time.time()
        for i in range(a):
            b[str(i)]=(dict(h.ix[i]))
        b['time']=ti
        cluster_central.insert(b)


#if __name__ == '__main__':
    #demo = data_cluster([{'col':'start_time','key':'name','attribute':["2014-11-21",
                                                                    #"2014-11-20",
                                                                    #"2014-11-24",
                                                                    #"2014-10-28",
                                                                    #"2014-10-29",
                                                                    #"2014-10-27",
                                                                    #"2014-10-24",
                                                                    #"2014-10-22",
                                                                    #"2014-10-23",
                                                                    #"2014-10-20",
                                                                    #"2014-10-21",
                                                                    #"2014-11-14",
                                                                    #"2014-11-17",
                                                                    #"2014-11-10",
                                                                    #"2014-11-11",
                                                                    #"2014-11-12",
                                                                    #"2014-11-13",
                                                                    #"2014-11-18",
                                                                    #"2014-11-19",
                                                                    #"2014-10-31",
                                                                    #"2014-10-30",
                                                                    #"2014-11-03",
                                                                    #"2014-11-07",
                                                                    #"2014-11-06",
                                                                    #"2014-11-05",
                                                                    #"2014-11-04"]}],
                        #{},
                        #{},
                        #[],
                        #{'n_clusters':99,'max_iter':300,'n_init':10,'init':'k-means++',
                         #'precompute_distances':True,'tol':1e-4,'n_jobs':1})