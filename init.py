from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
import time
def motorControl (mot1, mot2, command = None):
	if command != None:
		if command["type"] == "go":
			mot1.run_to_rel_pos(position_sp=command["par"], speed_sp=1000, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"], speed_sp=1000, stop_action="hold") 
			temp1 = command["par"]
			if (command["par"] < 0):
				temp1 = temp1 * -1
			time.sleep(temp1/900)
		if command["type"] == "turn":
			mot1.run_to_rel_pos(position_sp=command["par"][0], speed_sp=1000, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"][1], speed_sp=1000, stop_action="hold")
			if command["par"][0] >= -400 and command["par"][0] <= 400 and command["par"][1] >= -400 and command["par"][1] <= 400:
				time.sleep(0.5)
			else:
				time.sleep(1)
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
		else:
			print(command)
class robot:
	def __init__(self, colorS = [{"val": [3,6], "toDo": "forward"},{"val": [2], "toDo": "right"},{"val": [5], "toDo": "left"}], dist = 300, turnLMP = [200, -200], turnRMP = [-200, 200]):
		self.commands = [{"direction":"right", "toDo": turnRMP, "type": "turn"}, {"direction":"left", "toDo": turnLMP, "type": "turn"}, {"direction":"backward", "toDo": dist * -1, "type":"go"}, {"direction":"forward", "toDo": dist, "type": "go"}]
		self.colorSheet = colorS
		self.greenCounter = 0
		self.colorBefore = None;
	def do(self, whatToDo, mot1, mot2):
		for i in self.commands:
			
			if i["direction"] == whatToDo:
				print (i)
				motorControl(mot1,mot2, {"type": i["type"],"par":i["toDo"]})
	def colorResponse(self, color):
		
		if color == 0 or color == 1:
			print ("robot is maybe not in the right place")
		else:
			for i in self.colorSheet:
				for j in i["val"]:
					if color == j:
						if self.colorBefore != None:
							if color == 3 and self.colorBefore != 3:
								self.greenCounter = self.greenCounter + 1
								if self.greenCounter == 2:
									self.greenCounter = 0
									self.colorBefore = color
									return {"toDo": i["toDo"], "event": "brickDown"}
						if self.colorBefore != color:
							self.colorBefore = color				
							return {"toDo": i["toDo"], "event": None}
						else:
							return {'toDo': 'forward', 'event': None}
	def brickDown(self, mot):
		print("brickDown")
		
rob = robot()

brickMotor = MM("outD")
mot1 = LM("outC")
mot2 = LM("outB")
#~ rob.do("right", mot1, mot2)
#~ rob.do("left", mot1, mot2)
#~ rob.do("forward", mot1, mot2)
#~ rob.do("backward", mot1, mot2)
cs = CS()
#~ cs.mode='RGB-RAW'
def start():
	while True:
		if cs.color == 4:
			rob.do("forward", mot1, mot2)
			while True:
				print(cs.color)
				color = cs.color
				toDo = rob.colorResponse(color)
				print(toDo)
				if toDo != None:
					if toDo["event"] is None:
						rob.brickDown("")
						rob.do(toDo["toDo"], mot1, mot2)
					elif toDo["event"] == "brickDown":
						rob.do(toDo["toDo"], mot1, mot2)
		else:
			print ("color has to be yellow")
start()
