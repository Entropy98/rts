import random
import rts_images
import rts_helpers

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
		print('Compiling Tree Sprites...')
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
		random.shuffle(moves)
		for move in moves:
			if(pos[0]>0 and pos[0]<data.cells-1):
				if(pos[1]>0 and pos[1]<data.cells-1):
					if(board[move[0]][move[1]]=='field'):
						board[move[0]][move[1]]='forest'
						if(populateForests(data,forestNum,board,move,treeCount+1)!=None):
							return board
						board[move[0]][move[1]]='field'
		return None
