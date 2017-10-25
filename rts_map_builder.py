import random

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
			while(randDir[0]>data.cells-1 or randDir[0]<0 or randDir[1]>data.cells-1 or randDir[1]<0):
				for i in randDir:
					if(i>data.cells-1 or i<0):
						print('invalid tree location:',i,'out of range')
						directions.pop(directions.index(randDir))
						if(len(directions)>0):
							randDir=random.choice(directions)
							print('next tree location= ',randDir)
			curTileVal=data.board[randDir[0]][randDir[1]]
			while(curTileVal=='forest'):
				if(randDir in directions):
					directions.pop(directions.index(randDir))
				if(len(directions)>0):
					curTileVal=data.board[randDir[0]][randDir[1]]
					print('invalid tree location:',randDir,'already a tree')
					randDir=random.choice(directions)
					print('next tree location= ',randDir)
					for i in randDir:
						print('tree coordinate: ',i)
						if(i>data.cells-1 or i<0):
							print('invalid tree location:',i,'out of range')
							directions.pop(directions.index(randDir))
							if(len(directions)>0):
								randDir=random.choice(directions)
								print('next tree location= ',randDir)
							else:
								forestComplete=True
								break
				else:
					forestComplete=True
				if(forestComplete):
					break
			directions=[(curTile[0]+1,curTile[1]),(curTile[0],curTile[1]-1),((curTile[0]-1,curTile[1])),((curTile[0],curTile[1]+1))]
			if(forestComplete):
				break
			curTile=randDir
		print('----------------------------created forest of size',finalForestSize,'--------------------------------')
		forestSizes.append((finalForestSize,forestSize))
	print(forestSizes)