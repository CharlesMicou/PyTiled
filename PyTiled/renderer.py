#Renderer

import os
import string
import sys
import pygame
import sprite
import level
import player

color_black = 0, 0, 0

cursor_image = pygame.image.load("Resources/Images/cursorsprite.png")
cursor_rect = cursor_image.get_rect()

def UpdateSprites(LevelData):

	for item in LevelData.MapObjects:
		 if isinstance(item, sprite.Sprite):
		 	item.Advance()


def RenderScreen(screen, LevelData, RenderMode):

	offset = [0,0]

	screensize = screen.get_size()

	if RenderMode == 'centered':
		offset[0] = (screensize[0] - LevelData.MapData.width*LevelData.MapData.tilewidth)/2
		offset[1] = (screensize[1] - LevelData.MapData.height*LevelData.MapData.tileheight)/2


	if RenderMode == 'followplayer':
		for item in LevelData.MapObjects:
			if isinstance(item, player.PlayerObject):
				offset[0] = - (item.rect.left + item.rect.width/2 - screensize[0]/2)
				offset[1] = - (item.rect.top + item.rect.height/2 - screensize[1]/2)


				if offset[0] > 0:
					offset[0] = 0
				if offset[1] > 0:
					offset[1] = 0
				if offset[0] - screensize[0] < - LevelData.MapData.width*LevelData.MapData.tilewidth:
					offset[0] =  -LevelData.MapData.width*LevelData.MapData.tilewidth + screensize[0]
				if offset[1] - screensize[1] < - LevelData.MapData.height*LevelData.MapData.tileheight:
					offset[1] =  -LevelData.MapData.height*LevelData.MapData.tileheight + screensize[1]


	screen.fill(color_black)


	screen.blit(LevelData.backgroundimage, LevelData.bounds.move(offset))

	for item in LevelData.MapObjects:
		screen.blit(item.image, item.rect.move(offset))


	#Handle cursor position and set it as a player control
	cursor_location = pygame.Rect((pygame.mouse.get_pos()[0] + cursor_rect.width/2, pygame.mouse.get_pos()[1] + cursor_rect.height/2), (cursor_rect.width, cursor_rect.height))
	screen.blit(cursor_image, cursor_location)

	for item in LevelData.MapObjects:
		if isinstance(item, player.PlayerObject):
			item.controls.setCursor([cursor_location.left + cursor_rect.width/2 - offset[0], cursor_location.top  + cursor_rect.height/2 - offset[1]])
			


	pygame.display.flip()

def init():
	#screensize = width, height = 1024, 768
	screensize = width, height = 800, 600
	titleicon = pygame.image.load('Resources/Images/baricon.gif')
	pygame.display.set_icon(titleicon)
	screen = pygame.display.set_mode(screensize)
	pygame.display.set_caption('PyTiled Engine')


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
