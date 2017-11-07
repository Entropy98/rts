import pygame,sys
from pygame.locals import *
import rts_images

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=400
		self.units=[]
		self.drones=pygame.sprite.Group()

	def select(self,item):
		item['selected']=True

	def clearSelected(self):
		for unit in self.units:
			unit['selected']=False

	def addUnit(self,unit):
		self.units.append(unit)

	def createDrone(self,x,y):
		# hitBoxX=25
		# hitBoxY=25
		# speed=10
		# drone={
		# 'hitBoxX':hitBoxX,
		# 'hitBoxY':hitBoxY,
		# 'x':x,
		# 'y':y,
		# 'speed':speed,
		# 'selected':False,
		# 'destX':None,
		# 'destY':None
		# }
		# self.addUnit(drone)
		drone=rts_images.Drone(x,y)
		self.drones.add(drone)

player1=Player('Player 1')