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
    selectangle = Rectangle((0, 0), 1, 1)
    selectangle.x0 = eclick.xdata
    selectangle.y0 = eclick.ydata
    selectangle.x1 = erelease.xdata
    selectangle.y1 = erelease.ydata
    selectangle.set_width(selectangle.x1 - selectangle.x0)
    selectangle.set_height(selectangle.y1 - selectangle.y0)
    selectangle.set_xy((selectangle.x0, selectangle.y0))
    selectangle.figure.canvas.draw()


def toggle_selector(event):
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print ' RectangleSelector deactivated.'
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print ' RectangleSelector activated.'
        toggle_selector.RS.set_active(True)


class Index:
    ind = 0

    def toggle(self, event):
        if toggle_selector.RS.active:
            print ' RectangleSelector deactivated.'
            toggle_selector.RS.set_active(False)
        elif (not toggle_selector.RS.active):
            print ' RectangleSelector activated.'
            toggle_selector.RS.set_active(True)


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