#!/usr/bin/env python3
import time
import cfg
import math
'''
    This Controller class is for calculating the distance between the two Cars,
    and make the following-car move

    Input: x, y, w, h, center
    Output: PWM_Steering, PWM_Throttle
'''
class Controller(object):
    #Initiate the class
    def __init__(self):
        self.PWM_Steering = 0.0
        self.PWM_Throttle = 0.0

        self.running = True
        self.width = cfg.CAMERA_WIDTH
        self.height = cfg.CAMERA_HEIGHT

        self.distance = 0.0
        self.direction = 0.0
        self.angle = 0.0

    #Keep calling this function while running this class
    def run(self, x, y, w, h, center):
        if self.running == True:
            if w > 50:
                if h > 50:
                    print('found the guiding car')
                    direction = None
                    halfWidth = self.width/2
                    #Calculate the distance between the object and the middle-line
                    distanceX = halfWidth - (x+w/2)
                    #Calculate the distance
                    dist = calDistance(y, h)

                    if dist > 100:
                        #Move the car by pulsing the PWM
                        calDirection(distanceX) #Know the diretion
                        calAngle(dist, distancxX) #Know the angle


        #return self.PWM_Steering, self.PWM_Throttle

    #Caculate the Direction
    def calDirection(self, distanceX):
        '''
        direction = 1 means right
        direction = 0 means straight
        direction = -1 means left
        '''
		if(distanceX < 0):
            self.direction = 1
		elif(distanceX == 0):
            self.direction = 0
		else:
            self.direction = -1

    #Calculate the Angle
    #return Angle (in degree)
    def calAngle(self, dist, distanceX):
        distanceX = abs(distanceX)
        x = math.tan(distanceX/dist)
        rad = math.atan(x)
        self.degree = math.degrees(rad)

    #Calculate the distance between the two of the cars
    def calDistance(self, y, h):
        self.distane = self.height - ((y+h)/2)

    #Shut down the controller
    def shutdown(self):
        print('Shutting down the Controller')
        self.running = False

'''
    This class is for manipulating Steering
    input: PWM_Steering
    result: Manipulate the steering(Pulse the ESC)
'''
class SteeringPWMSender(object):

'''
    This class is for manipulating Throttle
    input: PWM_Throttle
    result: Manipulate the Throttle(Pulse the ESC)
'''
class ThrottlePWMSender(object):
