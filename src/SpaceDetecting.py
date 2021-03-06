import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import argparse
import csv
import re
import json

parser=argparse.ArgumentParser(description='Process the image frame in training or detecting mode')
parser.add_argument('-i', nargs='?', default='Topology_knowledge.csv', help='Topology training data')
#parser.add_argument('--detect', nargs='+', help='Detecting mode')
args=parser.parse_args()

camera = PiCamera()
camera.resolution = (1024,768)
rawCapture = PiRGBArray(camera)

camera.capture(rawCapture, format="bgr")
img = rawCapture.array

#img_path='/home/pi/Workspace/ParkMe/output38.jpg'
#img=cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

Topology_knowledge=[]
f = open(args.i,'r')
for line in f:
	values = re.split(',|:|\(',line)
	#print len(values)
	Topology_knowledge.append([int(values[1]),int(values[3]),int(values[5]),float(values[7]),float(values[9]),float(values[11])])
	#Topology_knowledge.append([int(values[1]),int(values[3]),int(values[5])])
f.close()

for (x,y,h,Gray_mean,Gray_minStdDev,Gray_maxStdDev) in Topology_knowledge:
	gray_crop=gray[y:y+h, x:x+h]
	result=str(cv2.meanStdDev(gray_crop))
	result=re.split('\(|,|\)|\]|\[| ',result)
	if float(result[14])<30:
                occupied=0
        else:
                occupied=1
	#print result
        print json.dumps({"x":x,"y":y,"h":h,"PreLearned_Gray_mean":Gray_mean,"PreLearned_Gray_minStdDev":Gray_minStdDev,"PreLearned_Gray_maxStdDev":Gray_maxStdDev,"Observed_Gray_mean":result[5],"Observed_Gray_StdDev":result[14],"Occupied":occupied})
	#print "x:%d," %x ,
	#print "y:%d," %y ,
	#print "h:%d," %h ,
        #print "PreLearned_Gray:%s," %RGB ,
	#print "Observed_Gray:%s\n" %result[1] 

number=001
output='/home/pi/Workspace/ParkMe/output_live'+str(number)+'.jpg'	
cv2.imwrite(output,img)



