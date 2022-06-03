import time
from motopi import PCA9685

class Device():

    def __init__(self):
        self.__motopi = PCA9685(0x41)
        self.__motopi.setPWMFreq(50)
        self.__angle_limits = [
            [0., 180.], [0., 180.], [30., 190.], [12., 193.], [0., 180.], [0., 100.]
        ]
        self.__pulse_limits = [
            [2500, 500], [2500, 500], [920, 2500], [500, 2350], [2500, 500], [1250, 1900]
        ]
        self.__SPEED = [15*i for i in range(1, 6)]

    def getAngle(self, channel):
        pulse = self.__motopi.readServoPulse(channel)
        return self.pulse2angle(channel, pulse)
    
    def setAngle(self, channel, angle, speed=3):
        N = self.__SPEED[speed-1]
        pulse = self.angle2pulse(channel, angle)
        start = self.__motopi.readServoPulse(channel)//5*5
        while start != pulse:
            if start < pulse:
                start = min(start+N, pulse)
                self.__motopi.setServoPulse(channel, start)
            else:
                start = max(start-N, pulse)
                self.__motopi.setServoPulse(channel, start)
            time.sleep(0.05)
        time.sleep(0.1)

    def setAngles(self, joints=[0,1,2,3,4], angles=[90,140,40,150,90], speed=3):
        n = len(angles)
        for i in range(n):
            if angles[i] != None:
                self.setAngle(joints[i], angles[i])
            else:
                continue
        time.sleep(0.1)

    def setGripper(self, angle=0):
        self.setAngle(5, angle, 3)
    
    def pulse2angle(self, channel, pulse):
        _diff = pulse - self.__pulse_limits[channel][0]
        _scope0 = self.__angle_limits[channel][1] - \
                  self.__angle_limits[channel][0]
        _scope1 = self.__pulse_limits[channel][1] - \
                  self.__pulse_limits[channel][0]
        return _diff/_scope1*_scope0 + self.__angle_limits[channel][0]

    def angle2pulse(self, channel, angle):
        _bottom = self.__angle_limits[channel][0]
        _up = self.__angle_limits[channel][1]
        target = min(max(float(angle), _bottom), _up)
        _diff = target - self.__angle_limits[channel][0]
        _scope0 = self.__angle_limits[channel][1] - \
                  self.__angle_limits[channel][0]
        _scope1 = self.__pulse_limits[channel][1] - \
                  self.__pulse_limits[channel][0]
        pulse = int((_diff/_scope0*_scope1 + \
                   self.__pulse_limits[channel][0])//5*5)
        return pulse
