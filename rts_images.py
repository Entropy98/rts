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

class Mine(pygame.sprite.Sprite):
	"""docstring for Tree"""
	def __init__(self,data,x,y):
		pygame.sprite.Sprite.__init__(self)
		image=pygame.image.load(os.path.join('rts_mine.png'))
		image=pygame.transform.scale(image,(50,50))
		self.image=image
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,x,y)
		self.coords=(x,y)
		self.metals=10000

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]-.5,self.coords[1]-.5)

	def updateResources(self,data):
		if(self.metals<1):
			self.kill()

class MenuButton1(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		if(data.localPlayer.menuState=='Drone'):
			data.localPlayer.menuState='Drone_b1'
			rts_helpers.updateMenuIcons(data)
		elif(data.localPlayer.menuState=='Drone_b1'):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.CommandCenter(data,-100,-100,data.localPlayer.team)
					unit.buildState='Select'
					unit.building=building
					break
		elif(data.localPlayer.menuState=='Drone_b2'):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.Barracks(data,-100,-100,data.localPlayer.team)
					unit.buildState='Select'
					unit.building=building
					break
		elif(data.localPlayer.menuState=='CommandCenter'):
			for building in data.localPlayer.selected:
				if(building.name=='CommandCenter'):
					if(len(building.buildQueue)<5):
						building.buildQueue.append('Drone')
					break
		elif(data.localPlayer.menuState=='Barracks'):
			for building in data.localPlayer.selected:
				if(building.name=='Barracks'):
					if(len(building.buildQueue)<5):
						building.buildQueue.append('Militia')
					break
		data.localPlayer.menuHover=None

	def hover(self,data):
		if(data.localPlayer.menuState=='Drone'):
			data.localPlayer.menuHover='Drone_b1'
		elif(data.localPlayer.menuState=='Drone_b1'):
			data.localPlayer.menuHover='CommandCenter'
		elif(data.localPlayer.menuState=='Drone_b2'):
			data.localPlayer.menuHover='Barracks'
		elif(data.localPlayer.menuState=='CommandCenter'):
			data.localPlayer.menuHover='Build_Drone'
		elif(data.localPlayer.menuState=='Barracks'):
			data.localPlayer.menuHover='Train_Militia'

class MenuButton2(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		if(data.localPlayer.menuState=='Drone'):
			data.localPlayer.menuState='Drone_b2'
			rts_helpers.updateMenuIcons(data)
		elif(data.localPlayer.menuState=='Drone_b1'):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.GeothermalGenerator(data,-100,-100,data.localPlayer.team)
					unit.buildState='Select'
					unit.building=building
					break
		elif(data.localPlayer.menuState=='Drone_b2'):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.WoodWall(data,-100,-100,data.localPlayer.team)
					unit.buildState='Select'
					unit.building=building
					break

	def hover(self,data):
		if(data.localPlayer.menuState=='Drone'):
			data.localPlayer.menuHover='Drone_b2'
		elif(data.localPlayer.menuState=='Drone_b1'):
			data.localPlayer.menuHover='GeothermalGenerator'
		elif(data.localPlayer.menuState=='Drone_b2'):
			data.localPlayer.menuHover='WoodWall'

class MenuButton3(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		if(data.localPlayer.menuState=='Drone_b1'):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					building=rts_buildings.Farm(data,-100,-100,data.localPlayer.team)
					unit.buildState='Select'
					unit.building=building
					break

	def hover(self,data):
		if(data.localPlayer.menuState=='Drone_b1'):
			data.localPlayer.menuHover='Farm'

class MenuButton4(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		for unit in data.localPlayer.selected:
			if(unit.name=='Drone'):
				unit.woodGathering=True
				unit.metalMining=True
			elif(unit.name=='CommandCenter'):
				unit.rallyReset=True
				break
			elif(unit.name=='Barracks'):
				unit.rallyReset=True
				break
		data.localPlayer.menuHover=None

	def hover(self,data):
		for unit in data.localPlayer.selected:
			if(unit.name=='Drone'):
				data.localPlayer.menuHover='Drone_Action'
			elif(unit.name=='CommandCenter'):
				data.localPlayer.menuHover='Rally_Point'
			elif(unit.name=='Barracks'):
				data.localPlayer.menuHover='Rally_Point'

class MenuButton6(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self,data):
		if(data.localPlayer.menuState=='Drone'):
			for unit in data.localPlayer.selected:
				unit.kill()
			data.localPlayer.menuState=None
		elif(data.localPlayer.menuState=='Drone_b1' or data.localPlayer.menuState=='Drone_b2'):
			data.localPlayer.menuState='Drone'
			rts_helpers.updateMenuIcons(data)
		elif(data.localPlayer.menuState=='CommandCenter' or data.localPlayer.menuState=='Barracks'):
			for unit in data.localPlayer.selected:
				unit.kill()
		data.localPlayer.menuHover=None

	def hover(self,data):
		if(data.localPlayer.menuState=='Drone'):
			data.localPlayer.menuHover='Destroy'
		elif(data.localPlayer.menuState=='Drone_b1' or data.localPlayer.menuState=='Drone_b2'):
			data.localPlayer.menuHover='Escape'
		elif(data.localPlayer.menuState=='CommandCenter' or data.localPlayer.menuState=='Barracks'):
			data.localPlayer.menuHover='Destroy'

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

class GeothermalGeneratorIcon(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_geothermal_generator_icon.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class FarmIcon(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_farm_icon.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class WoodWallIcon(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_wood_wall_icon.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class QueueIcon1(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_queue_icon1.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class QueueIcon2(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_queue_icon2.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class QueueIcon3(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_queue_icon3.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

class QueueIcon4(pygame.sprite.Sprite):
	def __init__(self,x,y,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join('rts_queue_icon4.png'))
		self.image=pygame.transform.scale(self.image,(width,height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		
	