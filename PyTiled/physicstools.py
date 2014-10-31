#physics calculations

import pygame
import math

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