import pygame,sys
from pygame.locals import *
import random

def init(data):
	data.cells=50
	data.maxCellWidth=100
	data.cellWidth=data.maxCellWidth
	data.zoom=1
	data.gameX=data.width//2
	data.gameY=-50
	data.cursorX=data.cells//2
	data.cursorY=data.cells//2
	data.numOfForests=50
	data.forestMinSize=50
	data.forestMaxSize=100
	data.board=[]
	for i in range(data.cells):
		newRow=[]
		for j in range(data.cells):
			newRow.append('field')
		data.board.append(newRow)
	populateForests(data)

def populateForests(data):
	forestSizes=[]
	for i in range(data.numOfForests):
		randX=random.randint(0,data.cells-1)
		randY=random.randint(0,data.cells-1)
		print('creating forest '+str(i),'at',randX,',',randY)
		while(data.board[randX][randY]!='field'):
			randX=random.randint(0,data.cells-1)
			randY=random.randint(0,data.cells-1)
		forestSize=random.randint(data.forestMinSize,data.forestMaxSize+1)
		curTile=(randX,randY)
		forestComplete=False
		finalForestSize=0
		while(finalForestSize<forestSize):
			print('creating tree '+str(i),'at',randX,randY)
			data.board[curTile[0]][curTile[1]]='forest'
			print('tree created at',curTile)
			finalForestSize+=1
			directions=[(curTile[0]+1,curTile[1]),(curTile[0],curTile[1]-1),((curTile[0]-1,curTile[1])),((curTile[0],curTile[1]+1))]
			randDir=random.choice(directions)
			print('next tree location= ',randDir)
			for i in randDir:
				if(i>data.cells-1 or i<0):
					directions.pop(directions.index(randDir))
					if(len(directions)>0):
						randDir=random.choice(directions)
						print('Q next tree location= ',randDir)
			curTileVal=data.board[randDir[0]][randDir[1]]
			while(curTileVal=='forest'):
				directions.pop(directions.index(randDir))
				if(len(directions)>0):
					curTileVal=data.board[randDir[0]][randDir[1]]
					print('invalid tree location',randDir,'already a tree')
					randDir=random.choice(directions)
					print('next tree location= ',randDir)
					for i in randDir:
						if(i>data.cells-1 or i<0):
							directions.pop(directions.index(randDir))
							if(len(directions)>0):
								randDir=random.choice(directions)
								print('next tree location= ',randDir)
				else:
					forestComplete=True
					break
			directions=[(curTile[0]+1,curTile[1]),(curTile[0],curTile[1]-1),((curTile[0]-1,curTile[1])),((curTile[0],curTile[1]+1))]
			if(forestComplete):
				break
			curTile=randDir
		print('----------------------------created forest of size',finalForestSize,'--------------------------------')
		forestSizes.append((finalForestSize,forestSize))
	print(forestSizes)

def mouseDown(event,data):
    if(event.button==5):
    	data.zoom-=.1
    elif(event.button==4):
    	data.zoom+=.1
    data.cellWidth=data.maxCellWidth*data.zoom

def mouseUp(event,data):
    pass

def keyDown(event,data):
	if(event.key==274):#down
		data.cursorY+=1
	elif(event.key==273):#up
		data.cursorY-=1
	elif(event.key==275):#right
		data.cursorX+=1
	elif(event.key==276):#left
		data.cursorX-=1

	if(event.unicode=='w'):
		data.gameY+=10/data.zoom
	elif(event.unicode=='s'):
		data.gameY-=10/data.zoom
	elif(event.unicode=='d'):
		data.gameX-=10/data.zoom
	elif(event.unicode=='a'):
		data.gameX+=10/data.zoom

def keyUp(event,data):
   	pass

def timerFired(data):
    pass

def drawGrid(display,data):
	for x in range(data.cells):
		for y in range(data.cells):
			xCoord=x
			yCoord=y
			point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

			point1=(((xCoord-1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

			point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

			point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
			tileLabel=data.board[x][y]
			if(tileLabel=='forest'):
				pygame.draw.polygon(display,(26,13,0),(point0,point1,point2,point3),2)
			else:
				pygame.draw.polygon(display,(51,153,51),(point0,point1,point2,point3),2)

def drawCursor(display,data):
	yCoord=data.cursorY
	xCoord=data.cursorX
	point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

	point1=(((xCoord-1)*.5*data.cellWidth - (yCoord)*.5*data.cellWidth)+data.gameX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

	point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

	point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
	pygame.draw.polygon(display,(153,230,255),(point0,point1,point2,point3),2)
	coordLabel=str(xCoord)+','+str(yCoord)
	fontSize=int(20*data.zoom)
	font=pygame.font.SysFont('Helvetica',fontSize)
	textSurface=font.render(coordLabel,False,(0,0,0))
	display.blit(textSurface,((((point1[0]+point3[0])//2)-fontSize,((point0[1]+point2[1])//2)-.5*fontSize)))

def redrawAll(display, data):
	drawGrid(display,data)
	drawCursor(display,data)

def run(width=300, height=300):
	def redrawAllWrapper(display, data):
		display.fill((255,255,255))
		redrawAll(display, data)
		pygame.display.update()  

	def mouseDownWrapper(event, display, data):
		mouseDown(event, data)
		redrawAllWrapper(display, data)

	def mouseUpWrapper(event, display, data):
		mouseUp(event, data)
		redrawAllWrapper(display, data)

	def keyDownWrapper(event, display, data):
		keyDown(event,data)
		redrawAllWrapper(display, data)

	def keyUpWrapper(event, display, data):
		keyUp(event,data)
		redrawAllWrapper(display, data)

	def quit():
		pygame.quit()
		sys.exit()

	def timerFiredWrapper(display, data):
		timerFired(data)
		redrawAllWrapper(display, data)
		data.fpsClock.tick(data.fps)

	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.fps=30 #frames per second
	data.fpsClock=pygame.time.Clock()
	init(data)

	# initialize module and display
	pygame.init()
	pygame.font.init()
	display = pygame.display.set_mode((data.width,data.height))
	pygame.display.set_caption('RTS')

	#main loop
	while(True):
		for event in pygame.event.get():
			if(event.type==QUIT):
				quit()
			if(event.type==KEYDOWN):
				keyDownWrapper(event,display,data)
			if(event.type==KEYUP):
				keyUpWrapper(event,display,data)
			if(event.type==MOUSEBUTTONDOWN):
				mouseDownWrapper(event,display,data)
			if(event.type==MOUSEBUTTONUP):
				mouseUpWrapper(event,display,data)
		timerFiredWrapper(display,data)

run(600,600)