from scene import *
import math



class DeathRing (SpriteNode):
	def __init__(self, pos, dir, **kwargs):
		SpriteNode.__init__(self, 'rsc/ring.png', **kwargs)
		speed = 4
		init_up = 4
		self.position = pos
		self.size = (32,32)
		self.x_vel = math.cos(dir) * speed
		self.y_vel = init_up + math.sin(dir) * speed
		self.grav = 0.1
	
	def update(self):
		self.y_vel -= self.grav
		x,y = self.position
		self.position = (x+self.x_vel, y+self.y_vel)
		w,h = self.size
		sw,sh = self.scene.size
		if x < w/2:
			self.x_vel *= -1
			self.position = (w/2,y)
		elif x > sw - w/2:
			self.x_vel *= -1
			self.position = (sw - w/2, y)
		if y > sh - h/2:
			self.y_vel = 0
			self.position = (x, sh - h/2)
