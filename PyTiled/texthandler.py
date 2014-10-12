#Textqueueing

import string

class TextQueue:

	def __init__(self):

		self.text = []

	def add(self,textstring):

		if "\n" in textstring:
			self.text.append(textstring.partition("\n")[0])
			self.text.append(self.add(textstring.partition("\n")[2]))

		else:
			self.text.append(textstring)

	def get_fifo(self):
		return self.text[0]

	def pop_fifo(self):
		return self.text.pop(0)

	def remove_fifo(self):
		self.text.pop(0)


textqueue = TextQueue()