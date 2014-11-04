#PyTiled game engine

import os
import string
import sys
import pygame
import physics
import level
import renderer
import player
import world
from pygame.locals import *


#Set up engine
pygame.init()
fpsClock = pygame.time.Clock()
fpsMax = 60

#Set up screen as defined in renderer.pydd (todo: write a screen-settings file)
screen = renderer.init()

#Load a world
atestworld = world.WorldData()
atestworld.AddLevelFolder('Resources/Maps')

#Add the player to the level
ourplayer = player.PlayerObject('Resources/Images/playersprite.png', 3, 30, [400, 70])
atestworld.get_current_level().AddObject(ourplayer)


#Game Loop
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif (event.type == KEYDOWN) or (event.type == KEYUP):
			ourplayer.UpdateControls(event)
		elif (event.type == MOUSEBUTTONDOWN) or (event.type == MOUSEBUTTONUP):
			ourplayer.UpdateControls(event)


	#Update the physics simulation
	PhysicsExitCode = physics.Update(atestworld, ourplayer)
 
	ourplayer.Refresh()

	#Update any sprites
	renderer.UpdateSprites(atestworld.get_current_level())	

	#Update the screen
	renderer.RenderScreen(screen, atestworld.get_current_level(), ourplayer, 'followplayer')

	#Enforce the framerate
	fpsClock.tick(fpsMax)





"""
==================
TODO LIST

Texthandler:
Fix the really bad queue system

Renderer Module:

Collisions:

TileMap Module:




==================
KNOWN ISSUES:

libpng is crap

"""