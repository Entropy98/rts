import random
import rts_images
import rts_helpers

# def populateForests(data):
# 	forestSizes=[]
# 	for i in range(data.numOfForests):
# 		randX=random.randint(0,data.cells-1)
# 		randY=random.randint(0,data.cells-1)
# 		while(data.board[randX][randY]!='field'):
# 			randX=random.randint(0,data.cells-1)
# 			randY=random.randint(0,data.cells-1)
# 		forestSize=random.randint(data.forestMinSize,data.forestMaxSize+1)
# 		curTile=(randX,randY)
# 		forestComplete=False
# 		finalForestSize=0
# 		while(finalForestSize<forestSize):
# 			data.board[curTile[0]][curTile[1]]='forest'
# 			finalForestSize+=1
# 			directions=[(curTile[0]+1,curTile[1]),(curTile[0],curTile[1]-1),((curTile[0]-1,curTile[1])),((curTile[0],curTile[1]+1))]
# 			randDir=random.choice(directions)
# 			while(randDir[0]>data.cells-1 or randDir[0]<0 or randDir[1]>data.cells-1 or randDir[1]<0):
# 				for i in randDir:
# 					if(i>data.cells-1 or i<0):
# 						directions.pop(directions.index(randDir))
# 						if(len(directions)>0):
# 							randDir=random.choice(directions)
# 			curTileVal=data.board[randDir[0]][randDir[1]]
# 			while(curTileVal=='forest'):
# 				if(randDir in directions):
# 					directions.pop(directions.index(randDir))
# 				if(len(directions)>0):
# 					curTileVal=data.board[randDir[0]][randDir[1]]
# 					randDir=random.choice(directions)
# 					while(randDir[0]>data.cells-1 or randDir[0]<0 or randDir[1]>data.cells-1 or randDir[1]<0):
# 						for i in randDir:
# 							if(i>data.cells-1 or i<0):
# 								directions.pop(directions.index(randDir))
# 								if(len(directions)>0):
# 									randDir=random.choice(directions)
# 								else:
# 									forestComplete=True
# 									break
# 				else:
# 					forestComplete=True
# 				if(forestComplete):
# 					break
# 			directions=[(curTile[0]+1,curTile[1]),(curTile[0],curTile[1]-1),((curTile[0]-1,curTile[1])),((curTile[0],curTile[1]+1))]
# 			if(forestComplete):
# 				break
# 			curTile=randDir
# 		forestSizes.append((finalForestSize,forestSize))

def populateForests(data,forestNum=0,board=None,pos=None,treeCount=1):
	if(board==None):
		board=data.board
	if(treeCount>=data.forestSize):#step case
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
		print('Complete')
		print('Compiling Tree Sprites...',end='')
		for i in range(len(board)):
			for j in range(len(board[0])):
				if(board[i][j]=='forest'):
					tree=rts_images.Tree(data,i,j)
					data.trees.add(tree)
		print('Complete')
		return board
	else:
		x,y=pos[0],pos[1]
		moves=[
			(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1)]
		for move in moves:
			if(board[move[0]][move[1]]=='field'):
				board[move[0]][move[1]]='forest'
				if(populateForests(data,forestNum,board,move,treeCount+1)!=None):
					return board
				board[move[0]][move[1]]='field'
		return None
