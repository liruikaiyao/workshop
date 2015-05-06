# encoding : utf-8

from __future__ import division
from config.db import user_clear
from pandas import Series, DataFrame
from lifelines import KaplanMeierFitter
import pandas as pd
from matplotlib import rcParams
from numpy import array
rcParams['figure.dpi'] = 160
rcParams['figure.figsize'] = (16,12)


duration = []
observed = []
group = []

for elem in user_clear.find():
    #if elem['duration'] <=15552000:
    duration.append(elem['duration']/86400)
    observed.append(elem['observed'])
    group.append(elem['gender'])
dura_obj = array(duration)
obs_obj = array(observed)
group_obj = array(group)
DataFrame(dura_obj,index=group_obj)
DataFrame(obs_obj,index=group_obj)
male = group_obj ==1
female = group_obj ==2
other = group_obj ==0

kmf = KaplanMeierFitter()
kmf.fit(dura_obj[male],obs_obj[male], label = 'male')
ax = kmf.plot()
kmf.fit(dura_obj[female],obs_obj[female], label = 'female')
kmf.plot(ax=ax)
#kmf.fit(dura_obj,obs_obj, label = 'both')
#kmf.plot(ax=ax)
#kmf.fit(dura_obj[other],obs_obj[other], label = 'other')
#kmf.plot(ax=ax)
ax.set_xlim(0,1)
ax.set_ylim(0.85,1.0)
ax.get_figure().savefig('maleAndFemale_day')