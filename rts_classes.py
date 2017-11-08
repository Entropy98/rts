import pygame,sys
from pygame.locals import *
import rts_images

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=400
		self.units=pygame.sprite.Group()
		self.selected=pygame.sprite.Group()

	def selectUnit(self,unit):
		self.selected.add(unit)

	def clearSelected(self):
		self.selected.empty()

	def addUnit(self,unit):
		self.units.append(unit)

	def createDrone(self,x,y):
		drone=rts_images.Drone(x,y)
		self.units.add(drone)

player1=Player('Player 1')