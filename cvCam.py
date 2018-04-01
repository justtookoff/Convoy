import cv2
import time
import cfg
from picamera.array import PiRGBArray
from picamera import PiCamera

'''
	This CvCam is for getting the images through CAMERA
	Input: PiCamera
	Return: Frame
'''
class CvCamCamera(object):

    def __init__(self, camera, rawCapture):
        self.camera = camera
        self.rawCapture = rawCapture
        self.frame = None
        self.running = True
        camera.start_recording('foo.h264')
    
    def run(self):
        if self.running == True:
            self.rawCapture = PiRGBArray(self.camera, size=cfg.CAMERA_RESOLUTION)
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            self.frame=self.rawCapture.array
            return self.frame

    def shutdown(self):
        self.camera.stop_recording()
        self.running=False
        time.sleep(1.5)
        self.camera.close()
        time.sleep(1.5)

'''
	This CvImageFilter class is to filter the image out
	the actual images in order to recognize the object better

	Input: Image
	Return: x, y, w, h, center
'''
class CvImageFilter(object):
	def __init__(self):
		self.running = True

	def run(self, image):
		if self.running == True:
			if image is not None:
				# converts images from BGR to HSV
				hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	    		# Threshold the HSV image to get only red colors
				mask = cv2.inRange(hsv, cfg.LOWER_RED, cfg.UPPER_RED)
				mask = cv2.erode(mask, None, iterations=2)
				mask = cv2.dilate(mask, None, iterations=2)

				#Find Contour of the Object
				cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
					cv2.CHAIN_APPROX_SIMPLE)[-2]
				center = None

				#If found the Object with Color
				if len(cnts) > 0:
					c = max(cnts, key=cv2.contourArea)
					(x,y,w,h) = cv2.boundingRect(c)
					center = (x+w/2, y+h/2)
					return x, y, w, h, center
				else:
					return None
			else:
				return None

	def shutdown(self):
		self.running = False
