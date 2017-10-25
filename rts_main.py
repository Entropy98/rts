from tkinter import *
import rts_helpers
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


def mousePressed(event,data):
	pass

def onMouseWheel(event,data):
	delta=event.delta/120
	data.zoom+=(delta/10)
	data.cellWidth=data.maxCellWidth*data.zoom

def keyPressed(event,data):
	if(event.keysym=='Down'):
		data.cursorY+=1
	elif(event.keysym=='Up'):
		data.cursorY-=1
	elif(event.keysym=='Right'):
		data.cursorX+=1
	elif(event.keysym=='Left'):
		data.cursorX-=1

	if(event.keysym=='w'):
		data.gameY+=10/data.zoom
	elif(event.keysym=='s'):
		data.gameY-=10/data.zoom
	elif(event.keysym=='d'):
		data.gameX-=10/data.zoom
	elif(event.keysym=='a'):
		data.gameX+=10/data.zoom

def timerFired(data):
	pass

def drawGrid(canvas,data):
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
				canvas.create_polygon(point0,point1,point2,point3,width=2,fill='brown',outline='black')
			else:
				canvas.create_polygon(point0,point1,point2,point3,width=2,fill='green',outline='black')
			#tileLabel=data.board[x][y]
			#fontSize=str(int(20*data.zoom))
			#canvas.create_text((point1[0]+point3[0])/2,(point0[1]+point2[1])/2,anchor='center',font='Helvetica '+fontSize,text=tileLabel)


def drawCursor(canvas,data):
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
	canvas.create_polygon(point0,point1,point2,point3,width=2,fill='deep sky blue',outline='black')
	coordLabel=str(xCoord)+','+str(yCoord)
	fontSize=str(int(20*data.zoom))
	canvas.create_text((point1[0]+point3[0])/2,(point0[1]+point2[1])/2,anchor='center',font='Helvetica '+fontSize,text=coordLabel)

def redrawAll(canvas,data):
	drawGrid(canvas,data)
	drawCursor(canvas,data)
	zoomLabel='Zoom: '+str(int(data.zoom*100))+'%'
	canvas.create_text(data.width-20,20,anchor='ne',text=zoomLabel,font='Helvetica 10')

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def onMouseWheelWrapper(event,canvas,data):
		onMouseWheel(event,data)
		redrawAllWrapper(canvas,data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)

	# create the root and the canvas
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:keyPressedWrapper(event, canvas, data))
	root.bind('<MouseWheel>', lambda event:onMouseWheelWrapper(event,canvas,data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed

run(600,600)