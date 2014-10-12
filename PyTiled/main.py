#PyTiled game engine

import os
import string
import sys
import pygame
import physics
import level
import renderer
import player
from pygame.locals import *


#Set up engine
pygame.init()
fpsClock = pygame.time.Clock()
fpsMax = 60

#Set up screen as defined in renderer.py (todo: write a screen-settings file)
screen = renderer.init()

#Load a level
atestlevel = level.LevelData('Resources/Maps/AnotherMap.tmx')

#Add the player to the level
ourplayer = player.PlayerObject('Resources/Images/playersprite.png', 3, 40, [400, 70])
atestlevel.AddObject(ourplayer)


#Game Loop
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif (event.type == KEYDOWN) or (event.type == KEYUP):
			ourplayer.UpdateControls(event)
		elif (event.type == MOUSEBUTTONDOWN) or (event.type == MOUSEBUTTONUP):
			ourplayer.UpdateControls(event)

		

	#Update the physics simulation
	player.ApplyPlayerActions(atestlevel, ourplayer)
	physics.Update(atestlevel.MapObjects, atestlevel.CollisionMap, atestlevel.bounds)

	#Update any player information
	ourplayer.Refresh()

	#Update any sprites
	renderer.UpdateSprites(atestlevel)	

	#Update the screen
	renderer.RenderScreen(screen, atestlevel, ourplayer, 'followplayer')

	#Enforce the framerate
	fpsClock.tick(fpsMax)





"""
==================
TODO LIST

Renderer Module:
Textqueue

Collisions:

TileMap Module:
Map-Linking



==================
KNOWN ISSUES:

libpng is crap

"""