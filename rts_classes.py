import pygame,sys
from pygame.locals import *
import rts_images
import rts_helpers

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=300
		self.metals=200
		self.units=pygame.sprite.Group()
		self.selected=pygame.sprite.Group()
		self.buildings=pygame.sprite.Group()
		self.inConstruction=pygame.sprite.Group()
		self.commandCenters=pygame.sprite.Group()
		self.menuState=None
		self.menuHover=None

	def select(self,data,item):
		if(self.menuState==None):
			self.menuState=item.name
			rts_helpers.updateMenuIcons(data)
		if(len(self.selected)<=40):
			self.selected.add(item)

	def clearSelected(self):
		self.menuState=None
		self.selected.empty()

	def createDrone(self,x,y,rallyX,rallyY):
		drone=rts_images.Drone(x,y,rallyX,rallyY)
		self.units.add(drone)

player1=Player('Player 1')