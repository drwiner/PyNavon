import numpy as np
from collections import namedtuple
from clockdeco import clock
from pyglet.gl import *
import itertools
import math
from OpenGL.arrays import vbo

Coordinate = namedtuple('Coordinate', ['x', 'y'])
Position = namedtuple('Position', ['i','j'])
# Cell = namedtuple('Cell', ['coordinate', 'position', 'size'])
Pattern = namedtuple('Pattern', ['length', 'positions'])

pat_A = Pattern(12,positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]))

pat_C = Pattern(12,positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]))

pat_T = Pattern(12,positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]))

pat_test = Pattern(2, positions=np.array([(0,0), (1,1)]))

word = [pat_T, pat_C, pat_A, pat_test]


def pattern_to_binary(pattern):
	k, positions = pattern
	binary_field = np.zeros((k,k))
	for y,x in positions:
		binary_field[x,y] = 1
	return binary_field

def position_to_coordinate(cell, position, pattern_length):
	return cell.coordinate + ((position * cell.size) / pattern_length)

def entry_at(field, u, v):
	return field[u,v,0], field[u,v,1]



def recalc_cell(host, cell):
	coord = position_to_coordinate(host, cell.position, host.length)
	size = host.size/host.length
	return Cell(coord, cell.position, size)


	#np.array([u for u, v in np.ndindex(k, k)]).reshape(k, k, 2)
	#row = np.array([self.coordinate + self.cellsize * i for i in range(math.pow(k, levels))])


class Cell:
	def __init__(self, numpy_coord, numpy_position, size):
		self.coordinate = numpy_coord
		self.position = numpy_position
		self.size = size

	def get_cells(self):
		return [self]

class Host:
	def __init__(self, cell, i, levels):
		#cell attributes
		self.coordinate = cell.coordinate
		self.size = cell.size
		self.position = cell.position
		self.letter_position = i
		self.level = levels

		#internal cells and attributes
		pattern  = word[self.letter_position]
		k, positions = pattern
		self.length = k

		_axis = np.linspace(0, self.size, num=self.size / self.cellsize, dtype=np.dtype(GLfloat))
		#self.field = np.vstack(np.meshgrid(_axis, _axis, np.array([0,1])))
		#self.field = [np.array([i,j]) for i in _axis for j in _axis]
		self.field = np.array([np.array([i,j]) for i in _axis for j in _axis])
		#self.verts = vbo.VBO(self.field)
		#label = np.dstack(self.field)
		#image = pyglet.image.Texture.create(1200,1200)
		#self.texture = pyglet.image.ImageData.create_texture(self.field,pyglet.image.Texture)
	#image = pyglet.image.ImageData(144,144,'RGB', )
		#self.field.View()
		#self.quad = gloo.Program(self.field)

	#	self.vertices =
		#pyglet.gl.glBindBuffer(pyglet.gl.GL_TEXTURE_2D, self.field)
		#self.field = np.meshgrid(_axis,np.array([0,1]), indexing='ij')
	#	pass

		#np.array([position_to_coordinate(self, np.array([u, v]), k) for u, v in np.ndindex(k, k)]).reshape(k, k, 2)

		#self.binary_field = pattern_to_binary(pattern)
	#	coord_field = np.array([position_to_coordinate(self, np.array([u, v]), k) for u, v in np.ndindex(k,k)]).reshape(k,k,2)
		#self.canvas = [Cell(entry_at(coord_field, u, v), np.array([u, v]), self.size/k) for u, v in np.ndindex(k,k) if self.binary_field[u,v]]

	#@clock
	def recalculate_cells(self):
		k = self.length
		#print(self.size)
		coord_field = np.array([position_to_coordinate(self, np.array([u, v]), k) for u, v in np.ndindex(k, k)]).reshape(k, k, 2)
		cells = []
		for i, cell in enumerate(self.canvas):
			if isinstance(cell, Host):
				cell.size = self.subsize
				cell.coordinate = coord_field[cell.position[0], cell.position[1]]
				cell.recalculate_cells()
				#cells.append(cell)
			else:
				cell.coordinate = coord_field[cell.position[0], cell.position[1]]
				cell.size = self.subsize
				#self.canvas[i] = Cell(coord_field[cell.position[0], cell.position[1]], cell.position, self.subsize)

	#@clock
	def get_cells(self):
		return itertools.chain.from_iterable([cell.get_cells() for cell in self.canvas])

	@property
	def subsize(self):
		return self.size/self.length

	@property
	def cellsize(self):
		return self.size/math.pow(self.length, self.level)

	@clock
	def linspace(self):
		return np.linspace(0, self.size, num=self.size / self.cellsize, dtype=np.dtype(np.float32))

	@clock
	def nparraythis(self, _axis):
		return np.array([(i,j) for i in _axis for j in _axis])
		#return [np.array([i, j]) for i in _axis for j in _axis]

	@clock
	def grow(self):
		self.size += ((self.size)/4)
		_axis = np.linspace(0, self.size, num=self.size / self.cellsize, dtype=np.dtype(np.float32))
		# self.field = np.vstack(np.meshgrid(_axis, _axis, np.array([0,1])))
		self.field = np.array([(i, j) for i in _axis for j in _axis])
		#self.field = [i for i in _axis.extend(_axis)]
		#self.recalculate_cells()

	def expand(self, n):
		if n == 0:
			return

		for i, cell in enumerate(self.canvas):
			if not isinstance(cell, Host):
				#create new Host
				j = (self.letter_position+1)%3
				new_host = Host(cell, j, n)
				self.canvas[i] = new_host
			else:
				cell.expand(n-1)

	def __repr__(self):
		return str(self.coordinate) + str(self.size)


