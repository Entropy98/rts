import pygame
import time
import rts_classes
import rts_helpers
import os
import rts_images
import rts_units

class Building(pygame.sprite.Sprite):
	def __init__(self,x,y,team):
		pygame.sprite.Sprite.__init__(self)
		self.x=x
		self.y=y
		self.team=team
		self.coords=(x,y)
		self.startTime=0
		self.energyProduced=0

		self.rallyReset=False

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)
		if(self.health<=0):
			self.kill()

class CommandCenter(Building):
	def __init__(self,data,x,y,team):
		Building.__init__(self,x,y,team)

		self.image=pygame.image.load(os.path.join('rts_command_center_frame.png'))
		self.image=pygame.transform.scale(self.image,(150,110))
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])
		self.xTileOffset=-1
		self.yTileOffset=-1

		self.name='CommandCenterX'

		self.prereqs=[]

		self.rally_pointX=self.rect.center[0]
		self.rally_pointY=self.rect.center[1]+100

		self.createStartTime=0
		self.buildQueue=[]

		self.energy=.01
		self.battery=100

		self.buildTime=15
		self.woodCost=300
		self.metalCost=200

		self.health=2000
		self.maxHealth=self.health

		self.layout=[
		[False,False,False,False,False,False],
		[False,True,True,True,True,False],
		[False,True,True,True,True,False],
		[False,True,True,True,True,False],
		[False,True,True,True,True,False],
		[False,False,False,False,False,False]
		]

	def createDrone(self,data):
		if(self.createStartTime==0):
			self.createStartTime=time.time()
		self.createTimeLeft=time.time()-self.createStartTime
		if(rts_units.Drone.getBuildTime()-self.createTimeLeft<=0):
			costs=rts_units.Drone.getBuildCost()
			woodCost=costs['wood']
			metalCost=costs['metals']
			energyCost=costs['energy']
			if(data.localPlayer.metals>=metalCost and data.localPlayer.wood>=woodCost and data.localPlayer.energy>=energyCost):
				data.localPlayer.createDrone(data,self.rect.center[0],self.rect.center[1],self.rally_pointX,self.rally_pointY)
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
			if(self.team=='yellow'):
				self.image=pygame.image.load(os.path.join('rts_command_center_yellow.png'))
			elif(self.team=='blue'):
				self.image=pygame.image.load(os.path.join('rts_command_center_blue.png'))
			elif(self.team=='red'):
				self.image=pygame.image.load(os.path.join('rts_command_center_red.png'))
			elif(self.team=='green'):
				self.image=pygame.image.load(os.path.join('rts_command_center_green.png'))
			self.image=pygame.transform.scale(self.image,(150,110))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.commandCenters.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

class GeothermalGenerator(Building):
	def __init__(self,data,x,y,team):
		Building.__init__(self,x,y,team)

		self.image=pygame.image.load(os.path.join('rts_geothermal_generator_construction.png'))
		self.image=pygame.transform.scale(self.image,(25,50))
		self.rect=self.image.get_rect()
		self.xTileOffset=-.8
		self.yTileOffset=-.8
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

		self.name='GeothermalGeneratorX'

		self.prereqs=['CommandCenter']

		self.buildTime=5
		self.woodCost=0
		self.metalCost=100

		self.energy=.05
		self.battery=5

		self.health=500
		self.maxHealth=self.health

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
			if(self.team=='yellow'):
				self.image=pygame.image.load(os.path.join('rts_geothermal_generator_yellow.png'))
			elif(self.team=='blue'):
				self.image=pygame.image.load(os.path.join('rts_geothermal_generator_blue.png'))
			elif(self.team=='red'):
				self.image=pygame.image.load(os.path.join('rts_geothermal_generator_red.png'))
			elif(self.team=='green'):
				self.image=pygame.image.load(os.path.join('rts_geothermal_generator_green.png'))
			self.image=pygame.transform.scale(self.image,(25,50))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)


class Farm(Building):
	def __init__(self,data,x,y,team):
		Building.__init__(self,x,y,team)

		self.image=pygame.Surface([50,50])
		self.rect=self.image.get_rect()
		self.xTileOffset=-.8
		self.yTileOffset=-.8
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

		self.name='FarmX'

		self.prereqs=['CommandCenter']

		self.buildTime=8
		self.woodCost=150
		self.metalCost=0
		self.energy=0
		self.battery=0

		self.supply=5

		self.health=500
		self.maxHealth=self.health

		self.layout=[
		[False,False,False,False],
		[False,True,True,False],
		[False,True,True,False],
		[False,False,False,False]
		]

	def build(self,data):
		if(self.startTime==0):
			self.startTime=time.time()
		self.buildTimeLeft=time.time()-self.startTime
		if(self.buildTime-self.buildTimeLeft<=0):
			self.buildComplete=True
			self.name='Farm'
			if(self.team=='yellow'):
				self.image=pygame.Surface([50,50])
				self.image.fill((255,255,0))
			elif(self.team=='blue'):
				self.image=pygame.Surface([50,50])
				self.image.fill((0,0,255))
			elif(self.team=='red'):
				self.image=pygame.Surface([50,50])
				self.image.fill((255,0,0))
			elif(self.team=='green'):
				self.image=pygame.Surface([50,50])
				self.image.fill((0,255,0))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

