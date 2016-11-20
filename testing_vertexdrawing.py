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
	def __init__(self, numpy_coord, numpy_position, size):
		self.coordinate = numpy_coord
		self.position = numpy_position
		self.size = size

	def get_cells(self):
		return [self]

class Host:
	def __init__(self, cell, letter_pos, levels):
		#cell attributes
		self.coordinate = cell.coordinate
		self.size = cell.size
		self.position = cell.position
		self.letter_position = letter_pos
		self.level = levels
		pattern  = word[self.letter_position]
		k, positions = pattern
		self.length = k
		self.pointsize = 1.0

		_axis = np.linspace(0, self.size, num=self.size / self.cellsize, dtype=np.dtype(gl.GLfloat))
		self.field = np.array([np.array([i, j]) for i in _axis for j in _axis])

	@property
	def cellsize(self):
		return self.size / math.pow(self.length, self.level)


	@clock
	def grow(self):
		self.pointsize += .01

	#	self.size += ((self.size) / 248)
		#t = self.cellsize - .5*self.cellsize
		gl.glPointSize(self.pointsize)
		drawArray(H.field)

	#self.size += ((self.size)/4)
		#_axis = np.linspace(0, self.size, num=self.size / self.cellsize, dtype=np.dtype(np.float32))
		#self.field = np.array([np.array([i, j]) for i in _axis for j in _axis])

def initial_config():
	C = Cell(np.array([10, 10]), np.array([0,0]), 1200)
	H = Host(C, 0, 2)
	return H

@clock
def draw_host(host):
	k = host.cellsize
	s = host.size
	for x in host.field:
		#glRectf(i+2, s-j+2, i+k-2, s-j_)
		glRectf(x[0]+2, s-x[1]+2, x[0] + k-2, s-x[1]+k-2)

@clock
def drawArray(someArray):

    vertPoints = someArray[:,:2].flatten().astype(ctypes.c_float)
    gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertPoints.ctypes.data)
    gl.glDrawArrays(gl.GL_POINTS, 0, len(vertPoints) // 2)

window = pyglet.window.Window(1200,1200)
H = initial_config()

@window.event
def on_draw():
    gl.glPointSize(1.0)
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

   # points = np.random.random((50,5))*np.array([400,400,1,1,1])
    drawArray(H.field)

def update(dt):
	H.grow()
	#time.sleep(0.2)
	#drawArray(H.field)
	#top_host.grow()


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()

