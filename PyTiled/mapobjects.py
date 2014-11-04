#MapObjects class: For objects on the map


import string
import pygame
#import level
import sprite
#import math
#import tiledparser as tiled
import physicstools
import texthandler

class Particle:

	def __init__(self, Image, Coordinates, Speed, Acceleration, collision):

		self.image = Image
		self.rect = pygame.Rect(int(Coordinates[0]), int(Coordinates[1]), 
			self.image.get_rect().width, self.image.get_rect().height)

		self.speed = [float(Speed[0]), float(Speed[1])]
		self.acceleration = [float(Acceleration[0]), float(Acceleration[1])]
		self.coordinates = [float(Coordinates[0]), float(Coordinates[1])]
		self.collision = collision

	def AlignToGrid(self):
		self.rect = pygame.Rect(int(self.coordinates[0]), int(self.coordinates[1]), 
			self.image.get_rect().width, self.image.get_rect().height)


	def SetCoords(self, Coordinates):
		self.coordinates = [Coordinates[0], Coordinates[1]]
		self.AlignToGrid()

	def tick(self):
		self.coordinates = [self.coordinates[0] + self.speed[0], self.coordinates[1] + self.speed[1]]
		self.speed = [self.speed[0] + self.acceleration[0], self.speed[1] + self.acceleration[1]]
		self.AlignToGrid()

	def SetImage(self, Image):
		self.image = Image
		self.AlignToGrid()


class Bouncer(Particle):
	def __init__ (self, Image, Coordinates, Speed, Acceleration, Bounciness):
		Particle.__init__(self, Image, Coordinates, Speed, Acceleration, True)
		self.bounciness = Bounciness

	def CollisionCheck(self, MapObjects, CollisionMap):

		futureself = Bouncer(self.image, self.coordinates, self.speed, self.acceleration, self.bounciness)
		futureself.tick()

		#Check for collisions with the environment
		collisionindex = futureself.rect.collidelist(CollisionMap)
		if collisionindex != -1:
			if (abs(self.rect.centerx - CollisionMap[collisionindex].centerx) > abs(self.rect.centery - CollisionMap[collisionindex].centery)):
				#horizontal collision
				self.speed[0] = -self.speed[0]*self.bounciness

			elif (abs(self.rect.centerx - CollisionMap[collisionindex].centerx) < abs(self.rect.centery - CollisionMap[collisionindex].centery)):
				#vertical collision
				self.speed[1] = -self.speed[1]*self.bounciness

			else:
				#diagonal collision
				self.speed[0] = -self.speed[0]
				self.speed[1] = -self.speed[1]
	

		#Check for collisions with other particles
		collideables = []
		for item in MapObjects:
			if isinstance(item, Particle) and (item != self) and (item != futureself):
				if item.collision == True:				
					collideables.append(item)

		colliderlist = []
		for particle in collideables:
			colliderlist.append(particle.rect)

		collisionindex = futureself.rect.collidelist(colliderlist)
		if collisionindex != -1:
			physicstools.TwoParticleBounce(self, collideables[collisionindex])


class Displacer:
	def __init__(self, left, top, width, height, destination):
		self.rect = pygame.Rect(left, top, width, height)
		self.destination = destination

class ArrivalPoint:
	def __init__(self, left, top, width, height, identifier):
		self.rect = pygame.Rect(left, top, width, height)
		self.identifier = identifier

