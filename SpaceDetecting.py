import numpy as np
import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import argparse
import csv
import re
import json
import scipy.stats


parser=argparse.ArgumentParser(description='Process the image frame in training or detecting mode')
parser.add_argument('-i', nargs='?', default='Topology_knowledge.csv', help='Topology training data')
#parser.add_argument('--detect', nargs='+', help='Detecting mode')
args=parser.parse_args()

#camera = PiCamera()
#camera.resolution = (1024,768)
#rawCapture = PiRGBArray(camera)

#camera.capture(rawCapture, format="bgr")
#img = rawCapture.array

img_path='output9.jpg'
img=cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

Topology_knowledge=[]
f = open(args.i,'r')
minimal_stddev=1000
for line in f:
	values = re.split(',|:|\(',line)
	if minimal_stddev>float(values[9]):
		minimal_stddev=float(values[9])
	#print len(values)
	Topology_knowledge.append([int(values[1]),int(values[3]),int(values[5]),float(values[7]),float(values[9])])
	#Topology_knowledge.append([int(values[1]),int(values[3]),int(values[5])])
f.close()

for (x,y,h,Gray_mean,Gray_apporAveStdDev) in Topology_knowledge:
	gray_crop=gray[y:y+h, x:x+h]
	result=str(cv2.meanStdDev(gray_crop))
	result=re.split('\(|,|\)|\]|\[| ',result)
	occupied=1
	if float(result[14])<minimal_stddev:
		F=float(result[14])/Gray_apporAveStdDev
		df1=x*y
		df2=x*y
		if scipy.stats.f.cdf(F,df1,df2)<0.05:
			occupied=0
			cv2.rectangle(img,(x,y),(x+h,y+h),(0,255,0),2)
			print float(scipy.stats.f.cdf(F,df1,df2))
	else:
		cv2.rectangle(img,(x,y),(x+h,y+h),(0,0,255),2)

	print json.dumps({"x":x,"y":y,"h":h,"PreLearned_Gray_mean":Gray_mean,"PreLearned_Gray_StdDev":Gray_apporAveStdDev,"Observed_Gray_mean":float(result[5]),"Observed_Gray_StdDev":float(result[14]),"Occupied":occupied})
	#print result
	#print "x:%d," %x ,
	#print "y:%d," %y ,
	#print "h:%d," %h ,
        #print "PreLearned_Gray:%s," %RGB ,
	#print "Observed_Gray:%s\n" %result[1] 

number=100
output='output_live'+str(number)+'.jpg'	
cv2.imwrite(output,img)



