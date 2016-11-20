import numpy as np; import ctypes
import pyglet; import pyglet.gl as gl
from clockdeco import clock

@clock
def drawArray(someArray):

    vertPoints = someArray[:,:2].flatten().astype(ctypes.c_float)
    gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertPoints.ctypes.data)
    gl.glDrawArrays(gl.GL_POINTS, 0, len(vertPoints) // 2)

window = pyglet.window.Window(400,400)

@window.event
def on_draw():
    gl.glPointSize(10.0)
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

    points = np.random.random((50,5))*np.array([400,400,1,1,1])
    drawArray(points)

pyglet.app.run()