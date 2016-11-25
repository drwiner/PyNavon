import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock
from collections import namedtuple
from functools import partial
import time
import math


Pattern = namedtuple('Pattern', ['length', 'positions', 'center'])

pat_A = Pattern(length=12,positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]),center=(5, 6))
pat_C = Pattern(length=12, positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]), center=(3, 8))
pat_T = Pattern(length=12,positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]),center=(5, 5))

word = [pat_T, pat_C, pat_A]

class Host:
	def __init__(self, numpy_coord, size, letter_pos, levels):
		self.coordinate = numpy_coord
		self.size = size
		self.levels = levels
		self.top_level = 0
		self.pointsize = 1.0
		self.center = self.get_center()
		self.updateField()

	#@clock
	def grow(self):
		if self.size > 8000:
			self.expand()
		else:
			self.size += (self.size / 24)
			self.coordinate = self.coordinate + (self.center - self.get_center())
			self.updateField()
			self.center = self.get_center()

	def get_center(self):
		L, _, C = self.getWord(self.top_level)
		size = self.size / L
		return self.coordinate + np.array(C) * size + [size/2, size/2]

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

	def make_cells(self, t, i, length, patt):
		size = int(self.size / math.pow(length, i))
		p = t + patt * (size / length)
		p[:][:, 1] = 1200 - p[:][:, 1]
		return p

	def recursive_strategy(self):
		length_0, patt_0, _ = word[self.top_level]
		return self.make_top_lefts(self.coordinate, 0, length_0, patt_0)

	def upgrade(self):
		return self.center - [self.size/2, self.size/2]

	#@clock
	def updateField(self):
		self.field = np.array(self.recursive_strategy())

	def expand(self):
		self.top_level += 1
		if self.top_level >= len(word):
			self.top_level = 0

		self.size /= 12
		self.coordinate = self.upgrade()
		self.center = self.get_center()

window = pyglet.window.Window(1200,1200)
H = Host(np.array([0, 0]), 1200, 0, 2)

#@clock
def drawArray(someArray):
	vertPoints = someArray[:, :2].flatten().astype(ctypes.c_float)
	gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertPoints.ctypes.data)
	gl.glDrawArrays(gl.GL_POINTS, 0, len(vertPoints) // 2)

@window.event
def on_draw():
	gl.glPointSize(H.pointsize)
	gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
	drawArray(H.field)

def update(dt):
	window.clear()
	H.grow()
	gl.glPointSize(H.pointsize)
	drawArray(H.field)


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()

