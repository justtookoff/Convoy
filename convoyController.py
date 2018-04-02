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
            if w > 150:
                if h > 75:
                    print('found the guiding car')
                    direction = None
                    halfWidth = self.width/2
                    #Calculate the distance between the object and the middle-line
                    distanceX = halfWidth - (x+w/2)
                    #Calculate the distance
                    self.distance = self.calDistance(y, h)

                    #Move the car by pulsing the PWM
                    self.direction = self.calDirection(distanceX) #Know the diretion
                    self.angle = self.calAngle(self.distance, distanceX) #Know the angle
                    self.PWM_Steering = self.calSteering(self.direction, self.angle)

                    self.PWM_Throttle = self.calThrottle(self.distance)
                    print('PWM_Throttle:', self.PWM_Throttle)
                    print('PWM_Steering:', self.PWM_Steering)

                    return self.PWM_Steering, self.PWM_Throttle
                else:
                    return None
            else:
                return None

    #Calculate the STEERING
    def calSteering(self, direction, angle):
        #Turn right
        if direction == 1 and angle > 25:
            return 465
        #Turn left
        elif direction == -1 and angle > 25:
            return 355
        #straight
        else:
            return cfg.STEERING_STRAIGTH

    #Calculate the THROTTLE
    def calThrottle(self, dist):
        #Speed two up
        if dist < cfg.OBJECT_NEED_SPEED_ONE and dist > 0:
            return 480
        #Speed one up
        elif dist <= cfg.OBJECT_NEED_SPEED_ONE and dist > cfg.OBJECT_NEED_SPEED_ZERO:
            return 460
        #Gradually slow the car
        elif dist <= cfg.OBJECT_NEED_SPEED_ZERO and dist > cfg.OBJECT_MIN_DIST:
            return 430
        #Stop the car
        else:
            return 400


    #Caculate the Direction
    def calDirection(self, distanceX):
        '''
        direction = 1 means right
        direction = 0 means straight
        direction = -1 means left
        '''
        if distanceX < 0:
            direction = 1
        elif distanceX == 0:
            direction = 0
        else:
            direction = -1
        return direction

    #Calculate the Angle
    #return Angle (in degree)
    def calAngle(self, dist, distanceX):
        distanceX = abs(distanceX)
        x = math.tan(distanceX/dist)
        rad = math.atan(x)
        return math.degrees(rad)

    #Calculate the distance between the two of the cars
    def calDistance(self, y, h):
        return self.height - ((y+h)/2)

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
    def __init__(self, steering_controller):
        self.running = True
        self.steering_controller = steering_controller

    def run(self, PWM_Steering):
        if PWM_Steering != None:
            print('sending steering:', PWM_Steering)
            self.steering_controller.set_pulse(int(PWM_Steering))
        else:
            print('PWM_Steering is None')

    def shutdown(self):
        self.running=False
        self.steering_controller.set_pulse(int(cfg.STEERING_STRAIGTH))
'''
    This class is for manipulating Throttle
    input: PWM_Throttle
    result: Manipulate the Throttle(Pulse the ESC)
'''
class ThrottlePWMSender(object):
    def __init__(self, throttle_controller):
        self.running = True
        self.throttle_controller = throttle_controller

    def run(self, PWM_Throttle):
        if PWM_Throttle != None:
            print('sending throttle:', PWM_Throttle)
            self.throttle_controller.set_pulse(int(PWM_Throttle))
        else:
            print('PWM_Throttle is stopped')
            self.throttle_controller.set_pulse(int(cfg.THROTTLE_STOPPED_PWM))

    def shutdown(self):
        self.running=False
        self.throttle_controller.set_pulse(int(cfg.THROTTLE_STOPPED_PWM))
