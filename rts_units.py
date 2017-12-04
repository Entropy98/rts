import pygame
import rts_helpers
import rts_images
from rts_dev_debug import efficiencyCheck
import random
import os

class Militia(pygame.sprite.Sprite):
	@efficiencyCheck
	def __init__(self,x,y,destX,destY,team):
		pygame.sprite.Sprite.__init__(self)
		self.team=team
		self.ssPos=(0,0)
		self.ssX=4
		self.ssY=12
		self.ssXGap=6
		self.ssYGap=10
		self.spriteWidth=52
		self.spriteHeight=47
		if(self.team=='yellow'):
			self.spritesheet=rts_images.SpriteSheet('rts_yellow_marine_sheet.png')
		elif(self.team=='blue'):
			self.spritesheet=rts_images.SpriteSheet('rts_blue_marine_sheet.png')
		elif(self.team=='red'):
			self.spritesheet=rts_images.SpriteSheet('rts_red_marine_sheet.png')
		elif(self.team=='green'):
			self.spritesheet=rts_images.SpriteSheet('rts_green_marine_sheet.png')
		self.image=self.spritesheet.image_at((self.ssX,self.ssY,self.spriteWidth,self.spriteHeight),(255,255,255))
		self.image=pygame.transform.scale(self.image,(40,44))
		self.rect=self.image.get_rect()
		self.speed=8
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
		self.attacking=False
		self.animationState=0
		self.animationFace='left'
		self.animateDx=0

	@efficiencyCheck
	def attack(self,data):
		if(self.target!=None):
			dist=((self.rect.center[0]-self.target.rect.center[0])**2+(self.rect.center[1]-self.target.rect.center[1])**2)**.5
			if(dist<=self.attackRange):
				self.attacking=True
				if(self.target.rect.center[0]>self.rect.center[0]):
					self.animateAttack(1)
				else:
					self.animateAttack(-1)
				self.desX=self.rect.center[0]
				self.desY=self.rect.center[1]
				self.target.health-=self.damage
				self.target.update(data)
				if(self.target.health<=0):
					self.target=None
			else:
				self.attacking=False
				self.desX=self.target.rect.center[0]
				self.desY=self.target.rect.center[1]
		else:
			self.attacking=False

	@efficiencyCheck
	def animateAttack(self,direction):
		if(direction==-1):
			self.animationFace='left'
		else:
			self.animationFace='right'
		if(self.animationState==1):
			self.image=self.spritesheet.image_at((247,self.ssY,54,self.spriteHeight),(255,255,255))
			self.image=pygame.transform.scale(self.image,(46,40))
			if(self.animationFace=='left'):
				self.rect.x-=2
				self.animateDx=2
			else:
				self.animateDx=0
		elif(self.animationState==0):
			self.image=self.spritesheet.image_at((313,self.ssY,67,self.spriteHeight),(255,255,255))
			self.image=pygame.transform.scale(self.image,(57,40))
			if(self.animationFace=='left'):
				self.rect.x-=11
				self.animateDx=11
			else:
				self.animateDx=0
		if(self.animationFace=='right'):
			self.image=pygame.transform.flip(self.image,True,False)
		self.animationState+=1
		self.animationState%=2

	@staticmethod
	@efficiencyCheck
	def getBuildTime():
		return 10

	@staticmethod
	@efficiencyCheck
	def getBuildCost():
		d={}
		d['metals']=50
		d['wood']=0
		d['energy']=0
		return d

	@efficiencyCheck
	def update(self,data):
		ogCenter=self.rect.center
		if(self.attacking):
			self.rect.x+=self.animateDx
		if(self.attacking==False):
			self.rect.center,moveDir=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
			if(moveDir!=None):
				self.animateMovement(moveDir[0])
			else:
				self.animateMovement(moveDir)
		self.attack(data)
		if(rts_helpers.legalPosition(data,self)==False):
			self.animateMovement(None)
			self.rect.center=ogCenter
		if(self.health<=0):
			self.kill()

	@efficiencyCheck
	def animateMovement(self,direction):
		if(self.animationState==0):
			self.ssPos=(0,1)
		elif(self.animationState==1):
			self.ssPos=(1,1)
		elif(self.animationState==2):
			self.ssPos=(2,1)
		elif(self.animationState==3):
			self.ssPos=(3,1)
		if(direction==None):
			self.ssPos=(0,0)
			self.animationState=0
		elif(direction==1):
			self.animationFace='right'
		elif(direction==-1):
			self.animationFace='left'
		self.image=self.spritesheet.image_at((self.ssX+(self.ssPos[0]*(self.spriteWidth+self.ssXGap)),\
			self.ssY+(self.ssPos[1]*(self.spriteHeight+self.ssYGap)),self.spriteWidth,self.spriteHeight),(255,255,255))
		self.image=pygame.transform.scale(self.image,(44,40))
		if(self.animationFace=='right'):
			self.image=pygame.transform.flip(self.image,True,False)
		self.animationState+=1
		self.animationState%=4


