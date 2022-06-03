import math
import time
import grabit
from tkinter import *
from motopi import PCA9685
import numpy as np
import itertools

# A1, A2, A3, A4 = 9.5, 10.5, 10, 14.5
A1, A2, A3, A4 = 6.5, 10.5, 10, 14.5

MAX_LEN = A2+A3+A4
MAX_HEIGHT = A1+A2+A3+A4

J1, J2, J3, J4 = 1, 2, 3, 4
P = 7.5 

CATCH = 1
RELEASE = 2

class MotionPlanner:
    def cos(self, degree):
        return math.cos(math.radians(degree))

    def sin(self, degree):
        return math.sin(math.radians(degree))

    def arctan(self, a, b):
        return math.degrees(math.atan2(a, b))

    def convert_degree(self, joint_id, value):
        if joint_id == 1:
            return value
        else:
            return 90 - value

    def is_valid_degree(self, joint_id, degree):
        if joint_id == J1:
            return 0 <= degree <= 180
        if joint_id == J2:
            return 10 <= degree <= 80 
        if joint_id == J3:
            return 0 <= degree <= 90
        if joint_id == J4:
            return 0 <= degree <= 100

    def to_angle(self, joint_id, degree):
        if joint_id == J1:
            return degree
        if joint_id == J2:
            return 110 - degree
        if joint_id == J3:
            return 190 - degree
        if joint_id == J4:
            return 185 - degree

    def calc_j1(self, x, y, z):
        length = round(math.sqrt((y+P)**2 + x**2))
        if length == 0:
            j1 = 0
        else:
            j1 = self.arctan(y+P, x)

        height = z
        return j1, length, height

    def calc_j3(self, L, H):
        cos3 = (L**2 + H**2 - A2**2 - A3**2) / (2 * A2 * A3)

        sin3 = math.sqrt(1 - cos3 ** 2)
        j3 = self.arctan(sin3, cos3)
        return j3 

    def calc_j2(self, L, H, j3):
        k1 = A2 + A3 * self.cos(j3)
        k2 = A3 * self.sin(j3)
        w = self.arctan(k2, k1)
        j2 = self.arctan(L, H) - w
        return j2

    def calc_j4(self, j2, j3, alpha):
        j4 = alpha - j2 - j3
        return j4


    def coordinate_to_angle(self, x, y, z, alpha):
        j1, length, height = self.calc_j1(x, y, z)

        if not self.is_valid_degree(J1, j1) or length >=MAX_LEN or height >= MAX_HEIGHT:
            return False, None, None, None, None

        L = length - A4 * self.sin(alpha)
        H = height - A4 * self.cos(alpha) - A1

        cos3 = (L**2 + H**2 - A2**2 - A3**2) / (2 * A2 * A3)
        if abs(cos3) > 1:
            return False, None, None, None, None

        j3 = self.calc_j3(L, H)

        if not self.is_valid_degree(J3, j3):
            return False, None, None, None, None

        j2 = self.calc_j2(L, H, j3)

        if not self.is_valid_degree(J2, j2):
            return False, None, None, None, None

        j4 = self.calc_j4(j2, j3, alpha)
        if not self.is_valid_degree(J4, j4):
            return False, None, None, None, None

        return True, j1, j2, j3, j4


    def search(self, x, y, z, alpha = 240):
        valid, j1, j2, j3, j4 = False, -1, -1, -1, -1
        while alpha >= 90 and not valid:
            valid, j1, j2, j3, j4 = self.coordinate_to_angle(x, y, z, alpha)
            if not valid:
                alpha -= 1

        return valid, j1, j2, j3, j4

    def find_sequence(self, src, dst):
        s_joints = [ self.to_angle(i+1, src[i]) for i in range(4) ]
        d_joints = [ self.to_angle(i+1, dst[i]) for i in range(4) ]

        permutations = list(itertools.permutations(range(4)))

        def compute_z(joints):
            return A1 + A2 * self.cos(joints[1]) + A3 * self.cos(joints[1] + joints[2]) + A4 * self.cos(joints[1] + joints[2] + joints[3])

        for seq in permutations:
            s_copy = s_joints.copy()
            d_copy = d_joints.copy()
            ret = True
            for i in seq:
                s_copy[i] = d_copy[i]
                # print(compute_z(s_copy))
                if compute_z(s_copy) < -2:
                    ret = False
                    break
            
            if ret:
                return list(seq) 
        
        return [0, 1, 2, 3] 
                
    def backward_kinematics(self, x, y, z):
        valid, j1, j2, j3, j4 = self.search(x, y, z)
        if valid:
            return self.to_angle(J1, j1), self.to_angle(J2, j2), self.to_angle(J3, j3), self.to_angle(J4, j4)

class MotionExecuter:
    def __init__(self):
        # self.IDLE = [90, 180, 35, 130, 90, 60]
        self.IDLE = [90, 100, 120, 130, 90, 60]
        self.last = self.IDLE
        self.idle()

    def do(self, joints, sequence=None, time_seq=None):
        dev = grabit.Device()
        if not sequence:
            sequence = range(len(joints))

        angle = [joints[i] for i in sequence]
        
        # print(sequence, joints)

        dev.setAngles(
           joints = sequence,
           angles = angle,
           speed=5
        )


    def compute_dist(self, src, dst):
        diff = np.abs( np.array(src) - np.array(dst) )
        time_seq = (diff / 5) * 0.2
        return time_seq

    def move_to(self, joint_list, catch_or_release):
        all_joints = joint_list
        time_seq = self.compute_dist(self.last[0:4], joint_list)

        planner = MotionPlanner()

        move_seq = planner.find_sequence(self.last[0:4], joint_list)

        # print(move_seq)

        all_joints.append(90)
        if catch_or_release == CATCH:
            all_joints.append(10)
        if catch_or_release == RELEASE:
            all_joints.append(60)
        
        time_seq = np.append(time_seq, [0.2, 0.2])
        move_seq.append(4)
        move_seq.append(5)

        self.do(all_joints, sequence=move_seq, time_seq=time_seq)
   
    def idle(self):
        sequence = [1,2,3,4,5,0]
        self.do(self.IDLE, sequence = sequence)
        self.last = self.IDLE



