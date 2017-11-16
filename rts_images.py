import pygame,sys
from pygame.locals import *
import os
import rts_helpers
import rts_classes
import rts_buildings
		
def loadImages(data):
	data.map=pygame.image.load(os.path.join('rts_map.png'))

def displayMap(display,data,x,y):
	pic=pygame.transform.scale(data.map,(5000,2500))
	display.blit(pic,(x,y))

class Tree(pygame.sprite.Sprite):
	"""docstring for Tree"""
	def __init__(self,data,x,y):
		pygame.sprite.Sprite.__init__(self)
		image=pygame.image.load(os.path.join('rts_tree.png'))
		image=pygame.transform.scale(image,(50,100))
		self.image=image
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,x,y)
		self.coords=(x,y)
		self.wood=50

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]-1.5,self.coords[1]-1.5)

	def updateResources(self,data):
		if(self.wood<1):
			self.kill()

class Drone(pygame.sprite.Sprite):
	"""docstring for Drone"""
	def __init__(self,x,y,destX,destY):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_drone_dl1_yellow.png'))
		self.image=pygame.transform.scale(self.image,(20,12))
		self.rect=self.image.get_rect()
		self.speed=10
		self.rect.center=(x,y)
		self.selected=False
		self.flying=True
		self.desX=destX
		self.desY=destY
		self.name='Drone'
		self.wood=0
		self.woodCapacity=25
		self.woodGathering=False
		self.buildState=None
		self.building=None
		self.stencil=None

	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		self.build(data)
		if(rts_helpers.legalPosition(data,self)==False):
			self.rect.center=ogCenter
		if(self.woodGathering):
			self.gatherWood(data)
		if(self.wood>=self.woodCapacity):
			self.woodGathering=False

	def build(self,data):
		if(self.buildState=='Select'):
			self.stencil=rts_helpers.compileBuildStencil(data,self.building.layout)
		elif(self.buildState=='Place'):
			for tile in self.stencil:
				if(tile[0]==False):
					self.buildState='Select'
			if(self.buildState=='Place'):
				if(rts_classes.player1.wood>=self.building.woodCost):
					newCoords=rts_helpers.placeBuilding(data,self.building.layout)
					self.building.coords=newCoords
					self.building.rect.center=rts_helpers.coord2Pos(data,newCoords[0],newCoords[1])
					self.building.rally_pointX=self.building.rect.center[0]
					self.building.rally_pointY=self.building.rect.center[1]+100
					self.buildState='Build'
					rts_classes.player1.inConstruction.add(self.building)
					self.stencil=None
					rts_classes.player1.wood-=self.building.woodCost
				else:
					self.buildState=None
					self.stencil=None
					self.building=None
		elif(self.buildState=='Build'):
			pass

	def dropOffMats(self):
		rts_classes.player1.wood+=self.wood
		self.wood=0

	def gatherWood(self,data):
		if(len(pygame.sprite.spritecollide(self,data.trees,None))>0):
			for tree in pygame.sprite.spritecollide(self,data.trees,None):
				tree.wood-=1
				tree.updateResources(data)
				self.wood+=1
				break

class MenuButton1(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		if(rts_classes.player1.menuState=='Drone'):
			rts_classes.player1.menuState='Drone_b1'
			rts_helpers.updateMenuIcons(data)
		elif(rts_classes.player1.menuState=='Drone_b1'):
			for unit in rts_classes.player1.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.CommandCenter(data,-100,-100)
					unit.buildState='Select'
					unit.building=building
					break
		elif(rts_classes.player1.menuState=='CommandCenter'):
			for building in rts_classes.player1.selected:
				if(building.name=='CommandCenter'):
					rts_classes.player1.createDrone(building.rect.center[0],building.rect.center[1],building.rally_pointX,building.rally_pointY)
					break

class MenuButton4(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		for unit in rts_classes.player1.selected:
			if(unit.name=='Drone'):
				unit.woodGathering=True
			elif(unit.name=='CommandCenter'):
				unit.rallyReset=True
				break

class MenuButton6(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self):
		if(rts_classes.player1.menuState=='Drone'):
			for unit in rts_classes.player1.selected:
				unit.kill()
			rts_classes.player1.menuState=None
		elif(rts_classes.player1.menuState=='Drone_b1'):
			rts_classes.player1.menuState='Drone'
		elif(rts_classes.player1.menuState=='CommandCenter'):
			for unit in rts_classes.player1.selected:
				unit.kill()

class DroneIcon(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_drone_icon.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class CommandCenterIcon(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_command_center_icon.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		
	