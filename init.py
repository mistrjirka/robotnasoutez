from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
import time
import _thread as th

def motorControl (mot1, mot2, command = None):
	if command != None:
		if command["type"] == "go":
			mot1.run_to_rel_pos(position_sp=command["par"], speed_sp=900, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"], speed_sp=900, stop_action="hold") 
			if(command["par"] <= 0 ):
				time.sleep(command["par"]*-1/900)
			else:
				time.sleep(command["par"]/900)
			#if command["par"] >= -400 and command["par"] <= 400:
			#	time.sleep(0.5)
			#else:
			#	time.sleep(5)
		if command["type"] == "turn":
			mot1.run_to_rel_pos(position_sp=command["par"][0], speed_sp=900, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"][1], speed_sp=900, stop_action="hold")
			#if command["par"][0] >= -400 and command["par"][0] <= 400 and command["par"][1] >= -400 and command["par"][1] <= 400:
			#	time.sleep(0.5)
			#else:
			#	time.sleep(1)
			temp1 = command["par"][0]
			temp2 = command["par"][1]
			if (command["par"][0] < 0):
				temp1 = temp1 * -1
			if (command["par"][1] < 0):
				temp2 = temp2 * -1

			if temp1 >= temp2:
				time.sleep(temp1/900)
			else:
				time.sleep(temp2/900)
class robot:
	def __init__(self, speed = 500, turnLMP = [300, -300], turnRMP = [-300, 300]):
		self.commands = [{"direction":"right", "toDo": turnRMP, "type": "turn"},{"direction":"left", "toDo": turnLMP, "type": "turn"},{"direction":"backwards", "toDo": speed * -1, "type":"go"} ,{"direction":"forwards", "toDo": speed, "type": "go"}]
	
	def do(self, whatToDo, mot1, mot2):
		for i in self.commands:
			print (i)
			if i["direction"] == whatToDo:
				motorControl(mot1,mot2, {"type": i["type"],"par":i["toDo"]})
				
rob = robot()

brickMotor = MM("outD")
mot1 = LM("outC")
mot2 = LM("outB")
#~ await mot1.run_to_rel_pos(position_sp=command["par"][0], speed_sp=900, stop_action="hold")
rob.do("right", mot1, mot2)
cs = CS()
while True:
	color = cs.color
	print (cs.color)
	if cs.color != 0 and cs.color != 1:
		print("color is not black or none")
