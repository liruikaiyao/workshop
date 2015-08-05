# coding=utf-8
from __future__ import division
import time
from config.db import sch
from pandas import Series, DataFrame
from lifelines import KaplanMeierFitter
import pandas as pd
from matplotlib import rcParams
from numpy import array

rcParams['figure.dpi'] = 160
rcParams['figure.figsize'] = (16, 12)

class ToUser(object):
    def __init__(self, events, users):
        self.events = events
        self.users = users
        self.hyd_events = sch[self.events]
        self.hyd_users = sch[self.users]

    def data_fit(self):
        user_list = []
        self.hyd_events.create_index('FromUserName')
        self.hyd_events.create_index('Event')
        self.hyd_users.create_index('openid')
        for elem in self.hyd_events.find({'Event': 'subscribe'}):
            user_list.append(elem['FromUserName'])
        user_list = list(set(user_list))
        print len(user_list)
        now_time = time.time()

        # add subscribe time
        # three tag: pic, text, event
        # format: 'user_id':'', 'sub_time':'', 'unsub_time':'', 'event':''.
        duration = []
        observed = []
        group = []

        time_block = []
        for elem in user_list:
            user_dict = {}
            for item in self.hyd_events.find({'FromUserName': elem}):
                time_block.append(item['CreateTime'])
            earlist = min(time_block)
            latest = max(time_block)
            sub_time = int(earlist)
            curt = self.hyd_events.find_one({'$and': [{'FromUserName': elem}, {'Event': 'unsubscribe'}]})
            if curt is None:
                unsub_time = int(now_time)
                user_dict['observed'] = 0
            else:
                unsub_time = int(latest)
                user_dict['observed'] = 1

            try:
                user_dict['duration'] = abs(unsub_time - sub_time)
            except Exception, e:
                print e
                print unsub_time
                print sub_time
            check = self.hyd_users.find_one({'openid': elem})
            # if gender exists, set it, if not, set gender=0, which means gender unknow
            try:
                user_dict['gender'] = check['sex']
            except TypeError:
                user_dict['gender'] = 0

            duration.append(user_dict['duration'] / 86400)
            observed.append(user_dict['observed'])
            group.append(user_dict['gender'])
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
            ax.get_figure().savefig('maleAndFemale')

if __name__ == '__main__':
    ToUser(events='ev', users='use')
