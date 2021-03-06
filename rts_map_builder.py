import random
import rts_images
import rts_helpers
import pygame
import time
from rts_dev_debug import efficiencyCheck

#function is recursive backtracking and creates forest paths from seed. Compiles sprites when done
@efficiencyCheck
def populateForests(display,data,startTime,forestNum=0,board=None,pos=None,treeCount=1,timeout=3):
	#check if board has been set. Serves same purpose as wrapper
	if(board==None):
		board=data.board
	#check if forest path has been completed
	if(treeCount>=data.forestSize):#step case
		drawLoadBar(display,data,'Planting Trees...',forestNum/data.forestSize)
		pos=None
		treeCount=1
		forestNum+=1
	#check if function is placing first tree in forest
	if(pos==None):
		#find a random location until a valid start location has been found
		randX=random.randint(0,data.cells-1)
		randY=random.randint(0,data.cells-1)
		while(data.board[randX][randY]!='field'):
			randX=random.randint(0,data.cells-1)
			randY=random.randint(0,data.cells-1)
		pos=(randX,randY)
	#compile the tree sprites if all forests have been made to adequate size
	if(forestNum>data.numOfForests):#base case
		return board
	else: #recursive case
		x,y=pos[0],pos[1] #current tree seed
		#check all positions around seed including diags
		moves=[
			(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1)]
		#shuffle moves so that the board does not create a straight line if possible
		random.shuffle(moves)
		if(time.time()-startTime>timeout):
			#print('timeout')
			1/0
		for move in moves:
			#is legal
			if(pos[0]>0 and pos[0]<data.cells-1):
				if(pos[1]>0 and pos[1]<data.cells-1):
					if(board[move[0]][move[1]]=='field'):
						#make move
						board[move[0]][move[1]]='forest'
						#recurse move
						if(populateForests(display,data,startTime,forestNum,board,move,treeCount+1)!=None):
							return board
						#undo move
						board[move[0]][move[1]]='field'
		#moves exhausted
		return None

#function finds all tree locations and builds a sprite at that location
###SLOW BECAUSE OF 2500+ TREE SPRITES COMPILED AT ONCE###
@efficiencyCheck
def compileTreeSprites(display,data):
	drawLoadBar(display,data,'Compiling Tree Sprites...',0)
	iterations=0
	for i in range(len(data.board)):
		iterations+=1
		for j in range(len(data.board[0])):
			iterations+=1
			if(data.board[i][j]=='forest'):
				drawLoadBar(display,data,'Compiling Tree Sprites...',(iterations)/(len(data.board)**2))
				tree=rts_images.Tree(data,i,j)
				data.trees.add(tree)

#function places mines at random unfilled locations
@efficiencyCheck
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

#function finds all mine locations and builds sprite at location
@efficiencyCheck
def compileMineSprites(display,data):
	for i in range(len(data.board)):
		for j in range(len(data.board[0])):
			if(data.board[i][j]=='mine'):
				data.mines.add(rts_images.Mine(data,i,j))

#function gets the position of the entire map as a single rhombus
@efficiencyCheck
def generateMapPos(data):
	point0=rts_helpers.coord2Pos(data,*data.mapCoords[0],'tile')[0]
	point1=rts_helpers.coord2Pos(data,*data.mapCoords[1],'tile')[1]
	point2=rts_helpers.coord2Pos(data,*data.mapCoords[2],'tile')[2]
	point3=rts_helpers.coord2Pos(data,*data.mapCoords[3],'tile')[3]
	return (point0,point1,point2,point3)

#uses mine and forest compilers to build 100x100 tile map
@efficiencyCheck
def buildMap(display,data):
	iterations=0
	for i in range(data.cells):
		iterations+=1
		newRow=[]
		for j in range(data.cells):
			iterations+=1
			newRow.append('field')
		data.board.append(newRow)
	emptyBoard=data.board
	drawLoadBar(display,data,'Planting Trees...',0)
	maxAttempts=25
	attempts=0
	for i in range(maxAttempts):
		try:
			startTime=time.time()
			populateForests(display,data,startTime)
			attempts+=1
			break
		except:
			data.board=emptyBoard
			attempts+=1
	#print(attempts)
	compileTreeSprites(display,data)
	populateMines(display,data)

#creates load bar without use of redraw all so that it can occur within a loop
@efficiencyCheck
def drawLoadBar(display,data,msg,progress):
	display.fill((20,20,20))
	data.loadingScreenImage.draw(display)
	loadmessage=data.font.render(msg+str(int(progress*100))+'%',1,(153,230,255))
	display.blit(loadmessage,(data.width*.4,data.height*.77))
	pygame.draw.rect(display,(76,76,76),(data.width*.1,data.height*.8,data.width*.8,10))
	pygame.draw.rect(display,(153,230,255),(data.width*.1,data.height*.8+2,data.width*.8*progress,6))
	if(data.loadingScreenTip=='CommandCenter'):
		tip='Maximize resource yield by placing your command center closer to mines and trees'
	elif(data.loadingScreenTip=='Marine'):
		tip='Militia, while strong in numbers, become disjointed when conjested. Place your army carefully!'
	elif(data.loadingScreenTip=='Drone'):
		tip='Fun Fact: The developer spent way too much time on this sprite that you can barely see in-game!'
	elif(data.loadingScreenTip=='Farm'):
		tip="Farms greatly increase your army size but at a hefty wood cost. Don't build more than you need!"
	elif(data.loadingScreenTip=='Generator'):
		tip='Generators have a great energy yield but a small battery. Build too many and their yield will become saturated'
	elif(data.loadingScreenTip=='Wall'):
		tip='Walls are cheap and sturdy. Taking the time to build them is worth keeping your enemy at bay'
	elif(data.loadingScreenTip=='Barracks'):
		tip='Barracks are costly and the only way to build an army. Focus these in your opponents bases'
	elif(data.loadingScreenTip=='Beacon'):
		tip='Beacons are sturdy structures but require a lot of energy to upkeep. Target the generators'
	tipLabel=data.font.render(tip,1,(153,230,255))
	display.blit(tipLabel,(data.width*.1,data.height*.9))
	pygame.display.update() 

#draws all map sprites
@efficiencyCheck
def drawMap(display,data):
	rts_images.displayMap(display,data,data.gameX-2500,data.gameY)
	data.visibleNature.empty()
	for mine in data.mines:
		if(rts_helpers.isVisible(data,mine)):
			data.visibleNature.add(mine)
	for tree in data.trees:
		if(rts_helpers.isVisible(data,tree)):
			data.visibleNature.add(tree)
	data.visibleNature.draw(display)