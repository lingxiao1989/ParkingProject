import numpy as np
import cv2
import sys
import argparse

parser=argparse.ArgumentParser(description='Process the image frame in training or detecting mode')
parser.add_argument('--train', nargs='+', help='Training mode')
parser.add_argument('--detect', nargs='+', help='Detecting mode')
args=parser.parse_args()

if args.train is not None:
	img_path=' '.join(args.train)
	car_cascade5=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cascade.xml')
	img=cv2.imread(img_path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	cars = car_cascade5.detectMultiScale(gray, 1.3, 5)
	roi=[]
	for (x,y,w,h) in cars:
		if h>150 and h<200:
			roi.append([x,y,w,h])
			#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	for (x,y,w,h) in roi:
		gray_crop=gray[y:y+h, x:x+w]
		print "h=%d :" %h ,
		print cv2.mean(gray_crop)
		#output='/home/pi/Workspace/ParkMe/HaarCarsXML/detection_result5_step3_'+str(h)+'.jpg'
		#cv2.imwrite(output,gray_crop)

#cv2.imwrite('/home/pi/Workspace/ParkMe/HaarCarsXML/output.jpg',img)



