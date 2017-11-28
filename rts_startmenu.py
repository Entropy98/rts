import pygame

def drawMenu(display,data):
	pygame.draw.rect(display,(20,20,20),(0,0,data.width,data.height))
	nameLabel=data.titleFont.render('',1,(20,20,20))
	#pygame.draw.line(display,(0,0,0),(data.width/2,0),(data.width/2,data.height))
	if(data.startMenuState=='Start'):
		nameLabel=data.titleFont.render('Second Earth',1,(153,230,255))
		if(data.startMenuSelect==1):
			pygame.draw.rect(display,(76,76,76),(data.width/2-100,data.height*.35,200,40))	
		pygame.draw.rect(display,(153,230,255),(data.width/2-100,data.height*.35,200,40),3)
		singplayerLabel=data.menuFont.render('Singleplayer',1,(153,230,255))
		display.blit(singplayerLabel,(data.width/2-70,data.height*.35))
		if(data.startMenuSelect==2):
			pygame.draw.rect(display,(76,76,76),(data.width/2-100,data.height*.43,200,40))	
		pygame.draw.rect(display,(153,230,255),(data.width/2-100,data.height*.43,200,40),3)
		multiplayerLabel=data.menuFont.render('Multiplayer',1,(153,230,255))
		display.blit(multiplayerLabel,(data.width/2-60,data.height*.43))
	elif(data.startMenuState=='Singleplayer'):
		nameLabel=data.titleFont.render('Singleplayer',1,(153,230,255))
		usernameLabel=data.menuFont.render('Username: ',1,(153,230,255))
		display.blit(usernameLabel,(data.width*.2,data.height*.35))
		pygame.draw.rect(display,(153,230,255),(data.width*.41,data.height*.35,200,40),1)
		if(data.singlePlayerTextBoxSelect==1):
			textBox1Text=data.menuFont.render(data.usernameInput+'_',1,(153,230,255))
		else:
			textBox1Text=data.menuFont.render(data.usernameInput,1,(153,230,255))
		display.blit(textBox1Text,(data.width*.41+5,data.height*.35))
		playLabel=data.menuFont.render('Start Game',1,(153,230,255))
		if(data.playButtonHover):
			pygame.draw.rect(display,(76,76,76),(data.width/2-80,data.height*.8,160,40))
		pygame.draw.rect(display,(153,230,255),(data.width/2-80,data.height*.8,160,40),3)
		display.blit(playLabel,(data.width/2-63,data.height*.8))
	elif(data.startMenuState=='Multiplayer'):
		nameLabel=data.titleFont.render('Multiplayer',1,(153,230,255))
		usernameLabel=data.menuFont.render('Username: ',1,(153,230,255))
		display.blit(usernameLabel,(data.width*.2,data.height*.35))
		pygame.draw.rect(display,(153,230,255),(data.width*.41,data.height*.35,200,40),1)
		if(data.multiplayerTextBoxSelect==1):
			textBox1Text=data.menuFont.render(data.usernameInput+'_',1,(153,230,255))
		else:
			textBox1Text=data.menuFont.render(data.usernameInput,1,(153,230,255))
		display.blit(textBox1Text,(data.width*.41+5,data.height*.35))

		IPLabel=data.menuFont.render('IP: ',1,(153,230,255))
		display.blit(IPLabel,(data.width*.355,data.height*.5))
		pygame.draw.rect(display,(153,230,255),(data.width*.41,data.height*.5,200,40),1)
		if(data.multiplayerTextBoxSelect==2):
			textBox2Text=data.menuFont.render(data.IPInput+'_',1,(153,230,255))
		else:
			textBox2Text=data.menuFont.render(data.IPInput,1,(153,230,255))
		display.blit(textBox2Text,(data.width*.41+5,data.height*.5))

		hostLabel=data.menuFont.render('Host',1,(153,230,255))
		if(data.multiplayerButtonHover==1):
			pygame.draw.rect(display,(76,76,76),(data.width*.28,data.height*.8,100,40))
		pygame.draw.rect(display,(153,230,255),(data.width*.28,data.height*.8,100,40),3)
		display.blit(hostLabel,(data.width*.32,data.height*.8))
		joinLabel=data.menuFont.render('Join',1,(153,230,255))
		if(data.multiplayerButtonHover==2):
			pygame.draw.rect(display,(76,76,76),(data.width*.58,data.height*.8,100,40))
		pygame.draw.rect(display,(153,230,255),(data.width*.58,data.height*.8,100,40),3)
		display.blit(joinLabel,(data.width*.62,data.height*.8))
	elif(data.startMenuState=='Lobby'):
		nameLabel=data.titleFont.render('Lobby',1,(153,230,255))
		usernameLabel=data.menuFont.render(data.localPlayer.username,1,(153,230,255))
		if(data.localPlayer.team=='yellow'):
			pygame.draw.rect(display,(255,248,0),(data.width*.2,data.height*.35,data.width*.08,40))
		elif(data.localPlayer.team=='blue'):
			pygame.draw.rect(display,(2,2,201),(data.width*.2,data.height*.35,data.width*.08,40))
		elif(data.localPlayer.team=='red'):
			pygame.draw.rect(display,(186,56,56),(data.width*.2,data.height*.35,data.width*.08,40))
		elif(data.localPlayer.team=='green'):
			pygame.draw.rect(display,(0,145,0),(data.width*.2,data.height*.35,data.width*.08,40))
		pygame.draw.rect(display,(39,117,135),(data.width*.2,data.height*.35,data.width*.08,40),3)
		display.blit(usernameLabel,(data.width*.3,data.height*.35))

		i=0
		for user in data.otherUsers:
			i+=1
			usernameLabel=data.menuFont.render(data.otherUsers[user].username,1,(153,230,255))
			if(data.otherUsers[user].team=='yellow'):
				pygame.draw.rect(display,(255,248,0),(data.width*.2,data.height*.35+((data.height*.05+40)*i),data.width*.08,40))
			elif(data.otherUsers[user].team=='blue'):
				pygame.draw.rect(display,(2,2,201),(data.width*.2,data.height*.35+((data.height*.05+40)*i),data.width*.08,40))
			elif(data.otherUsers[user].team=='red'):
				pygame.draw.rect(display,(186,56,56),(data.width*.2,data.height*.35+((data.height*.05+40)*i),data.width*.08,40))
			elif(data.otherUsers[user].team=='green'):
				pygame.draw.rect(display,(0,145,0),(data.width*.2,data.height*.35+((data.height*.05+40)*i),data.width*.08,40))
			pygame.draw.rect(display,(39,117,135),(data.width*.2,data.height*.35+((data.height*.05+40)*i),data.width*.08,40),3)
			display.blit(usernameLabel,(data.width*.3,data.height*.35+((data.height*.05+40)*i)))

		#green team
		pygame.draw.rect(display,(0,145,0),(data.width*.6,data.height*.4,40,40))
		pygame.draw.rect(display,(39,117,135),(data.width*.6,data.height*.4,40,40),3)
		#red team
		pygame.draw.rect(display,(186,56,56),(data.width*.69,data.height*.4,40,40))
		pygame.draw.rect(display,(39,117,135),(data.width*.69,data.height*.4,40,40),3)
		#yellow team
		pygame.draw.rect(display,(255,248,0),(data.width*.6,data.height*.49,40,40))
		pygame.draw.rect(display,(39,117,135),(data.width*.6,data.height*.49,40,40),3)
		#blue team
		pygame.draw.rect(display,(2,2,201),(data.width*.69,data.height*.49,40,40))
		pygame.draw.rect(display,(39,117,135),(data.width*.69,data.height*.49,40,40),3)

		if(data.localPlayer.role=='Host'):
			playLabel=data.menuFont.render('Start Game',1,(153,230,255))
			if(data.playButtonHover):
				pygame.draw.rect(display,(76,76,76),(data.width/2-80,data.height*.8,160,40))
			pygame.draw.rect(display,(153,230,255),(data.width/2-80,data.height*.8,160,40),3)
			display.blit(playLabel,(data.width/2-63,data.height*.8))

	elif(data.startMenuState=='syncMap'):
		nameLabel=data.titleFont.render('Waiting For Host...',1,(153,230,255))

	display.blit(nameLabel,(data.width/2-100,data.height*.15))

