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
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])

	def build(self,data):
		if(self.startTime==0):
			self.startTime=time.time()
		self.buildTimeLeft=time.time()-self.startTime
		if(self.buildTime-self.buildTimeLeft<=0):
			self.buildComplete=True
			self.name='CommandCenter'
			self.image=pygame.image.load(os.path.join('rts_command_center.png'))
			self.image=pygame.transform.scale(self.image,(125,84))
			rts_classes.player1.inConstruction.remove(self)
			rts_classes.player1.buildings.add(self)
			rts_classes.player1.commandCenters.add(self)
			rts_classes.player1.menuState='CommandCenter'
			rts_helpers.updateMenuIcons(data)


class CommandCenter(Building):
	def __init__(self,data,x,y):
		Building.__init__(self,x,y)

		self.image=pygame.image.load(os.path.join('rts_command_center_frame.png'))
		self.image=pygame.transform.scale(self.image,(125,84))
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])

		self.name='CommandCenterX'

		self.rally_pointX=self.rect.center[0]
		self.rally_pointY=self.rect.center[1]+100

		self.createStartTime=0
		self.buildQueue=[]

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

	def createDrone(self):
		if(self.createStartTime==0):
			self.createStartTime=time.time()
		self.createTimeLeft=time.time()-self.createStartTime
		if(rts_images.Drone.getBuildTime()-self.createTimeLeft<=0):
			costs=rts_images.Drone.getBuildCost()
			woodCost=costs['wood']
			metalCost=costs['metals']
			if(rts_classes.player1.metals>=metalCost and rts_classes.player1.wood>=woodCost):
				rts_classes.player1.createDrone(self.rect.center[0],self.rect.center[1],self.rally_pointX,self.rally_pointY)
				self.buildQueue.pop(0)
				self.createStartTime=0
				rts_classes.player1.metals-=metalCost
				rts_classes.player1.wood-=woodCost

