import pygame,sys
from pygame.locals import *
import os
import rts_helpers
		
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

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0]-1,self.coords[1]-2)

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

	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		if(rts_helpers.legalPosition(data,self)==False):
			self.rect.center=ogCenter
		
		
	