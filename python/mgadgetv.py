from bigfile import File, Dataset

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib
from matplotlib.animation import FFMpegWriter
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# plt.rcParams['animation.ffmpeg_path'] = '/opt/local/bin/ffmpeg'

writer = FFMpegWriter(fps=30)
plt.title('Black Holes, Mpcs')
fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

def generate_frame (fn):
    bf1 = File("output/PART_"+fn+"/5")
    print('Reading data from PART_'+fn)
    data1 = Dataset(bf1, ['Position','Mass'])
    bf2 = File("output/PIG_"+fn+"/5")
    print('Reading data from PIG_'+fn)
    data2 = Dataset(bf2, ['Position'])
    print('Generating lines for_'+fn)
    for b in data2:
       ax.plot([b[0][0]/1000, b[0][0]/1000], [b[0][1]/1000, b[0][1]/1000], zs=[b[0][2]/1000, 0], linewidth=1, color = 'gray', linestyle = 'dotted')
    print('Generating dots for_'+fn)
    for a in data1:
       ax.scatter(a[0][0]/1000, a[0][1]/1000, a[0][2]/1000, 'z', 1, cm.viridis(a[1]))
    print('Frame '+fn+' generated.')

f = open ('output/Snapshots.txt','r')

for line in f:
    tmp = line.split(' ', 1)
    with writer.saving(fig, "writer_test.mp4", 100):
         generate_frame(tmp[0])
         writer.grab_frame()

f.close

plt.show()
