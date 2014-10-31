#World is like a super level. Woo.

import os
import string
import pygame
import level
import mapobjects

class WorldData:

	def __init__(self):

		self.levels = []
		self.arrivalpoints = {}
		self.currentlevel = 0

	def AddLevelFolder(self,FolderPath):
		
		for filename in os.listdir(FolderPath):
			if filename.endswith('.tmx'):
				self.AddLevel(FolderPath + '/' + filename)


	def SetLevel(self,levelindex):
		self.currentlevel = levelindex

	def AddLevel(self,MapFilePath):

		newlevel = level.LevelData(MapFilePath)

		self.levels.append(newlevel)

		for item in newlevel.MapObjects:
			if isinstance(item, mapobjects.ArrivalPoint):
				if item.identifier in self.arrivalpoints.keys():
					print 'WARNING: DUPLICATE ArrivalPoint'
				else:
					self.arrivalpoints[item.identifier] = self.levels.index(newlevel)


	def ResetLevel(self,levelindex): #Performs a reload of the level from file. Does not alter arrivalpoints
		self.levels[levelindex] = level.LevelData(self.levels[levelindex].MapFilePath)

	def get_current_level(self):
		return self.levels[self.currentlevel]