def initial_config():
	C = Cell(np.array([10, 10]), Position(0, 0), 1200)
	H = Host(C, 0, 2)
	#H.expand(1)
	#H.expand(2)
	# for i in range(1, 2):
	# 	H.expand(i)
	return H

@clock
def draw_host(host):
	#vertices = host.field.view(gloo.VertexBuffer)
	# pyglet.image.Texture()
	# pyglet.glTexCoordPointerd(host.field)
	# pyglet.glEnable(GL_TEXTURE_COORD_ARRAY)
	#
	#img2 = pyglet.image.ImageData(1200, 1200, 'L', host.field.data, 1)
#	img2.blit(0,0,z=0, width=1200, height=1200)
	# img = pyglet.image.Texture.create(1200,1200)
	# img2.blit_into(img, 0,0, 0)
	# img2.blit(0,0)
	#host.quad.draw(gl.GL_TRIANGLES)
#	glBindTexture()
	k = host.cellsize
	s = host.size

	#glVertexPointer(2, GL_FLOAT, 0, host.verts)
	#pyglet.gl.glDrawArrays(GL_QUADS, 0, 2)
	for x in host.field:
		#glRectf(i+2, s-j+2, i+k-2, s-j_)
		glRectf(x[0]+2, s-x[1]+2, x[0] + k-2, s-x[1]+k-2)
	#for i,j in host.field:
	#[glRectf(i+2,host.size-j+2,i + host.cellsize-2, host.size - j + host.cellsize-2) for i, j in host.field]
	# k = range(int(len(host.field)/3))
	# #print(k)
	# for i in k:
	# 	for j in k:
	# 		print(i,k)
	# 		#print(host.field[i][j])
	#
#	cells = host.get_cells()
	# map(draw_cell, cells)
	#for cell in cells:
	#	draw_cell(cell)

def draw_cell(cell):
	y, x = cell.coordinate
	#print(x, y, cell.size)
	glRectf(x,1200-y, x + cell.size, 1200 - y + cell.size)



#window = app.Window(width=1200, height=1200)

top_host = initial_config()
# H = gloo.Program(vertex, fragment)
# H.bind(top_host.field)

window = pyglet.window.Window()
window.set_size(1200, 1200)


@window.event
def on_draw():
	window.clear()
	draw_host(top_host)

def update(dt):
	pass
	#top_host.grow()


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()