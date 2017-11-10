import pygame,sys
from pygame.locals import *
import rts_images

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=400
		self.units=pygame.sprite.Group()
		self.selected=pygame.sprite.Group()
		self.firstSelect=None

	def selectUnit(self,unit):
		if(self.firstSelect==None):
			self.firstSelect=unit.name
		if(len(self.selected)<=40):
			self.selected.add(unit)

	def clearSelected(self):
		self.firstSelect=None
		self.selected.empty()

	def createDrone(self,x,y):
		drone=rts_images.Drone(x,y)
		self.units.add(drone)

player1=Player('Player 1')