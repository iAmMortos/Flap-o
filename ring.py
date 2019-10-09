from scene import *
import random



class Ring (SpriteNode):
	def __init__(self, size):
		SpriteNode.__init__(self, 'rsc/ring.png')
		sw,sh = size
		w,h = 48,48
		self.size = (w,h)
		self.position = (sw+w/2,random.randint(0,sh-h)+h/2)
		
	def update(self, speed):
		x,y = self.position
		self.position = (x-speed, y)
		
	def get_hitbox(self):
		s = 32
		x,y = self.position
		return Rect(x-s/2,y-s/2,s,s)
