from __future__ import division
from config.db import hyd_events
import matplotlib.pyplot as plt

class survival:
    def __init__(self, db):
        self.db = db
        user_list = []
        for elem in self.db.find({'Event':'unsubscribe'}):
            user_list.append(elem['FromUserName'])
        user_list = list(set(user_list))
        print len(user_list)
        
        count = 0
        time_all=[]
        for elem in user_list:
            user_all=[]
            curt = self.db.find({'$and':[{'FromUserName':elem},{ 'Event': { '$in': ['subscribe', 'unsubscribe']}}]})
            cur = self.db.find({'$and':[{'FromUserName':elem},{ 'Event': 'subscribe'}]}).count()
            if cur>=2:
                for item in curt:
                    user_all.append({item['Event']:item['CreateTime']})
                    time_all.append(user_all)
        print len(time_all)
        
        time_block=[]
        
        #获取复活期时间
        for elem in time_all:
            pivot = 0
            time_user = []
            for item in elem:
                if item.keys()[0]=='subscribe':
                    if pivot==0:
                        pass
                    else:
                        time_user.append(int(item.values()[0])-int(pivot))
                        pivot=0
                else:
                    if pivot==0:
                        pivot=item.values()[0]
                    else:
                        pass
            try:
                time_block.append(min(time_user))
            except:
                pass
        
        time_b=time_block
        time_block=[]
        for elem in time_b:
            if elem > 0:
                time_block.append(elem/86400)
        #统计每个时间点复活的人数
        e=list(set(time_block))
        e=sorted(e)
        f=[]
        for elem in e:
            f.append(time_block.count(elem))
        
        
        #计算全部
        g=[]
        sum=0
        for elem in f:
            sum=sum+elem
            g.append(sum)
        
        #绘图
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax.plot(e,g)
        ax.set_xlabel('day')
        ax.set_ylabel('people')
        #ax.set_xlm(1,2)
        #ax.set_ylim(1,2)
        fig.savefig('survival')

if __name__ == '__main__':
    survival(hyd_events)