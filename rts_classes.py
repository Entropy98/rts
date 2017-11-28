import pygame,sys
from pygame.locals import *
import rts_images
import rts_helpers
import rts_units

class Player(object):
	def __init__(self, username):
		self.username = username
		self.wood=1000
		self.metals=1000
		self.energy=0
		self.powerCap=0
		self.supplyCap=0
		self.supply=0
		self.units=pygame.sprite.Group()
		self.selected=pygame.sprite.Group()
		self.buildings=pygame.sprite.Group()
		self.inConstruction=pygame.sprite.Group()
		self.commandCenters=pygame.sprite.Group()
		self.menuState=None
		self.menuHover=None
		self.team='red'
		self.ID=None

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
		drone=rts_units.Drone(x,y,rallyX,rallyY,self.team)
		self.units.add(drone)

	def createMilitia(self,x,y,rallyX,rallyY):
		militia=rts_units.Militia(x,y,rallyX,rallyY,self.team)
		militia.rect.center=(militia.rect.center[0],militia.rect.center[1]+militia.rect.height//2)
		self.units.add(militia)