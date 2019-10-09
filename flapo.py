from scene import SpriteNode, Rect, Action as A
import sound
import random
import math



class Flapo (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'rsc/hedgehog.png', **kwargs)
		self.size = (70,70)
		self.color = '#337aff'
		self.dead = False
		self.death_flash_frames = 4
		self.cur_dff = 0
		self.x_scale = -1
		self.gravity = .25
		self.y_vel = 0
		self.x_vel = 0
		self.y_vel_max_up = 12
		self.y_vel_max_down = 15
		self.flap_speed = 6
		
		self.reset()
		
	def update(self):
		x,y = self.position
		w,h = self.size
		sw,sh = self.scene.size
		self.y_vel -= self.gravity
		self.y_vel = min(self.y_vel, self.y_vel_max_up)
		self.y_vel = max(self.y_vel, self.y_vel_max_down * -1)
		self.position = (x + self.x_vel, y + self.y_vel)
		
		if y > sh:
			self.position = (x, sh)
			self.y_vel = 0
			sound.play_effect('rsc/bumper.mp3')
			
		if x - w/2 < 0:
			sound.play_effect('rsc/bumper.mp3')
			self.position = (w/2, y)
			self.x_vel *= -1
		elif x + w/2 > sw:
			sound.play_effect('rsc/bumper.mp3')
			self.position = (sw - w/2, y)
			self.x_vel *= -1
			
		if self.dead:
			self.rotation += 0.1
			if self.cur_dff == 0:
				self.alpha = (self.alpha + 1) % 2
			self.cur_dff += 1
			self.cur_dff %= self.death_flash_frames
		else:
			self.rotation = (self.y_vel/20)
		
	def flap(self):
		if self.y_vel < 0:
			self.y_vel = 0
		self.y_vel += self.flap_speed
		self.play_random_flap_sound()
		
	def play_random_flap_sound(self):
		p = random.random()*(0.5)+0.75
		if random.random() < .1:
			sound.play_effect('rsc/spin.mp3', pitch=p, volume=.3)
		else:
			sound.play_effect('rsc/jump.mp3', pitch=p, volume=.3)
		
	def get_hitbox(self):
		w,h = (42,36)
		x,y = self.position
		return Rect(x-w/2,y-h/2,w,h)
		
	def reset(self):
		self.position = (100,600)
		self.y_vel = 0
		self.x_vel = 0
		self.dead = False
		self.alpha = 1
		
	def die(self):
		self.rotation = math.pi
		self.y_vel = random.randint(6, 15)
		self.x_vel = random.randint(-6, 6)
		self.dead = True
