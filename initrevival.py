from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
from ev3dev.ev3 import TouchSensor as TS
from time import sleep as sleep

class CacheManager:
	def __init__(self):
		self.keyCounter = 0
		self.cache = []
	def addToCache(self, valueToAdd):
		self.keyCounter = self.keyCounter + 1
		self.cache.append({"data": valueToAdd, "key": self.keyCounter})
		return self.keyCounter
	def getFromCache(self, key):
		for i in self.cache:
			if i["key"] == key:
				return i["data"]
		return None
	def RemoveFromCache(self, key):
		for i in self.cache:
			if i["key"] == key:
				self.cache.remove(i)
	def editCache(self, key, data):
		for i in self.cache:
			if i["key"] == key:
				self.cache[i] = {"key": i["key"], "data": data} 

def getColorFromRaw(colorsnsr, colorResponse=[4,5,6,2,3], colorSheet=[[[160,290],[126,270],[45,85]],[[123,1000],[20,43],[10,130]],[[150,1000],[230,1000],[150,1000]],[[10,60],[30,72],[10,1000]], [[10, 30],[30,1000],[13,77]]]):
	colorsnsr.mode = "RGB-RAW"
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

class Robot:
	def __init__(self, commands = [{"direction":"right", "toDo": [-166, 166], "degreesDelay": 30}, {"direction":"left", "toDo": [166, -166],"degreesDelay": 30}, {"direction":"backward", "toDo": 400 * -1, "degreesDelay": 30}, {"direction":"forward", "toDo": 400, "degreesDelay": 30}], colorS = [{"val": [3,6], "toDo": "forward"}, {"val": [2], "toDo": "right"}, {"val": [5], "toDo": "left"}], motor1 = LM("outC"), motor2 = LM("outB")):
		self.commands = commands
		self.motors = [motor1, motor2]
		self.colorSheet = colorS
		self.greenCounter = 0
		self.colorBefore = None
		self.doCache = None
	def do(self, whatToDo):
		global motorAreRunning
		if whatToDo != self.doCache or motorAreRunning == False:
			for i in self.commands:
				if i["direction"] == whatToDo:
					#~ self.motors[0].stop()
					#~ self.motors[1].stop()
					motorAreRunning = False
					self.dist = self.motors[0].position
					self.motors[1].run_forever(speed_sp=400)
					self.motors[0].run_forever(speed_sp=400)
					motorAreRunning = True
					while (self.motors[0].position - self.dist) < i["degreesDelay"]:
						print(str(self.motors[0].position) + " " + str(self.motors[0].position - self.dist))
						sleep(0.01)
					#~ self.motors[0].stop()
					#~ self.motors[1].stop()
					motorAreRunning = False
					if str(type(i["toDo"]).__name__) == "list":
						print(str(i["toDo"]) +" "+ str(type(i["toDo"]).__name__))
						self.motors[0].run_to_rel_pos(position_sp=i["toDo"][0], speed_sp=400, stop_action="hold")
						self.motors[1].run_to_rel_pos(position_sp=i["toDo"][1], speed_sp=400, stop_action="hold")
						motorAreRunning = True
						for j in i["toDo"]:
							if j > 0:
								sleep(j/300)
						self.doCache = i["direction"]
					else:
						print(str(i["toDo"]) +" "+ str(type(i["toDo"]).__name__))
						self.motors[0].run_forever(speed_sp=i["toDo"])
						self.motors[1].run_forever(speed_sp=i["toDo"])
						motorAreRunning = True
						self.doCache = i["direction"]
		else:
			print(motorAreRunning)
	def colorResponse(self, color):
		if color == 0 or color == 1:
			print ("robot is maybe not in the right place")
		else:
			for i in self.colorSheet:
				for j in i["val"]:
					if color == j:
						if color == 3 and self.colorBefore != 3:
							print(self.colorBefore, color)
							print("tohle")
							self.greenCounter = self.greenCounter + 1
							if self.greenCounter == 2:
								self.greenCounter = 0
							self.colorBefore = color
							return {"toDo": i["toDo"], "event": "brickDown"}
						if self.colorBefore != color:
							print(color)
							self.colorBefore = color
							return {"toDo": i["toDo"], "event": None}
						else:
							return {'toDo': 'forward', 'event': None}
	def brickDownEvent(self, motor = MM("outD"), degrees = 360, speed = 1400, stopAction = "hold"):
		motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=stopAction)

#motor init
mot1 = LM("outC")
mot2 = LM("outB")

#class init
cache = CacheManager()
robot = Robot(motor1=mot1, motor2=mot2)

#sensor init
cs = CS()
ts = TS()

motorAreRunning = False
#main loop
history = "stop"
def main():
	global history
	global motorAreRunning
	motorAreRunning = True
	mot1.run_forever(speed_sp = 400)
	mot2.run_forever(speed_sp = 400)
	while getColorFromRaw(cs) == 4:
		sleep(0.03)
		print ("jeste ne" + str(getColorFromRaw(cs)))
	print("uz!!!")
	
	while True:
		color = getColorFromRaw(cs)
		print(color)
		toDo = robot.colorResponse(color)
		print (history)
		if toDo is not None:
			history = "start"
			if history == "stop": 
				motorAreRunning = False
			if toDo["event"] is None:
				robot.do(toDo["toDo"])
			else:
				robot.do(toDo["toDo"])
				robot.brickDownEvent()
		else:
			if getColorFromRaw(cs) != 4:
				while getColorFromRaw(cs) == None:
					mot1.run_forever(speed_sp = 400)
					mot2.run_forever(speed_sp = 400)
					
			else:
				mot1.stop()
				mot2.stop()
		
		sleep(0.25)
#wait for signal to start
while True:
	if getColorFromRaw(cs) == 4 or ts.value() == 1:
		main()
		break
