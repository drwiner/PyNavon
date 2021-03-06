import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock
from functools import partial
import math
from Pattern import WORD as WD



EXPAND_THRESHOLD = 6000
GROWTH = 24
SCREENSIZE = 1200

window = pyglet.window.Window(SCREENSIZE,SCREENSIZE)
batch = pyglet.graphics.Batch()

from pyglet_gui.manager import Manager
from pyglet_gui.text_input import TextInput
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
			   "font_size": 12,
			   "text_color": [255, 255, 255, 255],
			   "gui_color": [255, 0, 0, 255],
			   "input": {
				#	"text" : letters,
				   "image": {
					   "source": "input.png",
					   "frame": [3, 3, 2, 2],
					   "padding": [3, 3, 2, 3]
				   },
				   # need a focus color
				   "focus_color": [255, 255, 255, 64],
				   "focus": {
					   "image": {
						   "source": "input-highlight.png"
					   } }},
				"slider": {
                   "knob": {
                       "image": {
                           "source": "slider-knob.png"
                       },
                       "offset": [-5, -11]
                   },
                   "padding": [8, 8, 8, 8],
                   "step": {
                       "image": {
                           "source": "slider-step.png"
                       },
                       "offset": [-2, -8]
                   },
                   "bar": {
                       "image": {
                           "source": "slider-bar.png",
                           "frame": [8, 8, 8, 0],
                           "padding": [8, 8, 8, 8]
                       }
                   }
               },
			  }, resources_path='theme/')
letters = "hello world"
class Host:
	WORD = WD(letters)
	wd_lens = WORD.wd_lens()

	def __init__(self, numpy_coord, size, letter_pos, levels):
		self.coordinate = numpy_coord
		self.size = size
		self.levels = levels
		self.top_level = 0
		self.pointsize = 1.0
		self.updateField()
		self.center = self.get_center(self.top_level)
		self.zoom_mode = True

	def displacement(self):
		return (np.array([SCREENSIZE/2, SCREENSIZE/2]) - self.center) / (GROWTH*2)

	def grow(self):
		if self.size > EXPAND_THRESHOLD:
			self.expand()
		else:
			#pass
			if self.zoom_mode:
				self.size += (self.size / GROWTH)
				self.coordinate = self.coordinate + (self.center - self.get_center(self.top_level))
				self.updateField()
				self.center = self.get_center(self.top_level)
				self.center += self.displacement()
				self.pointsize += self.pointsize/(GROWTH*2)

	def get_center(self, level):
		L, _, C = self.getWord(level)
		size = self.size / L
		return self.coordinate + C * np.array([size, size]) + np.array([size/2, size/2])

	def getWord(self, i):
		return self.WORD[i%len(self.WORD)].astuple()

	def scaled_top_lefts(self, start_at, level, length, patt):
	#	size = self.size / math.pow(length, level)
		size = self.size / self.WORD.get_size(level, self.top_level)
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

		size = self.size / self.WORD.get_size(i, self.top_level)
		p = t + patt * (size / length)
		p[:][:, 1] = SCREENSIZE - p[:][:, 1]
		return p

#	@clock
	def recursive_strategy(self):
		length_0, patt_0, _ = self.getWord(self.top_level)
		return self.make_top_lefts(self.coordinate, 0, length_0, patt_0)

	def upgrade(self):
		return self.center - [self.size/2, self.size/2]

	def updateField(self):
		self.field = np.array(self.recursive_strategy())

	def expand(self):
		self.top_level += 1
		letter = self.WORD[self.top_level % len(self.WORD)]
		letter.replaceCenter()
		#self.size /= letter.length
		self.size /= self.wd_lens[(self.top_level-1)%len(self.WORD)]
		self.coordinate = self.upgrade()
		self.center = self.get_center(self.top_level)
		self.pointsize = 1.3


H = Host(np.array([0, 0]), SCREENSIZE, 0, 2)

from pyglet_gui.containers import VerticalContainer

from pyglet_gui.sliders import HorizontalSlider

class Letters(TextInput):

	def on_text(self, text):
		assert self.is_focus()
		self._caret.on_text(text)
		if self._max_length and len(self._document.text) > self._max_length:
			self._document.text = self._document.text[:self._max_length]
			self._caret.mark = self._caret.position = self._max_length

		print(self._document.text)
		H.WORD = WD(self._document.text.lower())
		H.wd_lens = H.WORD.wd_lens()
		return pyglet.event.EVENT_HANDLED

class SpeedSlider(HorizontalSlider):
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		bar_x, bar_y, bar_width, bar_height = self._bar.get_content_region()
		self.set_knob_pos(float(x - bar_x) / bar_width)
		global GROWTH
		GROWTH = 24 - (float(x - bar_x) / bar_width)
		print(GROWTH, (float(x - bar_x) / bar_width))
		return True

def f(value):
	print(value)
	global GROWTH
	if value <= 2:
		H.zoom_mode = False
	else:
		H.zoom_mode = True
		GROWTH = 100 - value

L = Letters(text=letters)
HS = HorizontalSlider(value=12, min_value=1.0, max_value=99.9, width=150, on_set=f)

Manager(VerticalContainer([HS, L]), window=window, batch=batch, theme=theme)
Manager.set_position(L, x=SCREENSIZE-300, y=SCREENSIZE-50)
Manager.set_position(HS, x=SCREENSIZE-300, y=SCREENSIZE-100)
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
	batch.draw()

if __name__ == '__main__':
#	H = Host(np.array([0, 0]), SCREENSIZE, 0, 3)
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()

