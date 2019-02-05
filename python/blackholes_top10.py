from bigfile import File, Dataset

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

name = 'blackholes'

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

def generate_frame (fn):
    print('\nStart bulding frame <-----------==== < ' +name+ ' > '+fn)
    bf1 = File("output/PART_"+fn+"/5")
    print('Reading data from PART_'+fn)
    tmpdata1 = Dataset(bf1, ['Position', 'Mass'])
    data11 = np.array(list((e[0]) for e in tmpdata1))
    data12 = np.array(list((e[1]) for e in tmpdata1))
    print(data11)
    bf2 = File("output/PIG_"+fn+"/5")
    print('Reading data from PIG_'+fn)
    data2 = Dataset(bf2, ['Position'])

    ax.clear()
    ax.set_title('Black Holes, Mpcs')
    ax.set_xlim(0,20);
    ax.set_ylim(0,20);
    ax.set_zlim(0,20);

    print('Finding Top 10 by Mass...')
    if (data12.size):
        ind = data12.argmax()
        ax.scatter(data11[ind][0]/1000, data11[ind][1]/1000, data11[ind][2]/1000, 'z', s=30, c='red', marker="*") 
        data11 = np.delete(data11, ind, axis=0)
        data12 = np.delete(data12, ind)
    
    for i in range(9):
        if (not data12.size): break
        ind = data12.argmax()
        ax.scatter(data11[ind][0]/1000, data11[ind][1]/1000, data11[ind][2]/1000, 'z', s=10, c='green', marker="D") 
        data11 = np.delete(data11, ind, axis=0)
        data12 = np.delete(data12, ind)

    print('Generating dots...')
    for i in range(data12.size):
        ax.scatter(data11[i][0]/1000, data11[i][1]/1000, data11[i][2]/1000, 'z', s=1, c=cm.viridis(data12[i]), marker='.') 

    print('Generating lines...')
    for a in data2:
        ax.plot([a[0][0]/1000, a[0][0]/1000], [a[0][1]/1000, a[0][1]/1000], zs=[a[0][2]/1000, 0], linewidth=1, color = 'gray', linestyle = 'dotted') 
    
    print('Saving frame: '+fn+'.png')
    fig.savefig(name+'/'+fn+'.png', format = 'png', dpi=250)
    print('Frame '+fn+' finished.')
    o = open(name+'/png.idx','a')
    o.write(fn+"\n")
    o.close

if not os.path.isdir(name):
    os.mkdir(name)
last = '0'
if os.path.isfile(name+'/png.idx'):
    f = open(name+'/png.idx','r')
    for line in f:
        last = line
else:
    f = open(name+'/png.idx','w')

f.close

f = open ('output/Snapshots.txt','r')
for line in f:
    tmp = line.split(' ', 1)
    if int(tmp[0]) >= int(last):
        generate_frame(tmp[0])

f.close

print(name)
