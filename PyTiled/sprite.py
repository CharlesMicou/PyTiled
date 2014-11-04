
import pygame

class Sprite:
	def __init__(self, ImageFilePath, framecount, framerate):

		baseimage = pygame.image.load(ImageFilePath).convert_alpha()
		self.framecount = framecount
		self.framerate = framerate
		self.frames = []
		self.framenumber = 0
		self.bufferframes = 0
		self.pause = False

		n = 0
		while(n < framecount):
			croparea = pygame.Rect(n*baseimage.get_rect().width / framecount, 0, baseimage.get_rect().width / framecount, baseimage.get_rect().height)	
			cropsurf = pygame.Surface([baseimage.get_rect().width / framecount, baseimage.get_rect().height], pygame.SRCALPHA, 32).convert_alpha()
			cropsurf.blit(baseimage, (0,0), croparea)
			self.frames.append(cropsurf)
			n += 1

		self.currentframe = self.frames[self.framenumber]


	def SetFrame(self, framenumber):
		self.currentframe = self.frames[framenumber]

	def Advance(self):

		if self.pause: return

		if self.framerate == 0: 
			return

		self.bufferframes += 1

		if self.bufferframes > self.framerate:
			self.framenumber += 1
			if self.framenumber > self.framecount - 1: 
				self.framenumber = 0
			self.SetFrame(self.framenumber)
			self.bufferframes = 0


