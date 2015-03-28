# A simple test of importing the lightcurve.
# ...that then became the main class of EVERYTHING
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
from matplotlib.widgets import RectangleSelector
from pylab import *

time = []
flux = []
selectedDataRange = []

#TODO: Make a class of File I/O
f = open("firstCurve.out")
for row in csv.reader(f):
    time.append(row[0])
    flux.append(row[5])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
l, = plt.plot(time, flux, lw=2)
plt.grid(True)

plt.suptitle("Corrected Data", fontsize=20)
plt.xlabel('Time', fontsize=16)
plt.ylabel('Flux', fontsize=16)

#for use later on
beenSelected = False

#to find the closest index from what we select since it's *too* precise
def findClosest(num, list):
    new_list = [float(i) for i in list]
    idx = (np.abs(new_list-num)).argmin() #I have no idea how this works, I just got it from stackoverflow
    return idx

#for the rectangle selector
def onselect(eclick, erelease):
    'eclick and erelease are matplotlib events at press and release'
    #print ' startposition : (%f, %f)' % (eclick.xdata, eclick.ydata)
    #print ' endposition   : (%f, %f)' % (erelease.xdata, erelease.ydata)
    global selectedDataRange
    if erelease.xdata < eclick.xdata:
        selectedDataRange = [erelease.xdata, eclick.xdata]
    elif erelease.xdata > eclick.xdata:
        selectedDataRange = [eclick.xdata, erelease.xdata]
    global beenSelected #to access global variables
    beenSelected = True

#I don't know why there's redundancy but it doesn't work if I take this out
def toggle_selector(event):
    if toggle_selector.RS.active:
        print ' RectangleSelector deactivated.'
        toggle_selector.RS.set_active(False)
    if  not toggle_selector.RS.active:
        print ' RectangleSelector activated.'
        toggle_selector.RS.set_active(True)

#still for the selector
class Index:
    def toggle(self, event):
        if toggle_selector.RS.active:
            print ' RectangleSelector deactivated.'
            toggle_selector.RS.set_active(False)
        elif (not toggle_selector.RS.active):
            print ' RectangleSelector activated.'
            toggle_selector.RS.set_active(True)

    def select(self, event):
        #The code that's run when you hit the "Select Data" button
        if not beenSelected:
            return
        global time #this is how we modify global variables
        x1 = findClosest(selectedDataRange[0], time) #find variables in flux array
        x2 = findClosest(selectedDataRange[1], time)
        newArr = flux[x1:x2] #slicing the array
        newTime = time[x1:x2]
        newArr2 = [float(i) for i in newArr] #because dft bitches if we don't convert it
        newTime2 = [float(i) for i in newTime]
        f = range(0,10^7,300*(10^6)) #the variables Dr. B gave me
        newFlux = dft(newTime2, newArr2, f)
        plt.clf() #clear plot
        l,=plt.plot(newTime2, newFlux, lw=2) #plot plot plot
        k,=plt.plot(newTime2, newArr, lw=2)
        plt.show() #plot

#Discrete Fourier Transform, taken directly from Dr. Buzasi's MATLAB function
def dft(t,x,f):
    i = 1j #might not have to set it to a variable but better safe than sorry!
    t = np.transpose(t) #the equivalent of t'
    w1 = f*t
    w2 = -2*math.pi*i
    W = exp(w1*w2)
    X = W * x
    return X

# the rectangle drawer
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
        if not toggle_selector.RS.active:
            return
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        if not toggle_selector.RS.active:
            return
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.rect.set_facecolor('blue')
        self.rect.set_alpha(0.5)
        self.ax.figure.canvas.draw()

#UI setup
a = Annotate() #the rectangle, I'm too scared to rename it
cursor = Cursor(ax, useblit=True, color='black', linewidth=2) #the crosshair of AWESOME

callback = Index() #button handler
togglePlacement = plt.axes([0.65, 0.05, 0.3, 0.055])
rectToggle = Button(togglePlacement, 'Rectangle Select Toggle')
rectToggle.on_clicked(callback.toggle)

selectDataPlacement = plt.axes([0.45, 0.05, 0.15, 0.055])
selectData = Button(selectDataPlacement, 'Select Data')
selectData.on_clicked(callback.select)

toggle_selector.RS = RectangleSelector(ax, onselect, drawtype='line')
toggle_selector.RS.set_active(False)

plt.grid(True)

plt.show()