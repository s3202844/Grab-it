import time
import grabit

if __name__=='__main__':
    # create the robot to control
    dev = grabit.Device()
    # Use setAngle(channel, angle, speed) to control one joint you specified
    # speed=1 is the slowest, speed=5 is the fastest, default is 3.
    dev.setAngle(0, 180, speed=3)
    # Use setAngles(joints, angles, speed) to control joints.
    # The order is as you specified in parameter 'joints'.
    # The default 'joints' is [0, 1, 2, 3, 4].
    # The default 'angles' is [90,140,40,150,90].
    dev.setAngles(
        angles=[0, 120, 50, 120, 45],
        speed=1)
    dev.setAngles(
        joints=[0, 1, 2, 3, 2, 4, 2],
        angles=[90, 135, 130, 155, 50, 90, 130],
        speed=5)
    dev.setAngles()
    # you can only use setGripper(angle) to control Gripper.
    dev.setGripper(60)
    dev.setGripper()