from scene import *
import ui



class PauseBtn (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'iob:ios7_pause_256', **kwargs)
		self.size = (64,64)
		self.anchor_point = (0,0)
		
	def set_play_icon(self):
		self.texture = Texture(ui.Image('iob:ios7_play_256'))
		self.size = (64,64)
		
	def set_pause_icon(self):
		self.texture = Texture(ui.Image('iob:ios7_pause_256'))
		self.size = (64,64)
