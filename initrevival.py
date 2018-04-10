from ev3dev.ev3 import LargeMotor as LM
from ev3dev.ev3 import MediumMotor as MM
from ev3dev.ev3 import ColorSensor as CS
from ev3dev.ev3 import TouchSensor as TS
from time import sleep as waitFor

class cacheManager():
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

class robot():
	__init__(self, colorS = [{"val": [3,6], "toDo": "forward"},{"val": [2], "toDo": "right"},{"val": [5], "toDo": "left"}], turnLMP = [100, -100], turnRMP = [-180, 180]):
		
cache = cacheManager()
