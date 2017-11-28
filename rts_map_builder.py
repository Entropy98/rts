import random
import rts_images
import rts_helpers
import pygame
import time

def populateForests(display,data,forestNum=0,board=None,pos=None,treeCount=1):
	if(board==None):
		board=data.board
	if(treeCount>=data.forestSize):#step case
		drawLoadBar(display,data,'Planting Trees...',forestNum/data.forestSize)
		pos=None
		treeCount=1
		forestNum+=1
	if(pos==None):
		#find a random location until a valid start location has been found
		randX=random.randint(0,data.cells-1)
		randY=random.randint(0,data.cells-1)
		while(data.board[randX][randY]!='field'):
			randX=random.randint(0,data.cells-1)
			randY=random.randint(0,data.cells-1)
		pos=(randX,randY)
	if(forestNum>data.numOfForests):#base case
		compileTreeSprites(display,data)
		return board
	else:
		x,y=pos[0],pos[1]
		moves=[
			(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1)]
		random.shuffle(moves)
		for move in moves:
			if(pos[0]>0 and pos[0]<data.cells-1):
				if(pos[1]>0 and pos[1]<data.cells-1):
					if(board[move[0]][move[1]]=='field'):
						board[move[0]][move[1]]='forest'
						if(populateForests(display,data,forestNum,board,move,treeCount+1)!=None):
							return board
						board[move[0]][move[1]]='field'
		return None

def compileTreeSprites(display,data):
	drawLoadBar(display,data,'Compiling Tree Sprites...',0)
	iterations=0
	print(data.board)
	for i in range(len(data.board)):
		iterations+=1
		for j in range(len(data.board[0])):
			iterations+=1
			if(data.board[i][j]=='forest'):
				drawLoadBar(display,data,'Compiling Tree Sprites...',(iterations)/(len(data.board)**2))
				tree=rts_images.Tree(data,i,j)
				data.trees.add(tree)

def populateMines(display,data):
	drawLoadBar(display,data,'Digging Mines...',0)
	numOfMines=0
	while(numOfMines<data.numOfMines):
		randX=random.randint(0,data.cells-1)
		randY=random.randint(0,data.cells-1)
		while(data.board[randX][randY]!='field'):
			randX=random.randint(0,data.cells-1)
			randY=random.randint(0,data.cells-1)
		drawLoadBar(display,data,'Digging Mines...',numOfMines/data.numOfMines)
		data.board[randX][randY]='mine'
		numOfMines+=1
	compileMineSprites(display,data)

def compileMineSprites(display,data):
	for i in range(len(data.board)):
		for j in range(len(data.board[0])):
			if(data.board[i][j]=='mine'):
				data.mines.add(rts_images.Mine(data,i,j))

def generateMapPos(data):
	point0=rts_helpers.coord2Pos(data,*data.mapCoords[0],'tile')[0]
	point1=rts_helpers.coord2Pos(data,*data.mapCoords[1],'tile')[1]
	point2=rts_helpers.coord2Pos(data,*data.mapCoords[2],'tile')[2]
	point3=rts_helpers.coord2Pos(data,*data.mapCoords[3],'tile')[3]
	return (point0,point1,point2,point3)

def buildMap(display,data):
	drawLoadBar(display,data,'Constructing Board...',0)
	iterations=0
	for i in range(data.cells):
		iterations+=1
		newRow=[]
		for j in range(data.cells):
			iterations+=1
			drawLoadBar(display,data,'Constructing Board...',(iterations)/(data.cells**2))
			newRow.append('field')
		data.board.append(newRow)
	drawLoadBar(display,data,'Planting Trees...',0)
	populateForests(display,data)
	populateMines(display,data)

def drawLoadBar(display,data,msg,progress):
	display.fill((20,20,20))
	loadmessage=data.font.render(msg+str(int(progress*100))+'%',1,(153,230,255))
	display.blit(loadmessage,(data.width*.4,data.height*.77))
	pygame.draw.rect(display,(76,76,76),(data.width*.1,data.height*.8,data.width*.8,10))
	pygame.draw.rect(display,(153,230,255),(data.width*.1,data.height*.8+2,data.width*.8*progress,6))
	pygame.display.update() 

def drawMap(display,data):
	rts_images.displayMap(display,data,data.gameX-2500,data.gameY)
	data.mines.draw(display)
	data.trees.draw(display)