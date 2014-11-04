#Renderer

import os
import string
import sys
import pygame
import sprite
import level
import player
import math
import texthandler
import mapobjects
#import numpy as np

color_black = 0, 0, 0
color_white = 255, 255, 255

cursor_image = pygame.image.load("Resources/Images/cursorsprite.png")
cursor_rect = cursor_image.get_rect()


def init():
	
	#Set screen size, properties
	screensize = width, height = 1024, 768
	#screensize = width, height = 800, 600
	titleicon = pygame.image.load('Resources/Images/baricon.gif')
	pygame.display.set_icon(titleicon)
	screen = pygame.display.set_mode(screensize)
	pygame.display.set_caption('PyTiled Engine')
	
	#Font definition
	global afont 
	afont = pygame.font.Font(None, 20)

	#Cursor definition
	empty_cursor = (            #sized 24x24
        "                        ",
        "                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",)

	datatuple, masktuple = pygame.cursors.compile( empty_cursor,
                                  black='.', white='X', xor='o' )
	pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )

	#pygame.mouse.set_cursor(*pygame.cursors.broken_x)

	return screen


def UpdateSprites(LevelData):

	for item in LevelData.MapObjects:
		 if isinstance(item, sprite.Sprite):
		 	item.Advance()



def RenderScreen(screen, LevelData,  PlayerData, RenderMode):

	offset = [0,0]

	screensize = screen.get_size()

	if RenderMode == 'centered':
		offset[0] = (screensize[0] - LevelData.MapData.width*LevelData.MapData.tilewidth)/2
		offset[1] = (screensize[1] - LevelData.MapData.height*LevelData.MapData.tileheight)/2


	elif RenderMode == 'followplayer':
		for item in LevelData.MapObjects:
			if isinstance(item, player.PlayerObject):
				offset[0] = - (item.rect.left + item.rect.width/2 - screensize[0]/2)
				offset[1] = - (item.rect.top + item.rect.height/2 - screensize[1]/2)

				#Lock camera to corners
				if offset[0] > 0:
					offset[0] = 0
				if offset[1] > 0:
					offset[1] = 0
				if offset[0] - screensize[0] < - LevelData.MapData.width*LevelData.MapData.tilewidth:
					offset[0] =  -LevelData.MapData.width*LevelData.MapData.tilewidth + screensize[0]
				if offset[1] - screensize[1] < - LevelData.MapData.height*LevelData.MapData.tileheight:
					offset[1] =  -LevelData.MapData.height*LevelData.MapData.tileheight + screensize[1]

				#Correct for tiny maps
				if screensize[0] >  LevelData.MapData.width*LevelData.MapData.tilewidth:
					offset[0] = (screensize[0] - LevelData.MapData.width*LevelData.MapData.tilewidth)/2
				if screensize[1] > LevelData.MapData.height*LevelData.MapData.tileheight:
					offset[1] = (screensize[1] - LevelData.MapData.height*LevelData.MapData.tileheight)/2



	screen.fill(color_black)


	screen.blit(LevelData.backgroundimage, LevelData.bounds.move(offset))

	#Render everything except the player
	for item in LevelData.MapObjects:
		if isinstance(item, mapobjects.Particle):
			if not isinstance(item, player.PlayerObject):
				screen.blit(item.image, item.rect.move(offset))


	#Apply vfx
	"""blurstrength = 15
	speed = math.sqrt(PlayerData.speed[0]**2 + PlayerData.speed[1]**2)
	if speed != 0 and speed > 1:
		blurstrength = int(15*(PlayerData.maxspeed - speed))
	if blurstrength != 0:
		screen.blit(blurvfx(screen,1000,5,blurstrength),pygame.Rect((0,0), screensize))"""

	#Handle cursor position and set it as a player control
	cursor_location = pygame.Rect((pygame.mouse.get_pos()[0] + cursor_rect.width/2, pygame.mouse.get_pos()[1] + cursor_rect.height/2), (cursor_rect.width, cursor_rect.height))
	screen.blit(cursor_image, cursor_location)

	for item in LevelData.MapObjects:
		if isinstance(item, player.PlayerObject):
			#Set the cursor
			item.controls.setCursor([cursor_location.left + cursor_rect.width/2 - offset[0], cursor_location.top  + cursor_rect.height/2 - offset[1]])
			#Draw the player
			screen.blit(item.image, item.rect.move(offset))


	#Handle onscreen text rendering
	if texthandler.textqueue.text != []:
		textsurf = afont.render(texthandler.textqueue.pop_fifo(), True, color_white)
		screen.blit(textsurf, pygame.Rect((5,5), (100,20)))

	#Update the screen
	pygame.display.flip()


"""def blurvfx(surf, blurcount, blurstrength, blursize):

	finalsurf = surf
	i = 0
	n = 10000

	while i < blurcount:
		croprect = pygame.Rect(np.random.randint(0,surf.get_width()-blursize),np.random.randint(0,surf.get_height()-blursize),
		 			blursize , blursize)

		offset = [blurstrength*np.random.randint(-blurstrength,blurstrength),blurstrength*np.random.randint(-blurstrength,blurstrength)]

		finalsurf.blit(surf, (croprect.left,croprect.top), croprect.move(offset))



		i += 1

	return finalsurf"""
