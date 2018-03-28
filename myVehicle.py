#import parts
from donkeycar.vehicle import Vehicle
from donkeycar.parts.actuator import PCA9685 #PWM motor controller
#from donkeycar.parts.camera import PiCamera, Webcam #Webcam is for testing
from picamera.array import PiRGBArray
from picamera import PiCamera
#import sys
#sys.path.append('/usr/local/lib/python3.5/dist-packages/')
#import pygame
#import pygame.camera

#import essential functions from cvCam
import time
import cfg
import cvCam
import convoyController

#Make new Vehicle
V = Vehicle()

#Make PiCamera Available

#cam = PiCamera(resolution=cfg.CAMERA_RESOLUTION) #This is for actutal car
#cam = Webcam(resolution=cfg.CAMERA_RESOLUTION) #This is for testing
camera = PiCamera()
print('Made a new PiCamera')

#Keep Getting the Images through PiCamera and returning frames
cam = cvCam.CvCam(camera)
V.add(cam, outputs=["camera/image"], threaded = True)
print('Added Camera')

#Make Display Available and Add to the Car
filertedDisp = cvCam.CvImageFilter()
V.add(filertedDisp, inputs = ["camera/image"],
    outputs=["x", "y", "w", "h", "center"], threaded = False)
print('Added Filted Images')

#Make Controller available and Calculate
convoyController = convoyController.Controller()
V.add(convoyController, inputs = ["x", "y", "w", "h", "center"],
        outputs = ["PWM_Steering, PWM_Throttle"], threaded = False)
print('Added convoyController')

#Make Steering and Throttle
#Make the car move
steering_controller = PCA9685(cfg.STEERING_CHANNEL)
throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL)

SteeringPWMSender= convoyController.SteeringPWMSender(steering_controller)
ThrottlePWMSender= convoyController.ThrottlePWMSender(throttle_controller)
V.add(SteeringPWMSender,inputs=["PWM_Steering"],threaded=False)
V.add(ThrottlePWMSender,inputs=["PWM_Throttle"],threaded=False)
print('Added PWMSending Parts')

V.start()
