from config.db import user_clear,users
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.cluster import KMeans


rcParams['savefig.dpi'] = 160
rcParams['figure.figsize'] = (16, 12)

#event_g = []
#pic_g = []
#text_g = []
#for elem in user_clear.find():
    #event_g.append(elem['event'])
    #pic_g.append(elem['pic'])
    #text_g.append(elem['text'])
#event_max = max(event_g)
#pic_max = max(pic_g)
#text_max = max(text_g)
#print event_max
#print pic_max
#print text_max

#dot_event = matrix([event_max,0,0])
#dot_pic = matrix([0,pic_max,0])
#dot_text = matrix([0,0,text_max])

#dot_event_g = []
#dot_pic_g = []
#dot_text_g = []

#for elem in user_clear.find():
    #datamat = matrix([elem['event'],elem['pic'],elem['text']])
    #dot_event_d = sqrt(sum(power(datamat - dot_event, 2)))
    #dot_pic_d = sqrt(sum(power(datamat - dot_pic, 2)))
    #dot_text_d = sqrt(sum(power(datamat - dot_text, 2)))
    #if dot_event_d == max([dot_event_d,dot_pic_d,dot_text_d]):
        #dot_event_g.append([elem['event'],elem['pic'],elem['text']])
    #elif dot_pic_d == max([dot_event_d,dot_pic_d,dot_text_d]):
        #dot_pic_g.append([elem['event'],elem['pic'],elem['text']])
    #else :
        #dot_text_g.append([elem['event'],elem['pic'],elem['text']])

#print len(dot_event_g)
#print len(dot_pic_g)
#print len(dot_text_g)



#def plotclass(group):
    #x = []
    #y = []
    #z = []
    #for elem in group:
        #x.append(elem[0])
        #y.append(elem[1])
        #z.append(elem[2])
    #xa = array(x)
    #ya = array(y)
    #za = array(z)
    #ax.scatter(xa, ya, za, marker='o',c=random.random(100))


#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.set_xlabel('event Label')
#ax.set_ylabel('pic Label')
#ax.set_zlabel('text Label')
#ax.legend()
#ax.set_xlim3d(0, 60)
#ax.set_ylim3d(0, pic_max)
#ax.set_zlim3d(0, 15)

#plotclass(dot_event_g)
#plotclass(dot_pic_g)
#plotclass(dot_text_g)

#ax.get_figure().savefig('3dx')

data = []
for elem in users.find():
    data.append(elem['event'])
data = array(data)
est = KMeans(n_clusters=3)
est.fit(data)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('view Label')
ax.set_ylabel('click Label')
ax.set_zlabel('other Label')
ax.legend()
ax.set_xlim3d(-20, 50)
ax.set_ylim3d(15, 50)
ax.set_zlim3d(-15, 20)
ax.scatter(data[:,0],data[:,1],data[:,2])
ax.get_figure().savefig('exam')