#Physics, woo!


import string
import pygame
import level
import math
import world
import tiledparser as tiled
import copy
import texthandler
import player
import mapobjects

def Update(WorldData, PlayerObject):


	CurrentLevel = WorldData.get_current_level()

	player.ApplyPlayerActions(CurrentLevel, PlayerObject)

	ObjectState = copy.copy(CurrentLevel.MapObjects) #Note: This *needs* to be a shallow copy

	for item in ObjectState:

		#Particle collisions
		if isinstance(item, mapobjects.Particle):

			if not item.rect.colliderect(CurrentLevel.bounds): #Remove any objects that have left the screen
				CurrentLevel.MapObjects.remove(item)

			if item.collision == True:
				item.CollisionCheck(ObjectState, CurrentLevel.CollisionMap)

		#Teleporters
		if isinstance(item, mapobjects.Displacer):
			if item.rect.colliderect(PlayerObject.rect):
				if item.destination in WorldData.arrivalpoints.keys():

					if WorldData.arrivalpoints[item.destination] != WorldData.currentlevel:
						#need to jump to another map
						CurrentLevel.MapObjects.remove(PlayerObject)
						WorldData.SetLevel(WorldData.arrivalpoints[item.destination])

						for testarrivalpoint in WorldData.get_current_level().MapObjects:
							if isinstance(testarrivalpoint, mapobjects.ArrivalPoint):
								if testarrivalpoint.identifier == item.destination:

									PlayerObject.SetCoords([testarrivalpoint.rect.centerx - PlayerObject.rect.width/2, testarrivalpoint.rect.centery - PlayerObject.rect.height/2])
									WorldData.get_current_level().AddObject(PlayerObject)
									return


					else: #destination is on the same map, no need to reload things
						for testarrivalpoint in WorldData.get_current_level().MapObjects:
							if isinstance(testarrivalpoint, mapobjects.ArrivalPoint):
								if testarrivalpoint.identifier == item.destination:
									PlayerObject.SetCoords([testarrivalpoint.rect.centerx - PlayerObject.rect.width/2, testarrivalpoint.rect.centery - PlayerObject.rect.height/2])
								



	#Update everything in one go
	for item in CurrentLevel.MapObjects:
		if isinstance(item, mapobjects.Particle):
			item.tick()

	#Make sure player is updated
	PlayerObject.Refresh()

	return 0