class Barracks(Building):
	def __init__(self,data,x,y,team):
		Building.__init__(self,x,y,team)

		self.image=pygame.Surface([100,50])
		self.rect=self.image.get_rect()
		self.xTileOffset=-.8
		self.yTileOffset=-.8
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

		self.name='BarracksX'
		self.prereqs=['Farm']

		self.rally_pointX=self.rect.center[0]
		self.rally_pointY=self.rect.center[1]+100

		self.createStartTime=0
		self.buildQueue=[]

		self.buildTime=15
		self.woodCost=200
		self.metalCost=100
		self.energy=0
		self.battery=0

		self.health=1000
		self.maxHealth=self.health

		self.layout=[
		[False,False,False,False,False],
		[False,True,True,True,False],
		[False,True,True,True,False],
		[False,False,False,False,False]
		]

	def build(self,data):
		if(self.startTime==0):
			self.startTime=time.time()
		self.buildTimeLeft=time.time()-self.startTime
		if(self.buildTime-self.buildTimeLeft<=0):
			self.buildComplete=True
			self.name='Barracks'
			if(self.team=='yellow'):
				self.image=pygame.Surface([100,50])
				self.image.fill((255,255,0))
			elif(self.team=='blue'):
				self.image=pygame.Surface([100,50])
				self.image.fill((0,0,255))
			elif(self.team=='red'):
				self.image=pygame.Surface([100,50])
				self.image.fill((255,0,0))
			elif(self.team=='green'):
				self.image=pygame.Surface([100,50])
				self.image.fill((0,255,0))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

	def createMilitia(self,data):
		if(self.createStartTime==0):
			self.createStartTime=time.time()
		self.createTimeLeft=time.time()-self.createStartTime
		if(rts_units.Militia.getBuildTime()-self.createTimeLeft<=0):
			costs=rts_units.Militia.getBuildCost()
			woodCost=costs['wood']
			metalCost=costs['metals']
			energyCost=costs['energy']
			if(data.localPlayer.metals>=metalCost and data.localPlayer.wood>=woodCost and data.localPlayer.energy>=energyCost):
				data.localPlayer.createMilitia(self.rect.center[0],self.rect.center[1]+self.rect.height//2,self.rally_pointX,self.rally_pointY)
				self.buildQueue.pop(0)
				self.createStartTime=0
				data.localPlayer.metals-=metalCost
				data.localPlayer.wood-=woodCost
				data.localPlayer.energy-=energyCost

class WoodWall(Building):
	def __init__(self,data,x,y,team):
		Building.__init__(self,x,y,team)

		self.image=pygame.Surface([25,50])
		self.rect=self.image.get_rect()
		self.xTileOffset=-.8
		self.yTileOffset=-.8
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]+self.xTileOffset,self.coords[1]+self.yTileOffset)

		self.name='WoodWallX'

		self.prereqs=['Barracks']

		self.buildTime=5
		self.woodCost=25
		self.metalCost=0

		self.energy=0
		self.battery=0

		self.health=1000
		self.maxHealth=self.health

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
			self.name='WoodWall'
			if(self.team=='yellow'):
				self.image=pygame.Surface([25,50])
				self.image.fill((255,255,0))
			elif(self.team=='blue'):
				self.image=pygame.Surface([25,50])
				self.image.fill((0,0,255))
			elif(self.team=='red'):
				self.image=pygame.Surface([25,50])
				self.image.fill((255,0,0))
			elif(self.team=='green'):
				self.image=pygame.Surface([25,50])
				self.image.fill((0,255,0))
			data.localPlayer.inConstruction.remove(self)
			data.localPlayer.buildings.add(self)
			data.localPlayer.select(data,self)
			rts_helpers.updateMenuIcons(data)

def drawBuildings(display,data):
	data.localPlayer.inConstruction.draw(display)
	data.localPlayer.buildings.draw(display)
	if(data.startMenuState!='Singleplayer'):
		for ID in data.otherUsers:
			player=data.otherUsers[ID]
			player.inConstruction.draw(display)
			player.buildings.draw(display)