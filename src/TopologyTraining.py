import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import argparse
import re

parser=argparse.ArgumentParser(description='Process the image frame in training or detecting mode')
parser.add_argument('-c', nargs='?', default='0', help='Choose whether to clear the previous data in the file')
parser.add_argument('-o', nargs='?', default='Topology_data.temp', help='Output filename')
#parser.add_argument('--detect', nargs='+', help='Detecting mode')
args=parser.parse_args()

camera = PiCamera()
camera.resolution = (1024,768)
rawCapture = PiRGBArray(camera)

camera.capture(rawCapture, format="bgr")
img = rawCapture.array
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if args.c=='0':
	f = open(args.o,'a')
else:
	f = open(args.o,'w')

#img_path='/home/pi/Workspace/ParkMe/output31.jpg'
#img=cv2.imread(img_path)
car_cascade5=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cascade_NewTrained_ver3.xml')

cars = car_cascade5.detectMultiScale(gray)
roi=[]
for (x,y,w,h) in cars:
	#if h>100 and h<200:
	roi.append([x,y,w,h])
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


	
for (x,y,w,h) in roi:
	gray_crop=gray[y:y+h, x:x+w]
	result=str(cv2.meanStdDev(gray_crop))
	result=re.split('\(|,|\)|\]|\[| ',result)
	f.write("x:%d," %x)
	f.write("y:%d," %y)
	f.write("h:%d," %h)
	f.write("Observed_Gray_mean:%s, " %result[5])
	f.write("Observed_Gray_StdDev:%s\n" %result[14])
		#output='/home/pi/Workspace/ParkMe/HaarCarsXML/detection_result5_step3_'+str(h)+'.jpg'
		#cv2.imwrite(output,gray_crop)
f.close()
	

cv2.imwrite('/home/pi/Workspace/ParkMe/output2.jpg',img)



