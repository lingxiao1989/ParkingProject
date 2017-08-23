import numpy as np
import cv2

#car_cascade1=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cars.xml')
#car_cascade2=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cars3.xml')
#car_cascade3=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/hogcascade_cars_sideview.xml')
#car_cascade4=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/lbpcascade_cars_frontbackview.xml')
car_cascade5=cv2.CascadeClassifier('/home/pi/Workspace/ParkMe/HaarCarsXML/cascade.xml')

img_empty=cv2.imread('/home/pi/Workspace/ParkMe/HaarCarsXML/parking-no-car.png')
img_parked=cv2.imread('/home/pi/Workspace/ParkMe/HaarCarsXML/parking-car.png')
#img2=cv2.imread('/home/pi/Workspace/ParkMe/HaarCarsXML/20140620-1819_02.jpg')
#img=cv2.imread('/home/pi/Workspace/ParkMe/HaarCarsXML/parking_etiquette.jpg')

#gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray_parked = cv2.cvtColor(img_parked, cv2.COLOR_BGR2GRAY)
gray_empty = cv2.cvtColor(img_empty, cv2.COLOR_BGR2GRAY)



cars = car_cascade5.detectMultiScale(gray_parked, 1.3, 5)
roi=[]
for (x,y,w,h) in cars:
	#cv2.rectangle(img_parked,(x,y),(x+w,y+h),(255,0,0),2)
	if h>150:
		roi.append([x,y,w,h])
        	cv2.rectangle(img_parked,(x,y),(x+w,y+h),(255,0,0),2)
		#output='/home/pi/Workspace/ParkMe/HaarCarsXML/test_gray_'+str(h)+'.jpg'
		#print (y,y+h,x,x+w)
		#test_gray=gray[y:y+h, x:x+w]
        	#test_color=img[y:y+h, x:x+w]
		#cv2.imwrite(output,test_gray)
        	#cv2.imwrite('/home/pi/Workspace/ParkMe/HaarCarsXML/test_color.jpg',test_color)        
	#roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
	#print (y,y+h,x,x+w)
	#test_gray=gray[11:45, 425:459]
	#test_color=img[11:45, 425:459]

#print(roi)
for (x,y,w,h) in roi:
	gray_parked_crop=gray_parked[y:y+h, x:x+w]
	gray_empty_crop=gray_empty[y:y+h, x:x+w]
	#gray_crop_subtract=gray_parked_crop-gray_empty_crop
	print "h=%d :" %h ,
	print cv2.mean(gray_parked_crop)
	print cv2.mean(gray_empty_crop)
	#print cv2.mean(gray_crop_subtract)
	output='/home/pi/Workspace/ParkMe/HaarCarsXML/detection_result5_step3_'+str(h)+'.jpg'
	cv2.imwrite(output,gray_empty_crop)

cv2.imwrite('/home/pi/Workspace/ParkMe/HaarCarsXML/detection_result5_step2.jpg',img_parked)



