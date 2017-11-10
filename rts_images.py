import pygame,sys
from pygame.locals import *
import os
import rts_helpers
import rts_classes
		
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
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]-1,self.coords[1]-2)

	def updateResources(self,data):
		if(self.wood<1):
			self.kill()

class Drone(pygame.sprite.Sprite):
	"""docstring for Drone"""
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([10,10])
		self.rect=self.image.get_rect()
		self.speed=10
		self.rect.center=(x,y)
		self.desX=x
		self.desY=y
		self.selected=False
		self.flying=True
		self.name='Drone'
		self.wood=0
		self.woodCapacity=25
		self.woodGathering=False

	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		if(rts_helpers.legalPosition(data,self)==False):
			self.rect.center=ogCenter
		if(self.woodGathering):
			self.gatherWood(data)
		if(self.wood>=self.woodCapacity):
			self.woodGathering=False

	def gatherWood(self,data):
		if(len(pygame.sprite.spritecollide(self,data.trees,None))>0):
			for tree in pygame.sprite.spritecollide(self,data.trees,None):
				tree.wood-=1
				tree.updateResources(data)
				self.wood+=1
				print(self.wood,tree.wood)

class MenuButton1(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([45,45])
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self):
		print('menu button 1 pressed')

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

class MenuButton6(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
		self.image=pygame.transform.scale(image,(45,45))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def pressed(self):
		for unit in rts_classes.player1.selected:
			unit.kill()
		rts_classes.player1.menuState=None
		
	