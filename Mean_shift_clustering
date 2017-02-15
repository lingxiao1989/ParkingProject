"""
=============================================
A demo of the mean-shift clustering algorithm
=============================================

Reference:

Dorin Comaniciu and Peter Meer, "Mean Shift: A robust approach toward
feature space analysis". IEEE Transactions on Pattern Analysis and
Machine Intelligence. 2002. pp. 603-619.

"""
print(__doc__)

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
import re
import cv2

###############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, _ = make_blobs(n_samples=10, centers=centers, cluster_std=0.6)
X=[]
Topology_data=[]
count=0
f = open('C:\\Users\\xiao\\Desktop\\New folder\\Topology_data.temp','r')
for line in f:
	values = re.split(',|:|\(',line)

	if int(values[5])>120 and count<150:
		Topology_data.append([int(values[1]),int(values[3]),int(values[5]),float(values[7]),float(values[9])])
		X.append([int(values[1]),int(values[3])])
	count+=1
f.close()

print count
img_path='C:\\Users\\xiao\\Desktop\\New folder\\output35.jpg'
img=cv2.imread(img_path)
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#for (x,y,h,Gray_mean,Gray_StdDev) in Topology_data:
	#if h>150 and count<200:
		#cv2.rectangle(img,(x,y),(x+h,y+h),(0,255,0),1)
		#count+=1

#cv2.imwrite('C:\\Users\\xiao\\Desktop\\New folder\\output_figure.jpg',img)



###############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
#bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)
bandwidth=120
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)



print("number of estimated clusters : %d" % n_clusters_)

###############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle
plt.figure(1)
plt.clf()


Topology_knowledge=[]
Topology_data=np.array(Topology_data)

#print Topology_data
for k in range(n_clusters_):
	my_members = labels == k
	cluster_center = cluster_centers[k]
	#print k,Topology_data[my_members,1]
	Topology_knowledge.append([int(np.mean(Topology_data[my_members,0])), int(np.mean(Topology_data[my_members,1])), int(np.mean(Topology_data[my_members,2])), np.mean(Topology_data[my_members,3]),np.min(Topology_data[my_members,4]),np.max(Topology_data[my_members,4]),np.sqrt(np.mean(np.square(Topology_data[my_members,4])))])

print Topology_knowledge

#for (x,y,h,Gray_mean) in Topology_knowledge:
	#if h>150 and count<200:
	#x=int(x)
	#y=int(y)
	#h=int(h)
	#print x,y,(x+h,y+h)
	#cv2.rectangle(img,(x,y),(x+h,y+h),(255,0,0),1)
#cv2.imwrite('C:\\Users\\xiao\\Desktop\\New folder\\output_figure.jpg',img)
#cv2.rectangle(img,(439,272),(693, 526),(255,0,0),1)
#cv2.rectangle(img,(48,221),(458, 631),(0,255,0),1)
#cv2.rectangle(img,(672,265),(887, 480),(0,0,255),1)

#cv2.imwrite('C:\\Users\\xiao\\Desktop\\New folder\\output_figure.jpg',img)

#my_members = labels == 2
#cluster_center = cluster_centers[2]
#for (x,y,h,Gray_mean,Gray_StdDev) in Topology_data[my_members]:
	#if h>150 and count<200:
	#x=int(x)
	#y=int(y)
	#h=int(h)
	#cv2.rectangle(img,(x,y),(x+h,y+h),(255,0,0),1)
#cv2.imwrite('C:\\Users\\xiao\\Desktop\\New folder\\output_figure.jpg',img)

#X=48, Y=221, H=410, Grey_mean=156.9505, Grey_maxStdDev=55.1854
#X=439, Y=272, H=254, Grey_mean=119.4492, Grey_maxStdDev=47.3753
#X=672, Y=265, H=215, Grey_mean=87.0308, Grey_maxStdDev=43.7591


colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    #print k,Topology_data[my_members]
    # plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    # plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
#plt.show()
