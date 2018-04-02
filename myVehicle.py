#import parts
from donkeycar.vehicle import Vehicle
from donkeycar.parts.actuator import PCA9685 #PWM motor controller
from picamera.array import PiRGBArray
from picamera import PiCamera

#import essential functions from cvCam
import time
import cfg
import cvCam
import convoyController

#Make new Vehicle
V = Vehicle()

#Make PiCamera Available
camera = PiCamera()
camera.resolution = cfg.CAMERA_RESOLUTION
camera.framerate = cfg.CAMERA_FRAMERATE
rawCapture = PiRGBArray(camera, size=cfg.CAMERA_RESOLUTION)
print('Made a new PiCamera')

time.sleep(.5)
print('Camera Ready')

#Keep Getting the Images through PiCamera and returning frames
cam = cvCam.CvCamCamera(camera, rawCapture)
V.add(cam, outputs=["camera/image"], threaded = False)
print('Added Camera')

#Make Display Available and Add to the Car
filertedDisp = cvCam.CvImageFilter()
V.add(filertedDisp, inputs = ["camera/image"],
    outputs=["x", "y", "w", "h", "center"], threaded = False)
print('Added Filted Images')

#Make Controller available and Calculate
controller = convoyController.Controller()
V.add(controller, inputs = ["x", "y", "w", "h", "center"],
    outputs=["PWM_Steering", "PWM_Throttle"], threaded = False)
print('Added Controller')

#Make Steering and Throttle
#Make the car move
steering_controller = PCA9685(cfg.STEERING_CHANNEL)
throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL)

SteeringPWMSender = convoyController.SteeringPWMSender(steering_controller)
ThrottlePWMSender = convoyController.ThrottlePWMSender(throttle_controller)
V.add(SteeringPWMSender, inputs = ["PWM_Steering"], threaded = False)
V.add(ThrottlePWMSender, inputs = ["PWM_Throttle"], threaded = False)
print('Added PWMSending Parts')

V.start()
