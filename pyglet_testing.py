import numpy as np
from itertools import chain
from collections import namedtuple
import math
import time
import tkinter as tk
from pyglet.gl import *



Coordinate = namedtuple('Coordinate', ['x', 'y'])
Position = namedtuple('Position', ['i','j'])
Cell = namedtuple('Cell', ['coordinate', 'position', 'size'])
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

class Host:
	def __init__(self, cell, pattern, i):
		#cell attributes
		self.coordinate = cell.coordinate
		self.size = cell.size
		self.position = cell.position
		self.letter_position = i

		#internal cells and attributes
		k, positions = pattern
		self.length = k
		self.binary_field = pattern_to_binary(pattern)
		coord_field = np.array([position_to_coordinate(self, np.array([u, v]), k) for u, v in np.ndindex(k,k)]).reshape(k,k,2)
		self.canvas = [Cell(entry_at(coord_field, u, v), np.array([u, v]), self.size/k) for u, v in np.ndindex(k,k) if self.binary_field[u,v]]

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
				cells.append(cell)
			else:
				cells.append(Cell(coord_field[cell.position[0], cell.position[1]], cell.position, self.subsize))
		self.canvas = cells

	def get_cells(self):
		new_cells = []
		for cell in self.canvas:
			if isinstance(cell, Host):
				new_cells.extend(cell.get_cells())
			else:
				new_cells.append(recalc_cell(self, cell))

		return new_cells

	@property
	def subsize(self):
		return self.size/self.length

	def grow(self):
		self.size += ((self.size)/12)
		self.recalculate_cells()

	def expand(self, n):
		if n == 0:
			return

		for i, cell in enumerate(self.canvas):
			if not isinstance(cell, Host):
				#create new Host
				j = (self.letter_position+1)%3
				new_host = Host(cell, word[j], j)
				self.canvas[i] = new_host
			else:
				cell.expand(n-1)

	def __repr__(self):
		return str(self.coordinate) + str(self.size)


def initial_config():
	C = Cell(np.array([10, 10]), Position(0, 0), 1200)
	H = Host(C, word[0], 0)
	H.expand(1)
#	H.expand(2)
	# for i in range(1, 2):
	# 	H.expand(i)
	return H

def draw_host(host):
	cells = host.get_cells()
	for cell in cells:
		draw_cell(cell)
#	map(draw_cell, cells)

def draw_cell(cell):
	x, y = cell.coordinate
	#print(x, y, cell.size)
	glRectf(1200-y, 1200-x, 1200 - y + cell.size, 1200 - x + cell.size)
	#glRectf(-10,-10,20,20)


# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=window.width // 2, y=window.height // 2,
#                           anchor_x='center', anchor_y='center')

top_host = initial_config()
# @window.event
# def on_draw():
# 	glClear(GL_COLOR_BUFFER_BIT)
# 	glLoadIdentity()
# 	window.clear()
# 	time.sleep(1)
# 	#glColor3f(float(1.0), float(0.0), float(0.0))
# 	draw_host(top_host)
# 	label.draw()



window = pyglet.window.Window()
window.set_size(1200, 1200)

@window.event
def on_draw():
	window.clear()
	draw_host(top_host)
	#glScalef(float(-1.0), float(1.0), float(-1.0))

def update(dt):
	top_host.grow()

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()