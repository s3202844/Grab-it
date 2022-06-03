import time
import grabit
from tkinter import *
from motopi import PCA9685


def setPWM0(angel):
    pulse = dev.angle2pulse(0, int(angel))
    pwm_chip.setServoPulse(0, pulse)
    time.sleep(0.01)
def setPWM1(angel):
    pulse = dev.angle2pulse(1, int(angel))
    pwm_chip.setServoPulse(1, pulse)
    time.sleep(0.01)
def setPWM2(angel):
    pulse = dev.angle2pulse(2, int(angel))
    pwm_chip.setServoPulse(2, pulse)
    time.sleep(0.01)
def setPWM3(angel):
    pulse = dev.angle2pulse(3, int(angel))
    pwm_chip.setServoPulse(3, pulse)
    time.sleep(0.01)
def setPWM4(angel):
    pulse = dev.angle2pulse(4, int(angel))
    pwm_chip.setServoPulse(4, pulse)
    time.sleep(0.01)
def setPWM5(angel):
    pulse = dev.angle2pulse(5, int(angel))
    pwm_chip.setServoPulse(5, pulse)
    time.sleep(0.01)

start = [90, 160, 50, 160, 90, 60]
end = [90, 180, 35, 130, 90, 0]
pwm_chip = PCA9685(0x41)
pwm_chip.setPWMFreq(50)
dev = grabit.Device()
root = Tk(screenName=":0")
root.title("control panel")
angels = [IntVar() for _ in range(6)]
for i in range(len(start)):
    pulse = dev.angle2pulse(i, start[i])
    pwm_chip.setServoPulse(i, pulse)
    time.sleep(0.1)
    angels[i].set(start[i])
args = dict(tickinterval=60, resolution=1, orient=HORIZONTAL, length=400)
labels = [Label(root, text="J"+str(i)).grid(row=i, column=0, pady=4, padx = 4) for i in range(6)]
s0 = Scale(root, from_=0, to=180, variable=angels[0], command=setPWM0, **args)
s1 = Scale(root, from_=0, to=180, variable=angels[1], command=setPWM1, **args)
s2 = Scale(root, from_=30, to=190, variable=angels[2], command=setPWM2, **args)
s3 = Scale(root, from_=12, to=193, variable=angels[3], command=setPWM3, **args)
s4 = Scale(root, from_=0, to=180, variable=angels[4], command=setPWM4, **args)
s5 = Scale(root, from_=0, to=100, variable=angels[5], command=setPWM5, **args)
s0.grid(row=0, column=1)
s1.grid(row=1, column=1)
s2.grid(row=2, column=1)
s3.grid(row=3, column=1)
s4.grid(row=4, column=1)
s5.grid(row=5, column=1)
mainloop()
for i in range(len(end)):
    pulse = dev.angle2pulse(i, end[i])
    pwm_chip.setServoPulse(i, pulse)
    time.sleep(0.1)

