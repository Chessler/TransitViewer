# A simple test of importing the lightcurve.
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
from matplotlib.patches import Rectangle

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

class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        print 'press'
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print 'release'
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()

a = Annotate()
plt.suptitle("Raw Data", fontsize=20)
plt.xlabel('Time', fontsize=16)
plt.ylabel('Flux', fontsize=16)

class Index:
    ind = 0
    def next(self, event):
        #self.ind += 1
        #i = self.ind % len(freqs)
        ydata = flux
        l.set_ydata(ydata)
        plt.grid(True)
        plt.suptitle("Detrended Data", fontsize=20)
        plt.draw()

    def prev(self, event):
        #self.ind -= 1
        #i = self.ind % len(freqs)
        ydata = raw
        l.set_ydata(ydata)
        plt.grid(True)
        plt.suptitle("Raw Data", fontsize=20)
        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

#l.set_title("Lightcurve 1")
#l.set_xlabel("Time")
#l.set_ylabel("Flux")

cursor = Cursor(ax, useblit=True, color='black', linewidth=2 )
plt.grid(True)

plt.show()