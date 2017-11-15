import pygame
import time
import rts_classes
import rts_helpers

class Building(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.x=x
		self.y=y
		self.coords=(x,y)
		self.buildComplete=False

	def update(self,data):
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])
		if(self not in rts_classes.player1.buildings and self.buildComplete):
			print('done Building')
			rts_classes.player1.inConstruction.remove(self)
			rts_classes.player1.buildings.add(self)

	def build(self,startTime=0):
		if(self.buildTime-(time.time()-startTime)<=0):
			self.buildComplete=True


class CommandCenter(Building):
	def __init__(self,data,x,y):
		Building.__init__(self,x,y)

		self.image=pygame.Surface([150,75])
		self.image.fill((0,0,255))
		self.rect=self.image.get_rect()
		self.rect.center=rts_helpers.coord2Pos(data,self.coords[0],self.coords[1])

		self.buildTime=15

		self.stencil=[
		[False,False,False,False,False],
		[False,True,True,True,False],
		[False,True,True,True,False],
		[False,True,True,True,False],
		[False,False,False,False,False]
		]

