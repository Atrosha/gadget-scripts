from bigfile import File, Dataset

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import matplotlib.pyplot as plt
from matplotlib import cm
import os

name = 'blackholes'

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

def generate_frame (fn):
    print('\nStart bulding frame <-----------==== '+fn)
    bf1 = File("output/PART_"+fn+"/5")
    print('Reading data from PART_'+fn)
    data1 = Dataset(bf1, ['Position','Mass'])
    bf2 = File("output/PIG_"+fn+"/5")
    print('Reading data from PIG_'+fn)
    data2 = Dataset(bf2, ['Position'])

    ax.clear()
    ax.set_title('Black Holes, Mpcs')
    ax.set_xlim(0,20);
    ax.set_ylim(0,20);
    ax.set_zlim(0,20);
    print('Generating dots...')
    for a in data1:
        ax.scatter(a[0][0]/1000, a[0][1]/1000, a[0][2]/1000, 'z', 1, cm.viridis(a[1])) 
    print('Generating lines...')
    for b in data2:
        ax.plot([b[0][0]/1000, b[0][0]/1000], [b[0][1]/1000, b[0][1]/1000], zs=[b[0][2]/1000, 0], linewidth=1, color = 'gray', linestyle = 'dotted') 
    
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
