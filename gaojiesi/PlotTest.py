#import numpy as np
#import matplotlib.pyplot as plt

#x = np.linspace(0,10,1000)
#y = np.sin(x)
#z = np.cos(x**2)

#plt.figure(figsize=(8,4))
#plt.plot(x,y,label = '$sin(x)$',color = 'red',linewidth = 2)
#plt.plot(x,z,'b--',label = '$cos(x^2)$')

#plt.xlabel('Time(s)')
#plt.ylabel('Volt')
#plt.title('PyPlot example')
#plt.ylim(-1.2,1.2)
#plt.legend()

#plt.show()


#from pymongo import MongoClient
#from pandas import Series, DataFrame
#from lifelines import KaplanMeierFitter
#import pandas as pd
#from matplotlib import rcParams

#client = MongoClient('localhost', 27017)
#user_clear = client['gaojiesi']['user_clear']
#rcParams['figure.dpi'] = 200
#rcParams['figure.figsize'] = (96, 64)

#duration = []
#observed = []
#for elem in user_clear.find():
    #if elem['duration'] <=864000:
        #duration.append(elem['duration'])
        #observed.append(elem['observed'])
#dura_obj = Series(duration)
#obs_obj = Series(observed)
#kmf = KaplanMeierFitter()
#kmf.fit(dura_obj, event_observed=obs_obj)
#kmf.plot()


#from mpl_toolkits.mplot3d import Axes3D
#import numpy as np
#import matplotlib.pyplot as plt

#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.scatter()


import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['savefig.dpi'] = 160
rcParams['figure.figsize'] = (16, 12)

#def randrange(n, vmin, vmax):
    #return (vmax-vmin)*np.random.rand(n) + vmin

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#n = 100
#for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    #xs = randrange(n, 23, 32)
    #ys = randrange(n, 0, 100)
    #zs = randrange(n, zl, zh)
    #ax.scatter(xs, ys, zs, c=c, marker=m)

#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')

#plt.show()
from config.db import user_clear
from numpy import array
x = []
y = []
z = []
for elem in user_clear.find():
    x.append(elem['text'])
    y.append(elem['pic'])
    z.append(elem['event'])
print len(x)
xl = array(x)
yl = array(y)
zl = array(z)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('text Label')
ax.set_ylabel('pic Label')
ax.set_zlabel('event Label')
ax.legend()
ax.set_xlim3d(0, 12)
ax.set_ylim3d(0, 10)
ax.set_zlim3d(0, 40)
ax.scatter(xl, yl, zl, marker='o')
ax.get_figure().savefig('3d')