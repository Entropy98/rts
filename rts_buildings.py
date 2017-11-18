import pygame
import time
import rts_classes
import rts_helpers
import os
import rts_images

class Building(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.x=x
		self.y=y
		self.coords=(x,y)
		self.startTime=0

		self.rallyReset=False

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

class CommandCenter(Building):
	def __init__(self,data,x,y):
		Building.__init__(self,x,y)

		self.image=pygame.image.load(os.path.join('rts_command_center_frame.png'))
		self.image=pygame.transform.scale(self.image,(125,84))
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])
		self.xTileOffset=0
		self.yTileOffset=0

		self.name='CommandCenterX'

		self.rally_pointX=self.rect.center[0]
		self.rally_pointY=self.rect.center[1]+100

		self.createStartTime=0
		self.buildQueue=[]

		self.energy=.01
		self.energyProduced=0
		self.battery=100

		self.buildTime=15
		self.woodCost=300
		self.metalCost=200

		self.layout=[
		[False,False,False,False,False],
		[False,True,True,True,False],
		[False,True,True,True,False],
		[False,True,True,True,False],
		[False,False,False,False,False]
		]

	def createDrone(self,data):
		if(self.createStartTime==0):
			self.createStartTime=time.time()
		self.createTimeLeft=time.time()-self.createStartTime
		if(rts_images.Drone.getBuildTime()-self.createTimeLeft<=0):
			costs=rts_images.Drone.getBuildCost()
			woodCost=costs['wood']
			metalCost=costs['metals']
			energyCost=costs['energy']
			if(data.localPlayer.metals>=metalCost and data.localPlayer.wood>=woodCost and data.localPlayer.energy>=energyCost):
				data.localPlayer.createDrone(self.rect.center[0],self.rect.center[1],self.rally_pointX,self.rally_pointY)
				self.buildQueue.pop(0)
				self.createStartTime=0
				data.localPlayer.metals-=metalCost
				data.localPlayer.wood-=woodCost
				data.localPlayer.energy-=energyCost

	def build(self,data):
		if(self.startTime==0):
			self.startTime=time.time()
		self.buildTimeLeft=time.time()-self.startTime
		if(self.buildTime-self.buildTimeLeft<=0):
			self.buildComplete=True
			self.name='CommandCenter'
			self.image=pygame.image.load(os.path.join('rts_command_center.png'))
			self.image=pygame.transform.scale(self.image,(125,84))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.commandCenters.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

class GeothermalGenerator(Building):
	def __init__(self,data,x,y):
		Building.__init__(self,x,y)

		self.image=pygame.image.load(os.path.join('rts_geothermal_generator_construction.png'))
		self.image=pygame.transform.scale(self.image,(25,50))
		self.rect=self.image.get_rect()
		self.xTileOffset=-.8
		self.yTileOffset=-.8
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

		self.name='GeothermalGeneratorX'

		self.buildTime=5
		self.woodCost=0
		self.metalCost=100

		self.energy=.05
		self.battery=5
		self.energyProduced=0

		self.layout=[
		[False,False,False],
		[False,True,False],
		[False,False,False]
		]

	def build(self,data):
		if(self.startTime==0):
			self.startTime=time.time()
		self.buildTimeLeft=time.time()-self.startTime
		if(self.buildTime-self.buildTimeLeft<=0):
			self.buildComplete=True
			self.name='GeothermalGenerator'
			self.image=pygame.image.load(os.path.join('rts_geothermal_generator.png'))
			self.image=pygame.transform.scale(self.image,(25,50))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.commandCenters.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

def drawBuildings(display,data):
	data.localPlayer.inConstruction.draw(display)
	data.localPlayer.buildings.draw(display)
