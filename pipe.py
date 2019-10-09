from scene import SpriteNode, Rect
import random
import math



class Pipe (SpriteNode):
	
	blocksize = 64
	
	def __init__(self, scene_size):
		self.gap = 150
		px,py = (scene_size.width,
		random.randint(Pipe.blocksize/2, scene_size.height - (Pipe.blocksize/2 + self.gap)))
		self.position = (px,py)
		self.img = 'plf:Tile_BoxCrate_double'
		
		# space from the opening to the top and bottom
		self.pbottomh = math.ceil(py)
		self.ptoph = math.ceil(scene_size.h - (py + self.gap))
		
		ny = 0
		for i in range(ny, ny-self.pbottomh, Pipe.blocksize*-1):
			n = SpriteNode (self.img, position=(0,i))
			n.anchor_point = (0,1)
			self.add_child(n)
		
		ny = self.gap + Pipe.blocksize
		for i in range(ny, ny+self.ptoph, Pipe.blocksize):
			n = SpriteNode (self.img, position=(0,i))
			n.anchor_point = (0,1)
			self.add_child(n)
		
	def update(self, dist):
		x,y = self.position
		self.position = (x - dist, y)
		
	def get_hit_boxes(self):
		x,y = self.position
		return [Rect(x, y + self.gap, Pipe.blocksize, self.ptoph),
		        Rect(x, 0, Pipe.blocksize, self.pbottomh)]
