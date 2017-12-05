import pygame
import rts_images

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
		if(data.startMenuSelect==3):
			pygame.draw.rect(display,(76,76,76),(data.width/2-100,data.height*.51,200,40))	
		pygame.draw.rect(display,(153,230,255),(data.width/2-100,data.height*.51,200,40),3)
		instructionsLabel=data.menuFont.render('Instructions',1,(153,230,255))
		display.blit(instructionsLabel,(data.width/2-60,data.height*.51))

	elif(data.startMenuState=='Instructions'):
		if(data.backButtonHover):
			pygame.draw.rect(display,(76,76,76),(30,30,35,35))
		data.backButton.draw(display)
		nameLabel=data.titleFont.render('Instructions',1,(153,230,255))
		data.instructions.draw(display)
		data.instructionScollers.draw(display)

	elif(data.startMenuState=='Singleplayer'):
		if(data.backButtonHover):
			pygame.draw.rect(display,(76,76,76),(30,30,35,35))
		data.backButton.draw(display)
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
		if(data.backButtonHover):
			pygame.draw.rect(display,(76,76,76),(30,30,35,35))
		data.backButton.draw(display)
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

		if(data.invalidIP):
			errorLabel=data.menuFont.render('Invalid IP',1,(255,0,0))
			display.blit(errorLabel,(data.width*.4,data.height*.6))

		joinLabel=data.menuFont.render('Join',1,(153,230,255))
		if(data.multiplayerButtonHover==1):
			pygame.draw.rect(display,(76,76,76),(data.width*.42,data.height*.8,100,40))
		pygame.draw.rect(display,(153,230,255),(data.width*.42,data.height*.8,100,40),3)
		display.blit(joinLabel,(data.width*.46,data.height*.8))

	elif(data.startMenuState=='Lobby'):
		data.hostIcon.empty()
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
		if(data.localPlayer.role=='Host'):
			data.hostIcon.add(rts_images.HostIcon(data.width*.2+1.5,data.height*.35+1.5))
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
			if(data.otherUsers[user].role=='Host'):
				data.hostIcon.add(rts_images.HostIcon(data.width*.2,data.height*.35+((data.height*.05+40)*i)))
			display.blit(usernameLabel,(data.width*.3,data.height*.35+((data.height*.05+40)*i)))

		data.hostIcon.draw(display)

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

	elif(data.startMenuState=='syncTime'):
		nameLabel=data.titleFont.render('Waiting For Other Players...',1,(153,230,255))

	if(data.startMenuState=='syncTime'):
		display.blit(nameLabel,(data.width*.2,data.height*.1))
	elif(data.startMenuState!='Instructions'):
		display.blit(nameLabel,(data.width/2-100,data.height*.15))
	else:
		display.blit(nameLabel,(data.width/2-100,data.height*.1))

def startMenuButtonHover(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			return 2
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.5 and pos[1]<data.height*.5+40):
			return 3

def startMenuButtonPressed(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			data.startMenuSelect=None
			return 'Singleplayer'
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			data.startMenuSelect=None
			return 'Multiplayer'
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.5 and pos[1]<data.height*.5+40):
			return 'Instructions'
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
	if(pos[0]>data.width*.42 and pos[0]<data.width*.42+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return 1

def multiplayerButtonsPressed(data,pos):
	if(pos[0]>data.width*.42 and pos[0]<data.width*.42+100):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			data.startMenuState='Lobby'
			return 1

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

def instructionPageFlip(data,pos):
	instructions=data.instructions.sprite
	if(pos[1]>data.height*.9 and pos[1]<data.height*.9+35):
		if(pos[0]>20 and pos[0]<55):
			if(instructions.page==1):
				instructions.changePage(4)
			elif(instructions.page==2):
				instructions.changePage(1)
			elif(instructions.page==3):
				instructions.changePage(2)
			elif(instructions.page==4):
				instructions.changePage(3)
		elif(pos[0]>data.width-55 and pos[0]<data.width-20):
			if(instructions.page==1):
				instructions.changePage(2)
			elif(instructions.page==2):
				instructions.changePage(3)
			elif(instructions.page==3):
				instructions.changePage(4)
			elif(instructions.page==4):
				instructions.changePage(1)