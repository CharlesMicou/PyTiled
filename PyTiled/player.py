#Player class

import physics
import pygame
import sprite
import sys
import os
import string
from pygame.locals import *


class PlayerObject(sprite.Sprite, physics.Particle):

	def __init__ (self, ImageFilePath, framecount, framerate, Coordinates):
		sprite.Sprite.__init__(self, ImageFilePath, framecount, framerate)
		physics.Particle.__init__(self, self.currentframe, Coordinates, [0.0, 0.0], [0.0, 0.0], True)
		self.controls = Controls()

	def Refresh(self):
		#More things can go in here as necessary
		self.SetImage(self.currentframe)
		self.ApplyControls()

	def ApplyControls(self):
		self.speed[0] = 2*(int(self.controls.right) - int(self.controls.left))
		self.speed[1] = 2*(int(self.controls.down) - int(self.controls.up))

	def UpdateControls(self, keyevent):

		if keyevent.type == KEYDOWN:
			if keyevent.key == K_UP:
				self.controls.up = True
			if keyevent.key == K_DOWN:
				self.controls.down = True
			if keyevent.key == K_LEFT:
				self.controls.left = True
			if keyevent.key == K_RIGHT:
				self.controls.right = True

		elif keyevent.type == KEYUP:
			if keyevent.key == K_UP:
				self.controls.up = False
			if keyevent.key == K_DOWN:
				self.controls.down = False
			if keyevent.key == K_LEFT:
				self.controls.left = False
			if keyevent.key == K_RIGHT:
				self.controls.right = False


	def CollisionCheck(self, MapObjects, CollisionMap):
	
		#Check for environment collision	
		self.EnvironmentCollisionCheck(MapObjects,CollisionMap)

		#Check for collisions with other particles
		futureself = physics.Particle(self.currentframe, self.coordinates, self.speed, self.acceleration, True)
		futureself.tick()	
		collideables = []
		for item in MapObjects:
			if isinstance(item, physics.Particle) and (item != self) and (item != futureself):
				if item.collision == True:				
					collideables.append(item)	
		colliderlist = []
		for particle in collideables:
			colliderlist.append(particle.rect)	
		collisionindex = futureself.rect.collidelist(colliderlist)
		if collisionindex != -1:
			physics.TwoParticleBounce(self, collideables[collisionindex])


		




	def EnvironmentCollisionCheck(self, MapObjects, CollisionMap):

		#We only need to bother with this if we're trying to go anywhere
		if self.speed[0] == 0 and self.speed[1] == 0: return

		futureself = physics.Particle(self.currentframe, self.coordinates, self.speed, self.acceleration, True)
		futureself.tick()	

		for item in CollisionMap:
			if futureself.rect.colliderect(item):
					if (abs(futureself.rect.centerx - item.centerx) > abs(futureself.rect.centery - item.centery)):
						#horizontal collision
						self.speed[0] = 0.0

					elif (abs(futureself.rect.centerx - item.centerx) < abs(futureself.rect.centery - item.centery)):
						#vertical collision
						self.speed[1] = 0.0

					else:
						#diagonal collision
						self.speed[0] = 0.0
						self.speed[1] = 0.0


class Controls:
	def __init__(self):
		self.up = False
		self.down = False
		self.left = False
		self.right = False

