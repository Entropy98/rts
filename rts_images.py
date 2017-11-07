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
		self.coods=(x,y)

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coods[0]-1,self.coods[1]-2)

class Drone(pygame.sprite.Sprite):
	"""docstring for Drone"""
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([10,10])
		self.rect=self.image.get_rect()
		self.speed=10
		self.selected=False
		self.desX=None
		self.desY=None
		self.rect.x=x
		self.rect.y=y
		
		
		
	