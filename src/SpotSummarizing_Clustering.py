import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import argparse


parser=argparse.ArgumentParser(description='Process the image frame in training or detecting mode')
parser.add_argument('--train', action='store_true', help='Training mode')
parser.add_argument('--detect', nargs='+', help='Detecting mode')
args=parser.parse_args()

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

camera.capture(rawCapture, format="bgr")
img = rawCapture.array
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if args.train:
	#img_path='/home/pi/Workspace/ParkMe/output50.jpg'
	car_cascade5=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cascade_NewTrained_ver3.xml')
	#img=cv2.imread(img_path)

	cars = car_cascade5.detectMultiScale(gray)
	roi=[]
	for (x,y,w,h) in cars:
		#if h>100 and h<200:
		roi.append([x,y,w,h])
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	for (x,y,w,h) in roi:
		gray_crop=gray[y:y+h, x:x+w]
		print "x=%d ;" %x ,
		print "y=%d ;" %y ,
		print "h=%d ;" %h ,
		print cv2.mean(gray_crop)
		#output='/home/pi/Workspace/ParkMe/HaarCarsXML/detection_result5_step3_'+str(h)+'.jpg'
		#cv2.imwrite(output,gray_crop)

if args.detect:
	gray_crop=gray[y:y+h, x:x+w]
	print cv2.mean(gray_crop)

	

cv2.imwrite('/home/pi/Workspace/ParkMe/output.jpg',img)



