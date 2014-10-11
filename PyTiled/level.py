#Level functions and class 
import os
import string
import tiledparser as tiled
import sys
import pygame
import physics


class LevelData:

	def __init__(self, MapFilePath):

		self.MapData = tiled.MapData(MapFilePath)
		self.MapObjects = self.MapData.mapobjects
		self.CollisionMap = tiled.GetCollisionRects(self.MapData)
		self.backgroundimage = tiled.CreateBackground(self.MapData)
		self.bounds = pygame.Rect(0 , 0 , self.MapData.width*self.MapData.tilewidth, self.MapData.height*self.MapData.tileheight)


	def AddObject(self, item):
		self.MapObjects.append(item)
		
		
