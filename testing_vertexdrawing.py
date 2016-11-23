import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock
from collections import namedtuple
import time
import math

Pattern = namedtuple('Pattern', ['length', 'positions'])

pat_A = Pattern(12,positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]))

pat_C = Pattern(12,positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]))

pat_T = Pattern(12,positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]))

pat_test = Pattern(2, positions=np.array([(0,0), (1,1)]))

word = [pat_T, pat_C, pat_A, pat_test]

class Cell:
	def __init__(self, numpy_coord, size):
		self.coordinate = numpy_coord
		#self.position = numpy_position
		self.size = size

	def get_cells(self):
		return [self]

class Host:
	def __init__(self, cell, letter_pos, levels):
		#cell attributes

		self.coordinate = cell.coordinate
		self.size = cell.size
		#self.position = cell.position
		self.letter_position = letter_pos
		self.levels = levels
		pattern = word[self.letter_position]
		self.length, self.positions = pattern
		self.pointsize = 0.3

		self.updateField()


	@property
	def cellsize(self):
		return self.size / math.pow(self.length, self.levels)

	def size_lvl(self, level):
		return self.size / math.pow(self.length, level)

	@property
	def subsize(self):
		return self.size / self.length

	@property
	def arr(self):
		return int(self.size/self.cellsize)

	#@clock
	def grow(self):
		pass
		# self.size += (self.size/36)
		# self.coordinate[0] -= 15
		# self.coordinate[1] -= 15
		# self.updatePointSize()
		#self.updateField()

	def updatePointSize(self, n=.35):
		self.pointsize -= n
		if self.pointsize < .5:
			self.pointsize = 10.0
			#self.pointsize = .5

	@clock
	def recursive_strategy(self):
		cells = [np.array(self.coordinate)]
		x = 0
		y = 0

		length_0, patt_0 = word[0]
		size = self.size
		rng_0 = range(0, size, 100)
		rng_0 = range(0, 12)
		inc_rng_0 = [(i,j) for i in rng_0 for j in rng_0]
		top_lefts = np.array(patt_0)*(size/length_0)
		#cells.update({(x + i + inci, y + j + incj) for i, j in patt_0 for inci, incj in inc_rng_0})
		#top_lefts = np.array([(i + inci, j + incj) for i, j in patt_0 for inci, incj in inc_rng_0])
		for tl in top_lefts:
			length_1, patt_1 = word[1]
			size_1 = int(self.size / math.pow(length_1, 1))
			rng_1 = range(0, size_1, int(size_1 / length_1))
			rng_1 = range(0, 12)
			p_1 = tl + np.array(patt_1)*(size_1/length_1)
			inc_rng_1 = [(i, j) for i in rng_1 for j in rng_1]

			#top_lefts_1 = [(x + i + inci, y + j + incj) for i, j in p_1 for inci, incj in inc_rng_1]

			for t in p_1:
				length_2, patt_2 = word[2]
				size_2 = int(self.size / math.pow(length_1, 2))
				p_2 = t + np.array(patt_2)*(size_2/length_2)
				new_cells = [np.array([tx, 1200 - ty]) for tx, ty in p_2]
				#new_cells = np.array([np.array([tx + i + inci, 1200 - ty - j - incj], dtype=np.dtype(gl.GLfloat))
				                 #     for i, j in p_2 for inci, incj in inc_rng_1])
				cells.extend(new_cells)
		#length_2, patt_2 = word[2]
		#size_2 = int(self.size / math.pow(length_2, 2))
		#rng_2 = range(0, size_2, int(size_2 / length_2))




		#top_1 = np.array([(x+i+inci, y+j+incj) for i, j in patt_1 for inci, incj in rng_1])
		#cells.update({(x + i + inci, y + j + incj) for i, j in patt_1 for inci, incj in inc_rng_1})
			#for tx, ty in top_1:
			#	cells.update({(tx+i+inci, ty+j+incj) for i, j in patt_2 for inci, incj in rng_2})

		return cells

	def cart_rng(self, length, k):
		rng = range(0, self.size, int(self.size / math.pow(length, k)))
		return np.array([(i, j) for i in rng for j in rng])

	def top_lefts(self, pattern, rng):
		#given a pattern and a rng,
		# where the rng should be scoped to a particular sub region,
		# generate an array of top-lefts
		return np.array([np.array([i + inci, j + incj]) for i, j in pattern for inci, incj in rng])

	@clock
	def updateField(self):
		#_axis_a = np.linspace(self.coordinate[0], self.coordinate[0]+self.size, num=self.size, dtype=np.dtype(gl.GLfloat))
		#_axis_b = np.linspace(self.coordinate[1], self.coordinate[1]+self.size, num=self.size, dtype=np.dtype(gl.GLfloat))
		#field = np.array([np.array([i, 1200-j]) for i in _axis_a for j in _axis_b]).reshape(self.size, self.size, 2)

		#mask = self.constructMask()
		self.field = np.array(self.recursive_strategy())
		#np array method
		#self.field = np.array([field[cell[0], cell[1]] for cell in cells])
		#tuple method
		#self.field = np.array([np.array([self.coordinate[0] + i, 1200-self.coordinate[1] - j]) for (i, j) in cells])
		#pass
		#self.field = np.array([field[i, j] for (i, j) in cells])

	@clock
	def constructMask(self):
		original = np.array(self.positions)
		ran = range(0, self.arr, self.length)
	#	smallest = range(0, self.arr, )
		#arr = int(self.size / self.cellsize)

		#high_scale is the set of (u,v) tuples which correspond to mid-subcell regions in pattern
		high_scale = self.mask_it(original, int(math.pow(self.length, 2)))

		#tiles are the lowest level units?
		tiles = np.array([np.array([i+inci, j+incj])
		                  for i, j in original
		                  for inci in ran
		                  for incj in ran
		                  if (i+inci, j+incj) in high_scale])
		return tiles

	def expand(self):
		pass #self.length = self.length*self.length

	def contract(self):
		pass

	@clock
	def tile_it(self, original, length, restricted):
		scaled = original * length
		lrange = [(i, j) for i in range(length) for j in range(length)]
		np.array([np.array([i + inci, j + incj]) for i, j in original for (inci, incj) in lrange
		          if (i + inci, j + incj) in restricted])

	@clock
	def mask_it(self, original, length):
		#ran = range(0, self.arr, length)
		scaled = original * length
		lrange = [(i, j) for i in range(length) for j in range(length)]
		return {(i + u, j + v) for (i, j) in scaled for (u, v) in lrange}

def initial_config():
	C = Cell(np.array([0, 0]), 1200)
	H = Host(C, 0, 2)
	return H



window = pyglet.window.Window(1200,1200)
H = initial_config()

# @clock
def drawArray(someArray):
	vertPoints = someArray[:, :2].flatten().astype(ctypes.c_float)
	gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertPoints.ctypes.data)
	gl.glDrawArrays(gl.GL_POINTS, 0, len(vertPoints) // 2)

@window.event
def on_draw():
	gl.glPointSize(H.pointsize)
	gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
	# points = np.random.random((50,5))*np.array([400,400,1,1,1])
	drawArray(H.field)

def update(dt):
	window.clear()
	H.grow()
	gl.glPointSize(H.pointsize)
	drawArray(H.field)


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()

