~~Second Earth: README~~
#######Install#########
Unpack ZIP files together. All files are housed in 'RTS' Folder
Libraries: pygame, sockets, threading, ast, os, subprocess
Import instructions:
-Pygame: in the command prompt enter "py pip install -m pygame" run a test document
with the line of code "import pygame" to test.
-All other libraries should be included in python. No additional work required

######Description#######
Second Earth is a real time strategy game. The objective is to either wipe all other
players off the map or to build the end game structure: The Warp Beacon. The player
starts with a drone and then builds a settlement by collecting resources from mines
and trees. The strategy comes from being able to control a mass of units and
structures as well as being able to micromanage an entire settlement.

#######Playing the Game######
Running Singleplayer:
run rts_main.py
Press Singleplayer and enter username
Press Start Game
[WARNING]Game can take a little while to load to due quantity of sprites.
DO NOT FORCE CLOSE even if "program is not responding"
Enjoy

Running Multiplayer:
Step 1. Obtain public IP address
Step 2. run rts_server.py on the computer hosting the game. 
The terminal should read "Looking for Connection"
Step 3. run rts_main.py on all computers playing the game
Step 4. Press Multiplayer and enter username and IP.
Step 5. First person to connect must press Start Game once all players are ready
Step 6. Person who pressed Start Game will load game
[WARNING]Game can take a little while to load to due quantity of sprites.
DO NOT FORCE CLOSE even if "program is not responding"
Other users will then receive the information and load it themselves
[WARNING]Game can take a little while to load to due quantity of sprites.
DO NOT FORCE CLOSE even if "program is not responding"
Step 7. After game has concluded Host must force close the server to disconnect
socket connections