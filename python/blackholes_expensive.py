#
# animation.FuncAnimation is recursive so its code waste too much memory and 
# slow down the PC in case a big amount of data.
# Approc on 50-60 snapshots it wastes 3 GB of memory.
#


from bigfile import File, Dataset

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

f = open ('output/Snapshots.txt','r')
ln = []
fnum = 0

for line in f:
    tmp = line.split(' ', 1)
    ln.append(tmp[0])  
    fnum = fnum + 1

f.close

def generate_frame (fnu):
    fn = ln[fnu]
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
    print('Generating lines...')
    for b in data2:
        ax.plot([b[0][0]/1000, b[0][0]/1000], [b[0][1]/1000, b[0][1]/1000], zs=[b[0][2]/1000, 0], linewidth=1, color = 'gray', linestyle = 'dotted') 
    print('Generating dots...')
    for a in data1:
        ax.scatter(a[0][0]/1000, a[0][1]/1000, a[0][2]/1000, 'z', 1, cm.viridis(a[1])) 

    print('Frame '+fn+' finished.')


anim = animation.FuncAnimation(fig, generate_frame, fnum, blit=False)

print('Exporting video...');
writer = FFMpegWriter(fps=30, bitrate=8000)
anim.save("blackholes.mp4", writer=writer)

