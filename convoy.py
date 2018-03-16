#!/usr/bin/env python3

from collections import deque
import numpy as np
import cv2
#import imutils
import argparse


def main():
	cap = cv2.VideoCapture(0)
	
	# To save Video	
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	#out1 = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640, 480))
	out2 = cv2.VideoWriter('output2.avi', fourcc, 20.0, (640, 480))

	while True:
    	# Capture frame-by-frame
		ret, frame = cap.read()
		
		if ret == True:
			#frame = cv2.flip(frame,1)
	
	    	# converts images from BGR to HSV
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
			# define range of red color in HSV
			lower_red = np.array([0, 80, 0])
			upper_red = np.array([15, 255, 255])
		
    		# Threshold the HSV image to get only red colors
			mask = cv2.inRange(hsv, lower_red, upper_red)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			
			#mask = cv2.flip(mask,1)
			# Bitwise-AND mask and original image
			#res = cv2.bitwise_and(frame,frame, mask= mask)
		
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None
		
			if len(cnts) > 0:
				c = max(cnts, key=cv2.contourArea)
				(x,y,w,h) = cv2.boundingRect(c)
				center = (x+w/2, y+h/2)

				if w > 10 and h> 10:
					#	print(x-225)
					cv2.rectangle(frame, (int(x), int(y)), (x+w, y+h), (0,255, 0), 2)
					cv2.line(frame, (600/2, 0), (600/2, 480), (0, 255, 0), 2)

					#cv2.circle(frame, center, 1, (0,0, 255), -1)
					cv2.line(frame, center, (600/2, y+h/2), (0,255,0), 2)
					
					cv2.rectangle(mask, (int(x), int(y)), (x+w, y+h), (0, 255, 0), 2)
					cv2.line(mask, (600/2, 0), (600/2, 480), (0, 255, 0), 2)
					
					cv2.line(mask, center, (600/2, y+h/2), (0,255, 0), 2)
		
			#out1.write(frame)
			out2.write(mask)

			cv2.imshow('frame',frame)
			cv2.imshow('mask',mask)
			#cv2.imshow('res',res)

			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break

		else:
			break
	# When everything done, release the capture
	cap.release()
	#out1.release()
	out2.release()
	cv2.destroyAllWindows()

if __name__=='__main__':
	main()