def startMenuButtonHover(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			return 2

def startMenuButtonPressed(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 'Singleplayer'
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			return 'Multiplayer'
	return data.startMenuState

def singlePlayerTextBoxSelect(data,pos):
	if(pos[0]>data.width*.41 and pos[0]<data.width*.41+200):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1

def multiplayerTextBoxSelect(data,pos):
	if(pos[0]>data.width*.41 and pos[0]<data.width*.41+200):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1
		if(pos[1]>data.height*.5 and pos[1]<data.height*.5+40):
			return 2

def playButtonHover(data,pos):
	if(pos[0]>data.width/2-80 and pos[0]<data.width/2+80):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return True
	return False

def playButtonPressed(data,pos):
	if(pos[0]>data.width/2-80 and pos[0]<data.width/2+80):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return True
	return False

def multiplayerButtonsHover(data,pos):
	if(pos[0]>data.width*.28 and pos[0]<data.width*.28+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return 1
	if(pos[0]>data.width*.58 and pos[0]<data.width*.58+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return 2

def multiplayerButtonsPressed(data,pos):
	if(pos[0]>data.width*.28 and pos[0]<data.width*.28+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			data.startMenuState='Lobby'
			return 1
	if(pos[0]>data.width*.58 and pos[0]<data.width*.58+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			data.startMenuState='Lobby'
			return 2

def lobbyTeamButtonsPressed(data,pos):
	if(pos[0]>data.width*.6 and pos[0]<data.width*.6+40):
		if(pos[1]>data.height*.4 and pos[1]<data.height*.4+40):
			return 'green'
		elif(pos[1]>data.height*.49 and pos[1]<data.height*.49+40):
			return 'yellow'
	elif(pos[0]>data.width*.69 and pos[0]<data.width*.69+40):
		if(pos[1]>data.height*.4 and pos[1]<data.height*.4+40):
			return 'red'
		elif(pos[1]>data.height*.49 and pos[1]<data.height*.49+40):
			return 'blue'
	return data.localPlayer.team