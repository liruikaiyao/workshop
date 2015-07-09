# coding=utf-8
import numpy
import toyplot

x = numpy.linspace(0, 10)
y = x ** 2

canvas = toyplot.Canvas(width=300, height=300)
axes = canvas.axes()
axes.plot(x, y)
