#Tiled Parser

import os
import sys
import pygame
import string
import mapobjects
import xml.etree.ElementTree as ET


class MapData:

	def __init__(self, MapFilePath):
		sets = []
		tilelayers = []
		self.mapdir = MapFilePath.rpartition('/')[0]
		
		tree = ET.parse(MapFilePath)
		root = tree.getroot()

		self.height, self.width = int(root.attrib['height']), int(root.attrib['width'])
		self.tileheight, self.tilewidth = int(root.attrib['tileheight']), int(root.attrib['tilewidth'])

		self.mapobjects = []

		for child in root:
			
			if 'tileset' in child.tag:	
				sets.append(TileSet(self.mapdir + '/' + child.attrib['source']))

			if 'layer' in child.tag:
				raw = []
				newlayer = []
				for data in child:
					for tiles in data:
						raw.append(int(tiles.attrib['gid']))
				for n in range(0, self.height):
					newlayer.append(raw[ n*self.width : (n+1)*self.width ])

				tilelayers.append(newlayer)


			if 'objectgroup' in child.tag:

				coordinates = []
				imagepath = 'default'

				for data in child:
					
					if 'type' in data.attrib:

						if 'particle' in data.attrib['type']:

							imagepath = 'default'
							speed = [0,0]
							acceleration = [0,0]
							collision = False
							coordinates = [int(data.attrib['x']), int(data.attrib['y'])] 

							for xmlwrapper in data:
								for propertyitem in xmlwrapper:
									
									if 'imagepath' in propertyitem.attrib['name']:
										imagepath = propertyitem.attrib['value']

									if 'speed' in propertyitem.attrib['name']:
										speed[0] = float(propertyitem.attrib['value'].partition(',')[0])
										speed[1] = float(propertyitem.attrib['value'].partition(',')[2])

									if 'acceleration' in propertyitem.attrib['name']:
										acceleration[0] = float(propertyitem.attrib['value'].partition(',')[0])
										acceleration[1] = float(propertyitem.attrib['value'].partition(',')[2])

									if 'collision' in propertyitem.attrib['name']:
										collision = bool(propertyitem.attrib['value'])

							if collision:
								self.mapobjects.append(mapobjects.Bouncer(pygame.image.load(imagepath), coordinates, speed, acceleration, collision))
							else:
								self.mapobjects.append(mapobjects.Particle(pygame.image.load(imagepath), coordinates, speed, acceleration, collision))

						if 'bouncer' in data.attrib['type']:

							imagepath = 'default'
							speed = [0,0]
							acceleration = [0,0]
							coordinates = [int(data.attrib['x']), int(data.attrib['y'])] 

							for xmlwrapper in data:
								for propertyitem in xmlwrapper:
									
									if 'imagepath' in propertyitem.attrib['name']:
										imagepath = propertyitem.attrib['value']

									if 'speed' in propertyitem.attrib['name']:
										speed[0] = float(propertyitem.attrib['value'].partition(',')[0])
										speed[1] = float(propertyitem.attrib['value'].partition(',')[2])

									if 'acceleration' in propertyitem.attrib['name']:
										acceleration[0] = float(propertyitem.attrib['value'].partition(',')[0])
										acceleration[1] = float(propertyitem.attrib['value'].partition(',')[2])

									if 'bounciness' in propertyitem.attrib['name']:
										bounciness = float(propertyitem.attrib['value'])

							
							self.mapobjects.append(mapobjects.Bouncer(pygame.image.load(imagepath), coordinates, speed, acceleration, bounciness))


						if 'displacer' in data.attrib['type']:

							coordinates = int(data.attrib['x']), int(data.attrib['y'])
							dimensions = int(data.attrib['width']), int(data.attrib['height'])
							destination = 'null'

							for xmlwrapper in data:
								for propertyitem in xmlwrapper:
									if 'destination' in propertyitem.attrib['name']:
										destination = propertyitem.attrib['value']

							self.mapobjects.append(mapobjects.Displacer(coordinates[0], coordinates[1], dimensions[0], dimensions[1], destination))
							

						if 'arrivalpoint' in data.attrib['type']:

							coordinates = int(data.attrib['x']), int(data.attrib['y'])
							dimensions = int(data.attrib['width']), int(data.attrib['height'])
							identifier = 'null'

							for xmlwrapper in data:
								for propertyitem in xmlwrapper:
									if 'id' in propertyitem.attrib['name']:
										identifier = propertyitem.attrib['value']

							self.mapobjects.append(mapobjects.ArrivalPoint(coordinates[0], coordinates[1], dimensions[0], dimensions[1], identifier))


					else:
						print "WARNING: invalid object in " + MapFilePath
						#mapobjects.append(physics.particle())


		self.tilesets = sets
		self.layers = tilelayers



class TileSet:

	def __init__(self, TileSetPath):
		fin = open(TileSetPath)

		for line in fin:
			if 'tileset name' in line:
				self.name = line[line.find('tileset name'):].partition('\"')[2].partition('\"')[0]
				self.tilewidth = int(line[line.find('tilewidth'):].partition('\"')[2].partition('\"')[0])
				self.tileheight =  int(line[line.find('tileheight'):].partition('\"')[2].partition('\"')[0])

			elif 'image source' in line:
				self.imagepath = TileSetPath.rpartition('/')[0] + '/' + line[line.find('image source'):].partition('\"')[2].partition('\"')[0]
				self.width = int(line[line.find('width'):].partition('\"')[2].partition('\"')[0])
				self.height = int(line[line.find('height'):].partition('\"')[2].partition('\"')[0])
				self.tilecount = (self.width / self.tilewidth) * (self.height / self.tileheight)

		fin.close()


def CreateBackground(Map):


	Background = pygame.Surface([Map.width*Map.tilewidth, Map.height*Map.tileheight])

	TileImages = ['null']

	for TileSet in Map.tilesets:
		baseimage = pygame.image.load(TileSet.imagepath)
		row = 0
		while row < (TileSet.height / TileSet.tileheight):
			col = 0
			while col < (TileSet.width / TileSet.tilewidth):
				
				croparea = pygame.Rect(col*TileSet.tilewidth, row*TileSet.tileheight, TileSet.tilewidth, TileSet.tileheight)
				cropsurf = pygame.Surface([TileSet.tilewidth, TileSet.tileheight])

				cropsurf.blit(baseimage, (0,0) ,croparea)
				TileImages.append(cropsurf)

				col += 1


			row += 1


	row = 0
	for line in Map.layers[0]:
		col = 0
		for tile in line:
			if tile != 0:
				Background.blit(TileImages[tile], [col*Map.tilewidth, row*Map.tileheight])
			col += 1

		row += 1


	return Background


def GetCollisionRects(Map):

	CollisionRects = []


	row = 0
	for line in Map.layers[1]:
		col = 0
		for tile in line:
			if tile != 0:
				CollisionRects.append(pygame.Rect(col*Map.tilewidth, row*Map.tileheight, Map.tilewidth, Map.tileheight))
			col += 1

		row += 1

	return CollisionRects

