import time
from motopi import PCA9685

if __name__=='__main__':

    pwm = PCA9685(0x41)
    pwm.setPWMFreq(50)
    pwm.setServoPulse(0, 1500)
    time.sleep(1)
    pwm.setServoPulse(1, 1500)
    time.sleep(1)
    pwm.setServoPulse(2, 1500)
    time.sleep(1)
    pwm.setServoPulse(3, 1500)
    time.sleep(1)
    pwm.setServoPulse(4, 1500)
    time.sleep(1)
    pwm.setServoPulse(5, 1600)
    time.sleep(1)