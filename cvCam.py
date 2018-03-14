import cv2
import time

class CvCam(object):
	
	def __init__(self, iCam=0):
		self.cap = cv2.VideoCapture(iCam)
		self.frame = None
		self.running = True
	
	def poll(self):
		ret, self.frame = self.cap.read()

	def update(self):
		while(self.running):
			self.poll()
		
	def run_threaded(self):
		return self.frame
		
	def run(self):
		return self.frame

	def shutdown(self):
		self.running = False
		time.sleep(0.2)
		self.cap.release()

class CvImageDisplay(object):
	
	def run(self, image):
		cv2.imshow('frame', image)
		cv2.waitkey(1)
	
	def shutdown(self):
		cv2.destroyAllWindows()
	