class Drone(pygame.sprite.Sprite):
	"""docstring for Drone"""
	@efficiencyCheck
	def __init__(self,x,y,destX,destY,team):
		pygame.sprite.Sprite.__init__(self)
		self.team=team
		self.spriteWidth=400
		self.spriteHeight=254
		if(self.team=='yellow'):
			self.spritesheet=rts_images.SpriteSheet('rts_drone_yellow_sheet.png')
		elif(self.team=='blue'):
			self.spritesheet=rts_images.SpriteSheet('rts_drone_blue_sheet.png')
		elif(self.team=='red'):
			self.spritesheet=rts_images.SpriteSheet('rts_drone_red_sheet.png')
		elif(self.team=='green'):
			self.spritesheet=rts_images.SpriteSheet('rts_drone_green_sheet.png')
		self.image=self.spritesheet.image_at((0,0,self.spriteWidth,self.spriteHeight),(217,0,255))
		self.image=pygame.transform.scale(self.image,(36,23))
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
		self.animationFace='left'

	@staticmethod
	@efficiencyCheck
	def getBuildTime():
		return 5

	@staticmethod
	@efficiencyCheck
	def getBuildCost():
		d={}
		d['metals']=30
		d['wood']=0
		d['energy']=20
		return d

	@efficiencyCheck
	def update(self,data):
		ogCenter=self.rect.center
		self.rect.center,moveDir=rts_helpers.moveUnit(self.rect.center[0],self.rect.center[1],self.desX,self.desY,self.speed)
		if(moveDir!=None):
			self.animateMovement(moveDir)
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

	@efficiencyCheck
	def animateMovement(self,direction):
		state=''
		if(direction[1]==-1):
			state+='U'
		else:
			state+='D'
		if(direction[0]==-1):
			state+='L'
		else:
			state+='R'
		if(state=='DL'):
			self.image=self.spritesheet.image_at((0,0,self.spriteWidth,self.spriteHeight),(217,0,255))
		elif(state=='UR'):
			self.image=self.spritesheet.image_at((self.spriteWidth,0,self.spriteWidth,self.spriteHeight),(217,0,255))
		elif(state=='DR'):
			self.image=self.spritesheet.image_at((0,273,self.spriteWidth,self.spriteHeight),(217,0,255))
		elif(state=='UL'):
			self.image=self.spritesheet.image_at((self.spriteWidth,273,self.spriteWidth,self.spriteHeight),(217,0,255))
		self.image=pygame.transform.scale(self.image,(36,23))

	@efficiencyCheck
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

	@efficiencyCheck
	def build(self,data):
		if(self.buildState=='Select'):
			self.stencil=rts_helpers.compileBuildStencil(data,self.building.layout)
		elif(self.buildState=='Place'):
			for tile in self.stencil:
				if(tile[0]==False):
					self.buildState='Select'
			if(self.buildState=='Place'):
				if(rts_helpers.buildReqsMet(data,self.building)):
					newCoords=rts_helpers.placeBuilding(data,self.building)
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
					buildingID=random.randint(1000000,9999999)
					data.localPlayer.IDs.add(buildingID)
					self.building.ID=buildingID
					tiles=str(self.building.tiles).replace(' ','')
					msg='buildBuilding %s %d %d %d %s \n'%(self.building.name,self.building.coords[0],self.building.coords[1],buildingID,tiles)
					if(data.startMenuState!='Singleplayer'):
						data.server.send(msg.encode())
				else:
					self.buildState=None
					self.stencil=None
					self.building=None
		elif(self.buildState=='Build'):
			pass

	@efficiencyCheck
	def dropOffMats(self,data):
		data.localPlayer.wood+=self.wood
		self.wood=0
		data.localPlayer.metals+=self.metals
		self.metals=0

	@efficiencyCheck
	def gatherWood(self,data):
		if(len(pygame.sprite.spritecollide(self,data.trees,None))>0):
			self.metalMining=False
			for tree in pygame.sprite.spritecollide(self,data.trees,None):
				self.metals=0
				tree.wood-=1
				tree.updateResources(data)
				self.wood+=1
				break

	@efficiencyCheck
	def mineMetals(self,data):
		if(len(pygame.sprite.spritecollide(self,data.mines,None))>0):
			self.woodGathering=False
			for mine in pygame.sprite.spritecollide(self,data.mines,None):
				self.wood=0
				mine.metals-=1
				mine.updateResources(data)
				self.metals+=1
				break