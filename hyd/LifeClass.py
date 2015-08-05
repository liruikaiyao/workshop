# coding=utf-8
from __future__ import division
from pandas import Series, DataFrame
from lifelines import KaplanMeierFitter
import pandas as pd
from matplotlib import rcParams
from numpy import array
from config.db import sch

rcParams['figure.dpi'] = 160
rcParams['figure.figsize'] = (16, 12)

after_users = sch['']


class LifeLine:
    def __init__(self, db, male=False, female=False, other=False, both=True):
        self.db = db
        self.male = male
        self.female = female
        self.other = other
        self.both = both

        duration = []
        observed = []
        group = []

        for elem in self.db.find():
            duration.append(elem['duration'] / 86400)
            observed.append(elem['observed'])
            group.append(elem['gender'])
        dura_obj = array(duration)
        obs_obj = array(observed)
        group_obj = array(group)
        DataFrame(dura_obj, index=group_obj)
        DataFrame(obs_obj, index=group_obj)
        male = group_obj == 1
        female = group_obj == 2
        other = group_obj == 0

        kmf = KaplanMeierFitter()
        kmf.fit(dura_obj, obs_obj, label='both')
        ax = kmf.plot()
        if self.male is True:
            kmf.fit(dura_obj[male], obs_obj[male], label='male')
            kmf.plot(ax=ax)
        if self.female is True:
            kmf.fit(dura_obj[female], obs_obj[female], label='female')
            kmf.plot(ax=ax)
        if self.other is True:
            kmf.fit(dura_obj[other], obs_obj[other], label='other')
            kmf.plot(ax=ax)
        # ax.set_xlim(19,22)
        # ax.set_ylim(1,2)
        ax.get_figure().savefig('maleAndFemale')


if __name__ == '__main__':
    LifeLine(after_users, True, True, True, True)
