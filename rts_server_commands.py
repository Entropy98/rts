import socket
import threading
import rts_classes
from queue import Queue

def joinServer(data,IP='',port=50003):
	HOST = IP # put your IP address here if playing on multiple computers
	PORT = port


	data.server.connect((HOST,PORT))
	print("connected to server")

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

def interpServerCommands(data):
	if (data.serverMsg.qsize() > 0):
		msg = data.serverMsg.get(False)
		try:
			print("received: ", msg, "\n")
			msg = msg.split()
			command = msg[0]

			if (command == "myIDis"):
				ID = msg[1]
				data.localPlayer.ID=ID

			elif(command=='newPlayer'):
				ID=msg[1]
				data.otherUsers[ID]=rts_classes.Player(data.usernameInput)
				update=''
				update+='newUsername %s \n'%data.usernameInput
				update+='newTeam %s \n'%data.localPlayer.team
				data.server.send(update.encode())

			elif(command=='newUsername'):
				ID=msg[1]
				username=msg[2]
				data.otherUsers[ID].username=username

			elif(command=='newTeam'):
				ID=msg[1]
				team=msg[2]
				data.otherUsers[ID].team=team

			elif(command=='startGame'):
				data.playButtonPressed=True

			elif(command=='board'):
				ID=msg[1]
				board=msg[2]
				data.board=board
				data.boardComplete=True

		except:
			print("failed")
		data.serverMsg.task_done()

