import pygame,sys
from pygame.locals import *
import rts_images
import rts_helpers

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=400
		self.units=pygame.sprite.Group()
		self.selected=pygame.sprite.Group()
		self.menuState=None

	def selectUnit(self,data,unit):
		if(self.menuState==None):
			self.menuState=unit.name
			rts_helpers.updateMenuIcons(data)
		if(len(self.selected)<=40):
			self.selected.add(unit)

	def clearSelected(self):
		self.menuState=None
		self.selected.empty()

	def createDrone(self,x,y):
		drone=rts_images.Drone(x,y)
		self.units.add(drone)

player1=Player('Player 1')