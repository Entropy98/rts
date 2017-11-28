import pygame
import rts_helpers
import os

class Militia(pygame.sprite.Sprite):
	def __init__(self,x,y,destX,destY,team):
		pygame.sprite.Sprite.__init__(self)
		self.team=team
		if(self.team=='yellow'):
			self.image=pygame.Surface([15,25])
			self.image.fill((255,255,0))
		elif(self.team=='blue'):
			self.image=pygame.Surface([15,25])
			self.image.fill((0,0,255))
		elif(self.team=='red'):
			self.image=pygame.Surface([15,25])
			self.image.fill((255,0,0))
		elif(self.team=='green'):
			self.image=pygame.Surface([15,25])
			self.image.fill((0,255,0))
		self.rect=self.image.get_rect()
		self.speed=5
		self.rect.center=(x,y)
		self.selected=False
		self.flying=False
		self.desX=destX
		self.desY=destY
		self.name='Militia'
		self.damage=5
		self.health=100
		self.maxHealth=self.health
		self.attackRange=300
		self.target=None

	def attack(self,data):
		if(self.target!=None):
			dist=((self.rect.center[0]-self.target.rect.center[0])**2+(self.rect.center[1]-self.target.rect.center[1])**2)**.5
			if(dist<=self.attackRange):
				self.desX=self.rect.center[0]
				self.desY=self.rect.center[1]
				self.target.health-=self.damage
				self.target.update(data)
				if(self.target.health<=0):
					self.target=None
			else:
				self.desX=self.target.rect.center[0]
				self.desY=self.target.rect.center[1]

	@staticmethod
	def getBuildTime():
		return 10

	@staticmethod
	def getBuildCost():
		d={}
		d['metals']=50
		d['wood']=0
		d['energy']=0
		return d

	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		self.attack(data)
		if(rts_helpers.legalPosition(data,self)==False):
			self.rect.center=ogCenter
		if(self.health<=0):
			self.kill()

class Drone(pygame.sprite.Sprite):
	"""docstring for Drone"""
	def __init__(self,x,y,destX,destY,team):
		pygame.sprite.Sprite.__init__(self)
		self.team=team
		if(self.team=='yellow'):
			self.image=pygame.image.load(os.path.join('rts_drone_dl1_yellow.png'))
		elif(self.team=='blue'):
			self.image=pygame.image.load(os.path.join('rts_drone_dl1_blue.png'))
		elif(self.team=='red'):
			self.image=pygame.image.load(os.path.join('rts_drone_dl1_red.png'))
		elif(self.team=='green'):
			self.image=pygame.image.load(os.path.join('rts_drone_dl1_green.png'))
		self.image=pygame.transform.scale(self.image,(24,15))
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
		self.metalMining=False
		self.metalCapacity=15
		self.metals=0
		self.buildState=None
		self.building=None
		self.stencil=None
		self.damage=.1
		self.health=50
		self.maxHealth=self.health
		self.attackRange=50
		self.target=None

	@staticmethod
	def getBuildTime():
		return 5

	@staticmethod
	def getBuildCost():
		d={}
		d['metals']=30
		d['wood']=0
		d['energy']=50
		return d

	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		self.attack(data)
		self.build(data)
		if(rts_helpers.legalPosition(data,self)==False):
			self.rect.center=ogCenter
		if(self.woodGathering):
			self.gatherWood(data)
		if(self.wood>=self.woodCapacity):
			self.woodGathering=False
		if(self.metalMining):
			self.mineMetals(data)
		if(self.metals>=self.metalCapacity):
			self.metalMining=False
		if(self.health<=0):
			self.kill()

	def attack(self,data):
		if(self.target!=None):
			dist=((self.rect.center[0]-self.target.rect.center[0])**2+(self.rect.center[1]-self.target.rect.center[1])**2)**.5
			if(dist<=self.attackRange):
				self.desX=self.rect.center[0]
				self.desY=self.rect.center[1]
				self.target.health-=self.damage
				self.target.update(data)
				if(self.target.health<=0):
					self.target=None
			else:
				self.desX=self.target.rect.center[0]
				self.desY=self.target.rect.center[1]

	def build(self,data):
		if(self.buildState=='Select'):
			self.stencil=rts_helpers.compileBuildStencil(data,self.building.layout)
		elif(self.buildState=='Place'):
			for tile in self.stencil:
				if(tile[0]==False):
					self.buildState='Select'
			if(self.buildState=='Place'):
				if(rts_helpers.buildReqsMet(data,self.building)):
					newCoords=rts_helpers.placeBuilding(data,self.building.layout)
					self.building.coords=newCoords
					self.building.rect.center=rts_helpers.coord2Pos(data,newCoords[0],newCoords[1])
					self.building.rally_pointX=self.building.rect.center[0]
					self.building.rally_pointY=self.building.rect.center[1]+100
					self.buildState='Build'
					data.localPlayer.inConstruction.add(self.building)
					self.stencil=None
					data.localPlayer.metals-=self.building.metalCost
					data.localPlayer.wood-=self.building.woodCost
					self.building.update(data)
				else:
					self.buildState=None
					self.stencil=None
					self.building=None
		elif(self.buildState=='Build'):
			pass

	def dropOffMats(self,data):
		data.localPlayer.wood+=self.wood
		self.wood=0
		data.localPlayer.metals+=self.metals
		self.metals=0

	def gatherWood(self,data):
		if(len(pygame.sprite.spritecollide(self,data.trees,None))>0):
			self.metalMining=False
			for tree in pygame.sprite.spritecollide(self,data.trees,None):
				self.metals=0
				tree.wood-=1
				tree.updateResources(data)
				self.wood+=1
				break

	def mineMetals(self,data):
		if(len(pygame.sprite.spritecollide(self,data.mines,None))>0):
			self.woodGathering=False
			for mine in pygame.sprite.spritecollide(self,data.mines,None):
				self.wood=0
				mine.metals-=1
				mine.updateResources(data)
				self.metals+=1
				break