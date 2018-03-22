from ev3dev.ev3 import *
import time
import _thread as th

#mot init
brickMotor = MediumMotor("outD")
mot1 = LargeMotor("outC")
mot2 = LargeMotor("outB")
