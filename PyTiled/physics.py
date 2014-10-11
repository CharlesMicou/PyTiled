#Physics, woo!


import string
import pygame
import level
import math
import tiledparser as tiled
import copy

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

	def tick(self):
		self.coordinates = [self.coordinates[0] + self.speed[0], self.coordinates[1] + self.speed[1]]
		self.speed = [self.speed[0] + self.acceleration[0], self.speed[1] + self.acceleration[1]]
		self.AlignToGrid()

	def SetImage(self, Image):
		self.image = Image


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
			TwoParticleBounce(self, collideables[collisionindex])

		




def Update(MapObjects, CollisionMap, bounds):

	ObjectState = copy.copy(MapObjects) #Note: This *needs* to be a shallow copy

	for item in ObjectState:

		if isinstance(item, Particle):

			if not item.rect.colliderect(bounds):
				MapObjects.remove(item)

			if item.collision == True:
				item.CollisionCheck(ObjectState, CollisionMap)

	#Update everything in one go
	for item in MapObjects:
		if isinstance(item, Particle):
			item.tick()


def TwoParticleBounce(a, b):

	#Establish normalised vector for plane of collision
	line = [float(b.rect.centerx - a.rect.centerx), float(b.rect.centery - a.rect.centery)]
	modulus = math.sqrt(line[0]*line[0] + line[1]*line[1])
	if modulus == 0:
		return

	line = [line[0]/modulus, line[1]/modulus]
	normal = [line[1], -line[0]]

	#Establish normalised direction of motion
	modulus = math.sqrt(a.speed[0]*a.speed[0] + a.speed[1]*a.speed[1])
	if modulus == 0:
		return
	direction = [a.speed[0]/modulus, a.speed[1]/modulus]

	#Find out how fast we're going in each direction
	linespeed = DotProduct2D(a.speed, line)
	normalspeed = DotProduct2D(a.speed, normal)

	#Flip the linespeed
	linespeed = -linespeed

	#Go back to original coordinate system
	a.speed[0] = linespeed*DotProduct2D([1,0], line) + normalspeed*DotProduct2D([1,0], normal)
	a.speed[1] = linespeed*DotProduct2D([0,1], line) + normalspeed*DotProduct2D([0,1], normal)


def DotProduct2D(a, b):
	return a[0]*b[0] + a[1]*b[1]

