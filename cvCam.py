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
class CvCam(object):

	def __init__(self, camera):
		resolution = cfg.CAMERA_RESOLUTION
		resolution = (resolution[1], resolution[0])
		self.camera = camera
		self.camera.resolution = resolution
		self.camera.framerate = cfg.CAMERA_FRAMERATE
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

		self.frame = None
		self.on = True

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)


    def run(self):
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()


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
