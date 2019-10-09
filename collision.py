def colliding(a,b):
	return a.intersects(b)
	
def colliding_o2m(a, bs):
	for b in bs:
		if colliding(a,b): return True
	return False



if __name__ == '__main__':
	from scene import *
	import scene_drawing
	import sound
	import random
	import math
	A = Action
	
	draw_hit_boxes = True
	
	class Square (SpriteNode):
		def __init__(self, **kwargs):
			SpriteNode.__init__(self, 'emj:White_Square', **kwargs)
			
	class Circle (SpriteNode):
		def __init__(self, **kwargs):
			SpriteNode.__init__(self, 'emj:Red_Circle', **kwargs)
			
	class MyScene (Scene):
		def setup(self):
			x,y,w,h = self.bounds
			
			self.sq = Square()
			self.sq.size = (100,100)
			self.sq.position = (w/2,h/2)
			self.add_child(self.sq)
			
			self.cr = Circle()
			self.cr.size = (100,100)
			self.cr.position = (50,50)
			self.add_child(self.cr)
		
		def did_change_size(self):
			pass
			
		def draw(self):
			if draw_hit_boxes:
				scene_drawing.stroke_weight(2)
				scene_drawing.no_fill()
				
				scene_drawing.stroke(255,0,0)
				scene_drawing.rect(*self.cr.frame)
				
				scene_drawing.stroke(0,0,255)
				scene_drawing.rect(*self.sq.frame)
		
		def update(self):
			if colliding(self.sq.frame, self.cr.frame):
				self.background_color = '#ad0000'
			else:
				self.background_color = '#64c800'
		
		def touch_began(self, touch):
			self.touch_moved(touch)
		
		def touch_moved(self, touch):
			self.cr.position = touch.location
		
		def touch_ended(self, touch):
			pass
			
	run(MyScene(), show_fps=False)
