# A simple test of importing the lightcurve.
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
from matplotlib.widgets import RectangleSelector
from pylab import *

time = []
flux = []
raw = []

f = open("firstCurve.out")
for row in csv.reader(f):
    time.append(row[0])
    raw.append(row[4])
    flux.append(row[5])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
l, = plt.plot(time, raw, lw=2)
plt.grid(True)

plt.suptitle("Raw Data", fontsize=20)
plt.xlabel('Time', fontsize=16)
plt.ylabel('Flux', fontsize=16)


def onselect(eclick, erelease):
    'eclick and erelease are matplotlib events at press and release'
    print ' startposition : (%f, %f)' % (eclick.xdata, eclick.ydata)
    print ' endposition   : (%f, %f)' % (erelease.xdata, erelease.ydata)
    print ' used button   : ', eclick.button


def toggle_selector(event):
    if toggle_selector.RS.active:
        print ' RectangleSelector deactivated.'
        toggle_selector.RS.set_active(False)
    if  not toggle_selector.RS.active:
        print ' RectangleSelector activated.'
        toggle_selector.RS.set_active(True)


class Index:
    def toggle(self, event):
        if toggle_selector.RS.active:
            print ' RectangleSelector deactivated.'
            toggle_selector.RS.set_active(False)
        elif (not toggle_selector.RS.active):
            print ' RectangleSelector activated.'
            toggle_selector.RS.set_active(True)


class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.pressed = False
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        print 'press'
        self.presssed = True
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        self.pressed = False
        print 'release'
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        if toggle_selector.RS.active:
            self.rect.set_facecolor('blue')
            self.rect.set_alpha(0.5)
            self.ax.figure.canvas.draw()

a = Annotate()
cursor = Cursor(ax, useblit=True, color='black', linewidth=2)

callback = Index()
togglePlacement = plt.axes([0.65, 0.05, 0.3, 0.075])
rectToggle = Button(togglePlacement, 'Rectangle Select Toggle')
rectToggle.on_clicked(callback.toggle)


# l.set_title("Lightcurve 1")
#l.set_xlabel("Time")
#l.set_ylabel("Flux")

plt.grid(True)

toggle_selector.RS = RectangleSelector(ax, onselect, drawtype='line')
toggle_selector.RS.set_active(False)

plt.show()