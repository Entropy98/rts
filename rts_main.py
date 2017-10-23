from tkinter import *

def init(data):
	data.cells=50
	data.maxCellWidth=100
	data.cellWidth=data.maxCellWidth
	data.zoom=1
	data.boardX=data.width//2
	data.boardY=-50
	data.cursorX=data.cells//2
	data.cursorY=data.cells//2

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
		data.boardY+=10
	elif(event.keysym=='s'):
		data.boardY-=10
	elif(event.keysym=='d'):
		data.boardX-=10
	elif(event.keysym=='a'):
		data.boardX+=10

def timerFired(data):
	pass

def drawGrid(canvas,data):
	for x in range(data.cells):
		for y in range(data.cells):
			xCoord=x
			yCoord=y
			point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
				(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.boardY)

			point1=(((xCoord-1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)

			point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
				((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)

			point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)
			canvas.create_polygon(point0,point1,point2,point3,width=2,fill='white',outline='black')

def drawCursor(canvas,data):
	yCoord=data.cursorY
	xCoord=data.cursorX
	point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
		(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.boardY)

	point1=(((xCoord-1)*.5*data.cellWidth - (yCoord)*.5*data.cellWidth)+data.boardX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)

	point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
		((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)

	point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.boardX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.boardY)
	canvas.create_polygon(point0,point1,point2,point3,width=2,fill='deep sky blue',outline='black')
	coordLabel=str(xCoord)+','+str(yCoord)
	canvas.create_text((point1[0]+point3[0])/2,(point0[1]+point2[1])/2,anchor='center',font='Helvetica 10',text=coordLabel)

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

run(300,300)