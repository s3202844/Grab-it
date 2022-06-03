import sys
import time
from pick_place import MotionPlanner, MotionExecuter, CATCH, RELEASE
from cv_color import ColorDetector
import grabit

planner = MotionPlanner()
executor = MotionExecuter()
detector = ColorDetector()

def pick_place(src, dst):
    j1, j2, j3, j4 = planner.backward_kinematics( *src )
    executor.move_to([j1, j2, j3, j4], CATCH)
    # print(j1, j2, j3, j4)
    time.sleep(2)
    j1, j2, j3, j4 = planner.backward_kinematics( *dst )
    # print(j1, j2, j3, j4)
    executor.move_to([j1, j2, j3, j4], RELEASE)
    time.sleep(2)
    executor.idle()

def dancing():
    dev = grabit.Device()

    sequence = [0, 0, 2, 2, 4, 4, 5, 5]
    angle = [0, 180, 120, 140, 0, 180, 0, 100]

    dev.setAngles(
       joints = sequence,
       angles = angle,
       speed=10
    )


if __name__ == '__main__':
    while True:
        color = detector.detectColor()
        print("color:", color)
        #pick 
        if color == 1:
            pick_place([-10, 0, 0], [10, 0, 1] )
            time.sleep(1)

        #pick
        if color == 2:
            pick_place([-10, 0, 0], [5, 8, 1] )
            time.sleep(1)

        #pick
        if color == 3:
            pick_place([-10, 0, 0], [0, 15, 1] )
            time.sleep(1)

        #other
        if color == 4:
            dancing()

