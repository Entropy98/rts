#########################
#adapted from 15-112 Sockets Demo
###########################

import socket
import threading
import rts_classes
import rts_helpers
import rts_buildings
from rts_dev_debug import efficiencyCheck
from queue import Queue

#function connects user to server using default port and given IP
@efficiencyCheck
def joinServer(data,IP='',port=50003):
	HOST = IP # put your IP address here if playing on multiple computers
	PORT = port

	data.server.connect((HOST,PORT))
	print("connected to server")

#background process for receiving serever messages and preparing them for interpretation
@efficiencyCheck
def handleServerMsg(server, serverMsg):
	print('called')
	server.setblocking(1)
	msg = ""
	command = ""
	while True:
		msg += server.recv(10).decode("UTF-8")
		command = msg.split("\n")
		while (len(command) > 1):
			readyMsg = command[0]
			msg = "\n".join(command[1:])
			serverMsg.put(readyMsg)
			command = msg.split("\n")

#various actions for specific server commands
@efficiencyCheck
def interpServerCommands(data):
	if (data.serverMsg.qsize() > 0):
		msg = data.serverMsg.get(False)
		try:
			print("received: ", msg, "\n")
			msg = msg.split()
			command = msg[0]

			#command given upon server connection
			if (command == "myIDis"):
				ID = msg[1]
				data.localPlayer.ID=ID
				if(ID=='alpha'):
					data.localPlayer.role='Host'
				else:
					data.localPlayer.role='Client'

			#command given when another player enters server
			elif(command=='newPlayer'):
				ID=msg[1]
				data.otherUsers[ID]=rts_classes.Player(data.usernameInput)
				if(ID=='alpha'):
					data.otherUsers[ID].role='Host'
				update=''
				update+='newUsername %s \n'%data.usernameInput
				update+='newTeam %s \n'%data.localPlayer.team
				data.server.send(update.encode())

			#command given upon lobby entrance
			elif(command=='newUsername'):
				ID=msg[1]
				username=msg[2]
				data.otherUsers[ID].username=username

			#change teams in lobby
			elif(command=='newTeam'):
				ID=msg[1]
				team=msg[2]
				data.otherUsers[ID].team=team

			#given when host starts game
			elif(command=='startGame'):
				data.playButtonPressed=True

			#given when host is done compiling random board and sends out info
			elif(command=='board'):
				ID=msg[1]
				board=msg[2]
				data.board=board
				data.boardComplete=True

			#whenever Player class creates drone
			elif(command=='createDrone'):
				ID=msg[1]
				x=int(msg[2])
				y=int(msg[3])
				coord=rts_helpers.coord2Pos(data,x,y)
				desX=int(msg[4])
				desY=int(msg[5])
				desCoord=rts_helpers.coord2Pos(data,desX,desY)
				unitID=eval(msg[6]) #possible values are 7 digit int or None
				user=data.otherUsers[ID]
				user.createDrone(data,coord[0],coord[1],desCoord[0],desCoord[1],True,unitID)

			elif(command=='createMilitia'):
				ID=msg[1]
				x=int(msg[2])
				y=int(msg[3])
				coord=rts_helpers.coord2Pos(data,x,y)
				desX=int(msg[4])
				desY=int(msg[5])
				desCoord=rts_helpers.coord2Pos(data,desX,desY)
				unitID=eval(msg[6]) #possible values are 7 digit int or None
				user=data.otherUsers[ID]
				user.createMilitia(data,coord[0],coord[1],desCoord[0],desCoord[1],True,unitID)

			#whenever unit destination changes
			elif(command=='moveUnit'):
				ID=msg[1]
				desX=int(msg[2])
				desY=int(msg[3])
				unitID=eval(msg[4]) #possible values are 7 digit int or None
				for unit in data.otherUsers[ID].units:
					if(unit.ID==unitID):
						unit.desX=unit.rect.center[0]-desX
						unit.desY=unit.rect.center[1]-desY

			#whenever drone builds building
			elif(command=='buildBuilding'):
				ID=msg[1]
				building=msg[2]
				xCoord=int(msg[3])
				yCoord=int(msg[4])
				buildingID=int(msg[5])
				#evals string of list of tuples
				tiles=eval(msg[6])
				user=data.otherUsers[ID]
				if(building=='CommandCenterX'):
					newBuilding=rts_buildings.CommandCenter(data,xCoord,yCoord,user.team)
				elif(building=='GeothermalGeneratorX'):
					newBuilding=rts_buildings.GeothermalGenerator(data,xCoord,yCoord,user.team)
				elif(building=='FarmX'):
					newBuilding=rts_buildings.Farm(data,xCoord,yCoord,user.team)
				elif(building=='BarracksX'):
					newBuilding=rts_buildings.Barracks(data,xCoord,yCoord,user.team)
				elif(building=='WoodWallX'):
					newBuilding=rts_buildings.WoodWallX(data,xCoord,yCoord,user.team)
				newBuilding.ID=buildingID
				newBuilding.tiles=tiles
				user.inConstruction.add(newBuilding)
				for tile in tiles:
					data.board[tile[0]][tile[1]]=user.team

			#whenever player right clicks
			elif(command=='newTarget'):
				ID=msg[1]
				unitID=int(msg[2])
				targetID=eval(msg[3]) #possible values are int or None
				user=data.otherUsers[ID]
				for unit in user.units:
					if(unit.ID==unitID):
						if(targetID!=None):
							unit.target=rts_helpers.findUnitByID(data,targetID)
						else:
							unit.target=None

			elif(command=='winCondition'):
				ID=msg[1]
				condition=msg[2]
				player=msg[3]
				if(ID!=player):
					data.otherUsers[player].winCondition=condition
				else:
					data.localPlayer.winCondition=condition

			elif(command=='destroyBuilding'):
				ID=msg[1]
				unitID=int(msg[2])
				#evals string of list of tuples
				tiles=eval(msg[3])
				for tile in tiles:
					data.board[tile[0]][tile[1]]='field'
				unit=rts_helpers.findUnitByID(data,unitID)
				unit.kill()

			elif(command=='destroyUnit'):
				ID=msg[1]
				unitID=int(msg[2])
				unit=rts_helpers.findUnitByID(data,unitID)
				unit.kill()

			elif(command=='cutTree'):
				ID=msg[1]
				x=msg[2]
				y=msg[3]
				for tree in data.trees:
					if(tree.x==x and tree.y==y):
						tree.kill()
				data.board[x][y]='field'

			elif(command=='ready'):
				ID=msg[1]
				data.otherUsers[ID].multiplayerReady=True


			#whenever a unit/building is dealt damage
			# elif(command=='damageDealt'):
			# 	ID=msg[1]
			# 	unitID=int(msg[2])
			# 	damage=int(msg[3])
			# 	unit=rts_helpers.findUnitByID(data,unitID)
			# 	unit.health-=damage


		except:
			print("failed")
		data.serverMsg.task_done()

