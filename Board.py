import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock
from functools import partial
import math
from Pattern import WORD as WD

WORD = WD()

EXPAND_THRESHOLD = 8000
GROWTH = 6
SCREENSIZE = 1200

class Host:
	def __init__(self, numpy_coord, size, letter_pos, levels):
		self.coordinate = numpy_coord
		self.size = size
		self.levels = levels
		self.top_level = 0
		self.pointsize = 1.0
		self.updateField()
		self.center = self.get_center(self.top_level)

	def displacement(self):
		return (np.array([SCREENSIZE/2, SCREENSIZE/2]) - self.center) / (GROWTH*2)

	def grow(self):
		if self.size > EXPAND_THRESHOLD:
			self.expand()
		else:
			self.size += (self.size / GROWTH)
			self.coordinate = self.coordinate + (self.center - self.get_center(self.top_level))
			self.updateField()
			self.center = self.get_center(self.top_level)
			self.center += self.displacement()
			self.pointsize += self.pointsize/GROWTH

	def get_center(self, level):
		L, _, C = self.getWord(level)
		size = self.size / L
		return self.coordinate + C * np.array([size, size]) + np.array([size/2, size/2])

	def getWord(self, i):
		return WORD[i%len(WORD)].astuple()

	def scaled_top_lefts(self, start_at, level, length, patt):
		size = self.size / math.pow(length, level)
		return start_at + patt * (size/length)

	def make_top_lefts(self, t, i, length, patt):

		if i >= self.levels:
			return self.make_cells(t, i, length, patt)

		p_1 = self.scaled_top_lefts(t, i, length, patt)
		ll, pp, _ = self.getWord(i+self.top_level+1)

		cells = []
		mtl = partial(self.make_top_lefts, i=i+1, length=ll, patt=pp)
		for tt in p_1:
			cells.extend(mtl(tt))
		return cells

	def make_cells(self, t, i, length, patt):

		size = self.size / math.pow(length, i)
		p = t + patt * (size / length)
		p[:][:, 1] = SCREENSIZE - p[:][:, 1]
		return p

	@clock
	def recursive_strategy(self):
		length_0, patt_0, _ = self.getWord(self.top_level)
		return self.make_top_lefts(self.coordinate, 0, length_0, patt_0)

	def upgrade(self):
		return self.center - [self.size/2, self.size/2]

	def updateField(self):
		self.field = np.array(self.recursive_strategy())

	def expand(self):
		self.top_level += 1
		WORD[self.top_level%len(WORD)].replaceCenter()
		self.size /= 12
		self.coordinate = self.upgrade()
		self.center = self.get_center(self.top_level)
		self.pointsize = 0.3

window = pyglet.window.Window(SCREENSIZE,SCREENSIZE)
H = Host(np.array([0, 0]), SCREENSIZE, 0, 2)

# @clock
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

