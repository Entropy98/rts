class Player(object):
	def __init__(self, username):
		self.username = username
		self.selected=[]
		self.wood=400
		self.units=[]

	def select(self,item):
		if(item not in self.selected):
			self.selected.append(item)

	def clearSelected(self):
		self.selected=[]

	def addUnit(self,unit):
		self.units.append(unit)

	def createDrone(self,x,y):
		hitBoxX=25
		hitBoxY=25
		speed=10
		drone={
		'hitBoxX':hitBoxX,
		'hitBoxY':hitBoxY,
		'x':x,
		'y':y,
		'speed':speed
		}
		self.addUnit(drone)

player1=Player('Player 1')