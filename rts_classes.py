import pygame,sys
from pygame.locals import *
import rts_images
import rts_helpers
import rts_units
import random

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
		self.IDs=set()
		self.winCondition='play'

	def select(self,data,item):
		if(item.ID in self.IDs):
			if(self.menuState==None):
				self.menuState=item.name
				rts_helpers.updateMenuIcons(data)
			if(len(self.selected)<=40):
				self.selected.add(item)

	def clearSelected(self):
		self.menuState=None
		self.selected.empty()

	def createDrone(self,data,x,y,rallyX,rallyY,client=False,ID=None):
		drone=rts_units.Drone(x,y,rallyX,rallyY,self.team)
		if(ID==None):
			drone.ID=random.randint(1000000,9999999)
			self.IDs.add(drone.ID)
		else:
			drone.ID=ID
		self.units.add(drone)
		if(data.startMenuState!='Singleplayer' and client==False):
			coord=rts_helpers.pos2Coord(data,x,y)
			rallyCoord=rts_helpers.pos2Coord(data,rallyX,rallyY)
			msg='createDrone %d %d %d %d %d \n'%(coord[0],coord[1],rallyCoord[0],rallyCoord[1],drone.ID)
			data.server.send(msg.encode())

	def createMilitia(self,data,x,y,rallyX,rallyY,client=False,ID=None):
		militia=rts_units.Militia(x,y,rallyX,rallyY,self.team)
		if(ID==None):
			militia.ID=random.randint(1000000,9999999)
			self.IDs.add(militia.ID)
		else:
			militia.ID=ID
		militia.rect.center=(militia.rect.center[0],militia.rect.center[1]+militia.rect.height//2)
		self.units.add(militia)
		if(data.startMenuState!='Singleplayer' and client==False):
			coord=rts_helpers.pos2Coord(data,x,y)
			rallyCoord=rts_helpers.pos2Coord(data,rallyX,rallyY)
			msg='createMilitia %d %d %d %d %d \n'%(coord[0],coord[1],rallyCoord[0],rallyCoord[1],militia.ID)
			data.server.send(msg.encode())