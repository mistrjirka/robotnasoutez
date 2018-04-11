from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
from ev3dev.ev3 import TouchSensor as TS
from time import sleep as waitFor

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

class Robot:
	def __init__(self, commands = [{"direction":"right", "toDo": [-100, 100]}, {"direction":"left", "toDo": [100, -100]}, {"direction":"backward", "toDo": 600 * -1}, {"direction":"forward", "toDo": 600}], colorS = [{"val": [3,6], "toDo": "forward", "degreesDelay": 100}, {"val": [2], "toDo": "right", "degreesDelay": 100}, {"val": [5], "toDo": "left", "degreesDelay": 100}], motor1 = LM("outC"), motor2 = LM("outB")):
		self.commands = commands
		self.motors = [motor1, motor2]
		self.colorSheet = colorS
		self.greenCounter = 0
		self.colorBefore = None
		self.doCache = cache.addToCache(None)
	def do(self, whatToDo, mot1, mot2):
		if whatToDo != cache.getFromCache(self.doCache):
			for i in self.commands:
				if i["direction"] == whatToDo:
					if type(i["toDo"]).__name__ is "list":
						self.motors[0].run_to_rel_pos(position_sp=i["toDo"][0], speed_sp=600, stop_action="hold")
						self.motors[1].run_to_rel_pos(position_sp=i["toDo"][1], speed_sp=600, stop_action="hold")
						cache.editCache(self.doCache, i["direction"])
					else:
						self.motors[0].run_forever(speed_sp=i["toDo"])
						self.motors[1].run_forever(speed_sp=i["toDo"])
						cache.editCache(self.doCache, i["direction"])
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
	def brickDownEvent(self, motor = MM("outD"), degrees = 180, speed = 1400, stopAction = "hold"):
		motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=stopAction)

#class init
cache = cacheManager()
robot = Robot()
