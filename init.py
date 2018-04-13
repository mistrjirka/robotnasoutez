from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
from ev3dev.ev3 import TouchSensor as TS

import time

def getColorFromRaw(colorsnsr, colorResponse=[4,5,6,2,3], colorSheet=[[[160,250],[165,270],[50,85]],[[150,1000],[20,43],[15,30]],[[200,1000],[280,1000],[180,1000]],[[20,60],[40,72],[20,1000]], [[15, 30],[90,1000],[13,77]]]):
	
	values = [0,0,0]
	values[0] = colorsnsr.value(0)
	values[1] = colorsnsr.value(1)
	values[2] = colorsnsr.value(2)
	index = 0
	for i in colorSheet:
		print(str(index)+ " " +str(values) + str(i))
		if values[0] in range(i[0][0], i[0][1]) and values[1] in range(i[1][0], i[1][1]) and values[2] in range(i[2][0], i[2][1]):
			print("succes" + str(colorResponse[index]))
			return colorResponse[index]
		index = index + 1

def motorControl (mot1, mot2, command = None):
	if command != None:
		if command["type"] == "go":
			mot1.run_to_rel_pos(position_sp=command["par"], speed_sp=400, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"], speed_sp=400, stop_action="hold") 
			temp1 = command["par"]
			if (command["par"] < 0):
				temp1 = temp1 * -1
			time.sleep(temp1/900)
		if command["type"] == "turn":
			mot1.run_to_rel_pos(position_sp=command["par"][0], speed_sp=400, stop_action="hold")
			mot2.run_to_rel_pos(position_sp=command["par"][1], speed_sp=400, stop_action="hold")
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
	def __init__(self, colorS = [{"val": [3,6], "toDo": "forward"},{"val": [2], "toDo": "right"},{"val": [5], "toDo": "left"}], dist = 300, turnLMP = [160, -160], turnRMP = [-160, 160]):
		self.commands = [{"direction":"right", "toDo": turnRMP, "type": "turn"}, {"direction":"left", "toDo": turnLMP, "type": "turn"}, {"direction":"backward", "toDo": dist * -1, "type":"go"}, {"direction":"forward", "toDo": dist, "type": "go"}]
		self.colorSheet = colorS
		self.greenCounter = 0
		self.colorBefore = None
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
ts = TS()

#~ cs.mode='RGB-RAW'
def start():
	while True:
		if getColorFromRaw(cs) == 4 or ts.value() == 1:
			rob.do("forward", mot1, mot2)
			while True:
				print(getColorFromRaw(cs))
				color = getColorFromRaw(cs)
				toDo = rob.colorResponse(color)
				print(toDo)
				if toDo != None:
					if toDo["event"] is None:
						rob.brickDown("")
						mot1.run_to_rel_pos(position_sp=30, speed_sp=400, stop_action="hold")
						mot2.run_to_rel_pos(position_sp=30, speed_sp=400, stop_action="hold")
						rob.do(toDo["toDo"], mot1, mot2)
					elif toDo["event"] == "brickDown":
						brickMotor.run_to_rel_pos(position_sp=360, speed_sp=1400, stop_action="hold")
						mot1.run_to_rel_pos(position_sp=30, speed_sp=400, stop_action="hold")
						mot2.run_to_rel_pos(position_sp=30, speed_sp=400, stop_action="hold")
						rob.do(toDo["toDo"], mot1, mot2)
		else:
			print ("color has to be yellow")
start()
