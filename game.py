from scene import *
from flapo import Flapo
from pipe import Pipe
from ring import Ring
from death_ring import DeathRing
from parallax import Parallax
from pause_btn import PauseBtn
from collision import colliding_o2m, colliding
import scene_drawing
from enum import Enum
import os
import sound
import random
import math



debug = False



class State (Enum):
	INIT = 0
	PLAYING = 1
	DYING = 2
	GAME_OVER = 3
	PAUSED = 4



class Game (Scene):
	def setup(self):
		self.gottagofast = sound.play_effect('rsc/gottagofast.mp3', looping=True, volume=0.5)
		self.background_color = '#d0f4f7'
		self.state = State.INIT
		self.new_high_score = False
		
		self.score = 0
		self.high_score = 0
		
		if os.path.exists('.score'):
			with open('.score', 'r') as f:
				self.high_score = int(f.read())
		
		self.game_speed = 1
		self.game_speedup = 0.05
		self.new_pipe_trigger = 214
		
		self.pipes = []
		self.passed = []
		self.rings = []
		self.death_rings = []
		
		self.flapo = Flapo()
		self.flapo.z_position = 50
		self.add_child(self.flapo)
		self.add_pipe()
		
		self.parallax = Parallax(self.size)
		self.parallax.position = (0,0)
		self.parallax.z_position = -50
		if not debug:
			self.add_child(self.parallax)
		
		sw,sh = self.size
		self.score_node = LabelNode('0', font=('Helvetica', 72))
		self.score_node.anchor_point = (0.5, 1)
		self.score_node.position = (sw/2, sh)
		self.score_node.z_position = 100
		self.score_node.color = '#333'
		self.add_child(self.score_node)
		
		self.high_score_node = LabelNode('High Score: %s' % self.high_score)
		self.high_score_node.anchor_point = (0,1)
		self.high_score_node.position = (0,sh)
		self.high_score_node.z_position = 100
		self.high_score_node.color = '#333'
		self.add_child(self.high_score_node)
		
		self.center_label = LabelNode('Tap To Go Fast', font=('Helvetica', 32))
		self.center_label.position = (sw/2, sh/2)
		self.center_label.z_position = 100
		self.center_label.color = '#333'
		self.add_child(self.center_label)
		
		self.center_title = LabelNode('Sänic', font=('Helvetica', 64))
		self.center_title.position = (sw/2, sh/2 + 60)
		self.center_title.z_position = 100
		self.center_title.color = '#333'
		self.add_child(self.center_title)
		
		self.pause_btn = PauseBtn()
		self.pause_btn.position = (5,5)
		self.pause_btn.z_position = 100
		self.add_child(self.pause_btn)
		
	def update(self):
		if self.state == State.PLAYING:
			self.update_scene()
			self.check_collision()
			self.flapo.update()
			self.parallax.update(self.game_speed)
		elif self.state == State.DYING:
			self.update_scene()
			self.flapo.update()
			self.parallax.update(self.game_speed)
			if self.flapo.position.y < self.size.h * -1:
				self.game_over()
		elif self.state == State.PAUSED:
			pass
	
	def touch_began(self, touch):
		if self.state == State.INIT:
			self.start()
		elif self.state == State.GAME_OVER:
			self.restart()
		elif self.state == State.PLAYING:
			if touch.location in self.pause_btn.frame:
				self.pause()
			else:
				self.flapo.flap()
		elif self.state == State.PAUSED:
			self.unpause()
		
	def add_pipe(self):
		p = Pipe(self.size)
		self.add_child(p)
		self.pipes.append(p)
		
	def add_ring(self):
		r = Ring(self.size)
		r.position = (self.size.width + self.new_pipe_trigger/2 + Pipe.blocksize/2, r.position.y)
		self.add_child(r)
		self.rings.append(r)
		
	def update_scene(self):
		for ring in self.rings:
			ring.update(self.game_speed)
		for dr in self.death_rings:
			dr.update()
		for pipe in self.pipes:
			pipe.update(self.game_speed)
			if pipe not in self.passed and pipe.position.x + Pipe.blocksize < self.flapo.position.x and not self.flapo.dead:
				self.passed.append(pipe)
				sound.play_effect('rsc/mark.mp3')
				self.game_speed += self.game_speedup
				self.increment_score()
		self.pipes.sort(key=lambda p:p.position.x)
		self.rings.sort(key=lambda r:r.position.x)
		if len(self.rings) and self.rings[0].position.x < 0 - self.rings[0].size.width/2:
			self.rings[0].remove_from_parent()
			self.rings = self.rings[1:]
		if self.pipes[0].position.x < 0 - Pipe.blocksize:
			self.pipes[0].remove_from_parent()
			if self.pipes[0] in self.passed:
				self.passed.remove(self.pipes[0])
			self.pipes = self.pipes[1:]
		if self.pipes[-1].position.x <= self.size.width - self.new_pipe_trigger:
			self.add_pipe()
			if random.random() <= 0.4:
				self.add_ring()
			
	def die(self):
		sound.play_effect('rsc/rings_out.mp3')
		self.state = State.DYING
		nrings = 20
		curdir = 0
		while curdir < 2 * math.pi:
			dr = DeathRing(self.flapo.position, curdir)
			dr.z_position = 40
			self.death_rings.append(dr)
			self.add_child(dr)
			curdir += (2*math.pi)/nrings
		self.flapo.die()
		
	def ring_get(self, ring):
		sound.play_effect('rsc/ring.mp3')
		ring.remove_from_parent()
		self.rings.remove(ring)
		self.increment_score()
			
	def game_over(self):
		sound.play_effect('rsc/killed.mp3', volume=2)
		self.center_title.text = 'Game Over'
		self.center_label.text = 'New High Score!' if self.new_high_score else 'Tap to Go Fast Again'
		self.state = State.GAME_OVER
			
	def check_collision(self):
		for pipe in self.pipes:
			if colliding_o2m(self.flapo.get_hitbox(), pipe.get_hit_boxes()):
				self.die()
		for ring in self.rings:
			if colliding(self.flapo.get_hitbox(), ring.get_hitbox()):
				self.ring_get(ring)
				
		if self.flapo.position.y < 0 - 32:
			self.die()
				
	def increment_score(self):
		self.score += 1
		self.score_node.text = str(self.score)
		if self.score > self.high_score:
			self.new_high_score = True
			self.high_score = self.score
			with open('.score', 'w') as f:
				f.write(str(self.high_score))
			self.high_score_node.text = 'High Score: %s' % self.high_score
		
	def reset_score(self):
		self.score = 0
		self.score_node.text = str(self.score)
		
	def start(self):
		sound.play_effect('rsc/voice.m4a', volume=3)
		self.state = State.PLAYING
		self.center_label.text = ''
		self.center_title.text = ''
		
	def restart(self):
		for p in self.pipes:
			p.remove_from_parent()
		for r in self.rings:
			r.remove_from_parent()
		for dr in self.death_rings:
			dr.remove_from_parent()
		self.pipes = []
		self.passed = []
		self.rings = []
		self.death_rings = []
		self.reset_score()
		self.add_pipe()
		self.game_speed = 1
		self.flapo.reset()
		self.parallax.reset()
		self.new_high_score = False
		self.start()
		
	def stop(self):
		if self.gottagofast:
			self.gottagofast.stop()
			
	def pause(self):
		self.pause_btn.set_play_icon()
		self.state = State.PAUSED
		self.center_title.text = 'Paused'
		self.center_label.text = 'Temporarily Not Going Fast'
			
	def unpause(self):
		self.pause_btn.set_pause_icon()
		sound.play_effect('rsc/voice.m4a')
		self.state = State.PLAYING
		self.center_label.text = ''
		self.center_title.text = ''

	def draw(self):
		if debug:
			scene_drawing.stroke(255,0,0)
			scene_drawing.stroke_weight(2)
			scene_drawing.no_fill()
			scene_drawing.rect(*self.flapo.get_hitbox())
		
		

if __name__ == '__main__':
	run(Game(), show_fps=False, orientation=PORTRAIT)
