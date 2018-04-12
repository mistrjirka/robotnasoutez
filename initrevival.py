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

class Robot:
	def __init__(self, commands = [{"direction":"right", "toDo": [-100, 100], "degreesDelay": 100}, {"direction":"left", "toDo": [100, -100], "degreesDelay": 100}, {"direction":"backward", "toDo": 600 * -1, "degreesDelay": 100}, {"direction":"forward", "toDo": 600, "degreesDelay": 100}], colorS = [{"val": [3,6], "toDo": "forward"}, {"val": [2], "toDo": "right"}, {"val": [5], "toDo": "left"}], motor1 = LM("outC"), motor2 = LM("outB")):
		self.commands = commands
		self.motors = [motor1, motor2]
		self.colorSheet = colorS
		self.greenCounter = 0
		self.colorBefore = None
		self.doCache = cache.addToCache(None)
	def do(self, whatToDo):
		if whatToDo != self.doCache:
			for i in self.commands:
				if i["direction"] == whatToDo:
					self.motors[0].stop()
					self.motors[1].stop()
					self.dist = self.motors[0].position
					self.motors[1].run_forever(speed_sp=400)
					self.motors[0].run_forever(speed_sp=400)
					while (self.motors[0].position - self.dist) < i["degreesDelay"]:
						print(str(self.motors[0].position) + " " + str(self.motors[0].position - self.dist))
						sleep(0.02)
					self.motors[0].stop()
					self.motors[1].stop()
					if str(type(i["toDo"]).__name__) == "list":
						print(str(i["toDo"]) +" "+ str(type(i["toDo"]).__name__))
						self.motors[0].run_to_rel_pos(position_sp=i["toDo"][0], speed_sp=600, stop_action="hold")
						self.motors[1].run_to_rel_pos(position_sp=i["toDo"][1], speed_sp=600, stop_action="hold")
						self.doCache = i["direction"]
					else:
						print(str(i["toDo"]) +" "+ str(type(i["toDo"]).__name__))
						self.motors[0].run_forever(speed_sp=i["toDo"])
						self.motors[1].run_forever(speed_sp=i["toDo"])
						self.doCache = i["direction"]
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

#motor init
mot1 = LM("outC")
mot2 = LM("outB")

#class init
cache = CacheManager()
robot = Robot(motor1=mot1, motor2=mot2)

#sensor init
cs = CS()
ts = TS()

#main loop
def main():
	mot1.run_forever(speed_sp = 1400)
	mot2.run_forever(speed_sp = 1400)
	while cs.color == 4:
		sleep(0.02)
	mot1.stop()
	mot2.stop()
	while True:
		color = cs.color
		toDo = robot.colorResponse(color)
		print(toDo)
		if toDo is not None:
			print (toDo["event"])
			if toDo["event"] is None:
				robot.do(toDo["toDo"])
			else:
				robot.brickDownEvent()
				robot.do(toDo["toDo"])
			sleep(0.1)
	
#wait for signal to start
while True:
	if cs.color == 4 and ts.value() == 1:
		main()
		break
