import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock
from collections import namedtuple
from functools import partial
import time
import math


Pattern = namedtuple('Pattern', ['length', 'positions', 'center'])

pat_A = Pattern(length=12,
                positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]),
                center=(5, 6))

# _,pos = pat_A
# cell_A = np.array([(i, 1200-j) for i, j in pos])


pat_C = Pattern(length=12,
                positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]),
                center=(3, 8))

# _,pos = pat_C
# cell_C = np.array([(i,1200-j) for i,j in pos])


pat_T = Pattern(length=12,
                positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]),
                center=(5, 5))

# _,pos = pat_T
# cell_T = np.array([(i,1200-j) for i,j in pos])


#pat_test = Pattern(2, positions=np.array([(0,0), (1,1)]))

word = [pat_T, pat_C, pat_A]
#cell_worlds = [cell_T, cell_C, cell_A]

class Cell:
	def __init__(self, numpy_coord, size):
		self.coordinate = numpy_coord
		self.size = size

	def get_cells(self):
		return [self]

class Host:
	def __init__(self, cell, letter_pos, levels):
		self.coordinate = cell.coordinate
		self.size = cell.size
		self.levels = levels
		self.top_level = 0
		self.pointsize = 1.0
		self.center = self.get_center()
		self.updateField()

	#@clock
	def grow(self):
		#self.coordinate[0] -= 25

		self.size += (self.size / 24)
		if self.size > 8000:
			self.expand()
	#	if self.pointsize > 4.0:
	#		self.pointsize -= 3.0
		self.coordinate = self.coordinate + (self.center - self.get_center())
		self.updateField()



		#self.dialate(C, self.size, L)

		#self.pointsize += .03
		# print('pointsize', self.pointsize)
		# print('size', self.size)

		self.center = self.get_center()

	def make_cells(self, t, i, length, patt):
		size = int(self.size / math.pow(length, i))
		p = t + patt * (size / length)
		p[:][:, 1] = 1200 - p[:][:, 1]
		return p
		#return [(u, 1200-v) for u, v in p]
		#return [(tx,ty) for tx]
		#return [(tx, 1200 - ty]) for tx, ty in p]

	def top_range(self):
		length, patt, _ = self.getWord(self.top_level+1) #assumes top_level already adjusted
		size = int(self.size / math.pow(length, 1))
		return self.coordinate + patt * (size / length)

	@clock
	def get_center(self):
		#set the center at level 1 to be the scaled version
		#self.coordinate will be 0,0
		L, _, C = self.getWord(self.top_level)
		size = self.size / L
		return self.coordinate + np.array(C) * size + [size/2, size/2]
		#return self.scaled_top_lefts(self.coordinate, 1, L, np.array(C))


	def dialate(self, ctr, size, length):
		#np.array(ctr)*(self.size / 16)

		c = self.coordinate + np.array(ctr)
		c = c/16
		c = self.coordinate - c
		self.coordinate = self.coordinate + c

	def getWord(self, i):
		return word[((self.top_level + i) % len(word))]

	def scaled_top_lefts(self, start_at, level, length, patt):
		size = int(self.size / math.pow(length, level))
		return start_at + patt * (size/length)

	def make_top_lefts(self, t, i, length, patt):
		if i >= self.levels:
			return self.make_cells(t, i, length, patt)

		p_1 = self.scaled_top_lefts(t, i, length, patt)
		ll, pp, _ = self.getWord(i + 1)

		cells = []
		mtl = partial(self.make_top_lefts, i=i+1, length=ll, patt=pp)
		for tt in p_1:
			cells.extend(mtl(tt))
		return cells

	def recursive_strategy(self):
		length_0, patt_0, _ = word[self.top_level]
		return self.make_top_lefts(self.coordinate, 0, length_0, patt_0)

	def f(self, field):
		return [field[j][i] for i, j in self.indices]

	@clock
	def updateField(self):
		#before_coordinate = self.coordinate
		self.field = np.array(self.recursive_strategy())
		#cb = self.coordinate - before_coordinate
		#self.coordinate += cb


	def old_update_field(self):
		# idea: generate incides once (and after every expand), and just generate this array. But, not as fast apprtly.
		_axis_a = np.linspace(self.coordinate[0], self.coordinate[0]+self.size, num=1728, dtype=np.dtype(gl.GLfloat))
		_axis_b = 1200 - np.linspace(self.coordinate[1], self.coordinate[1]+self.size, num=1728, dtype=np.dtype(gl.GLfloat))
		field = [[(i, j) for i in _axis_a] for j in _axis_b]
		self.field = np.array(self.f(field))

	def expand(self):
		self.top_level += 1
		if self.top_level >= len(word):
			self.top_level = 0
		#top_lefts = self.top_range()
		self.size = self.size / 12
		#pass the torch
		self.coordinate = self.center
		self.center = self.get_center()

		#self.coordinate = find_nearest(top_lefts, np.zeros_like(top_lefts))


def initial_config():
	C = Cell(np.array([0, 0]), 1200)
	H = Host(C, 0, 2)
	return H

def find_nearest(array,value):
    idx = (np.abs(value-array)).argmin()
    return array[idx]


window = pyglet.window.Window(1200,1200)
H = initial_config()

#@clock
def drawArray(someArray):
	# x = (ctypes.c_float * len(someArray))(*someArray[:][0])
	# y = (ctypes.c_float * len(someArray))(*someArray[:][1])
	# vertPoints = list(zip(x,y))
	#someArray = np.array(someArray)
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

