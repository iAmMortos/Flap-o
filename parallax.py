from scene import Node, SpriteNode



class Parallax (SpriteNode):
	def __init__(self, scene_size):
		
		self.r1img = 'plf:Ground_GrassMid'
		self.r2img = 'plf:BG_Colored_grass'
		
		self.row1 = Node(parent=self, position=(0,0))
		self.row2 = Node(parent=self, position=(0,64))
		
		self.row1.anchor_point = (0,0)
		self.row2.anchor_point = (0,0)
		
		self.row1.z_position = -50
		self.row2.z_position = -100
		
		self.r1size = 64
		self.r2size = 512
		
		self.row1.scale = 2
		self.row2.scale = 1
		
		#self.row1scale = 0.5
		#self.row2scale = 0.1
		self.row1scale = 10
		self.row2scale = 3
		
		for x in range(0, round(scene_size.width) + self.r1size, self.r1size):
			r1 = SpriteNode(self.r1img, position=(x, self.row1.position.y))
			r1.anchor_point = (0,0)
			self.row1.add_child(r1)
		for x in range(0,round(scene_size.width) + self.r2size, self.r2size):
			r2 = SpriteNode(self.r2img, position=(x, self.row2.position.y))
			r2.anchor_point = (0,0)
			self.row2.add_child(r2)
			
	def update(self, speed):
		r1x,r1y = self.row1.position
		r2x,r2y = self.row2.position
		
		nr1x = r1x - (speed * self.row1scale)
		nr2x = r2x - (speed * self.row2scale)
		
		while nr1x < self.r1size * -1 * self.row1.scale:
			nr1x += self.r1size * self.row1.scale
		while nr2x < self.r2size * -1 * self.row2.scale:
			nr2x += self.r2size * self.row2.scale
			
		self.row1.position = (nr1x, r1y)
		self.row2.position = (nr2x, r2y)
		
	def reset(self):
		self.row1.position = (0, self.row1.position.y)
		self.row2.position = (0, self.row2.position.y)
