# coding:utf-8
from __future__ import division
import heatmap
import gridfs
import tempfile
from config.db import db, weibo_lbs


fs = gridfs.GridFS(db)
hm = heatmap.Heatmap()
result = tempfile.gettempdir()

# 传入时间为时间戳格式


class UserLbs:
    def __init__(self, a_dist, a_center, a_time_start, a_time_end):
        self.dist = a_dist  # float
        self.center = a_center  # [float,float]
        self.time_start = a_time_start
        self.time_end = a_time_end

        radius = 6371

        cursor = weibo_lbs.aggregate([{'$geoNear': {'near': self.center,
                                                    'distanceField': 'dist',
                                                    'num': 1000000,
                                                    'maxDistance': self.dist / radius,
                                                    'query': {
                                                        'time_stamp': {'$gte': self.time_start, '$lte': self.time_end}},
                                                    'spherical': 'true',
                                                    'distanceMultiplier': radius}},
                                      {'$sort': {'time_stamp': -1}}
        ])  # 6371 Km
        within_lbs = cursor['result']
        print len(within_lbs)
        user = {}
        f = []
        for elem in within_lbs:
            if elem['uid'] in user:
                if len(user[elem['uid']]) == 3:
                    pass
                else:
                    user[elem['uid']].append(tuple(elem['loc']))
            else:
                user[elem['uid']] = [tuple(elem['loc'])]
        for item in user.keys():
            if len(user[item]) == 1:
                for i in range(0, 3):
                    f.extend(user[item])
            elif len(user[item]) == 2:
                f.extend(user[item])
                f.append(user[item][0])
            else:
                f.extend(user[item])

        print len(f)
        print len(user)
        hm.heatmap(f, 10, 128, size=(4096, 4096))
        hm.saveKML('G:\weibo_5.kml')


if __name__ == '__main__':
    klx = UserLbs(50, [121.435101153, 31.1952376167], 1385740800, 1405995856)