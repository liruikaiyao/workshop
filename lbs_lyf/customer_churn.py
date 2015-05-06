#coding=utf-8


from __future__ import division
from config.db import lyf

from pandas import Series, DataFrame
from lifelines import KaplanMeierFitter
import pandas as pd
from numpy import array
import matplotlib.pyplot as plt


survival=lyf['survival']
store_area=lyf['store_area']


def surAnalysis(storeId):
    duration = []
    observed = []
    
    for elem in survival.find({'store_id':storeId}):
        duration.append(elem['duration']/86400)
        observed.append(elem['observed'])
    if duration==[]:
        pass
    else:
        dura_obj = array(duration)
        obs_obj = array(observed)
        
        kmf = KaplanMeierFitter()
        kmf.fit(dura_obj,obs_obj)
        ax = kmf.plot()
        #ax.set_xlim(0,1)
        #ax.set_ylim(0.85,1.0)
        ax.get_figure().savefig('F:\workshop\lbs_lyf\static\images\\' + storeId)
        plt.close(ax.get_figure())
