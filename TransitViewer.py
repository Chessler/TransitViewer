# A simple test of importing the lightcurve.
# ...that then became the main class of EVERYTHING
import tkFileDialog
import time as tardis
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
from matplotlib.widgets import RectangleSelector
from pylab import *
from Tkinter import Tk
from tkFileDialog import askopenfilename

time = []
flux = []
frequency = []
selectedDataRange = []
resumeFlag = False
beenTransf = False

Tk().withdraw() # open file open dialog
filename = askopenfilename()
f = open(filename)
for row in csv.reader(f):
    #generated lightcurves are stored differently than saved lightcurves,
    #so here we check if the file is a saved file or a new file
    if row[0] == 'F' or row[0] == 'R':
        resumeFlag = True
        if row[0] == 'F':
            global beenTransf
            beenTransf = True
        continue

    if resumeFlag:
        time.append(row[0])
        flux.append(row[1])

    if not resumeFlag:
        time.append(row[0])
        flux.append(row[5])

#for use later on
beenSelected = False
currentX = time
currentY = flux

#to find the closest index from what we select since it's *too* precise
def findClosest(num, list):
    new_list = [float(i) for i in list]
    idx = (np.abs(new_list - num)).argmin()  #I have no idea how this works, I just got it from stackoverflow
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
    global beenSelected  #to access global variables
    beenSelected = True


#I don't know why there's redundancy but it doesn't work if I take this out
def toggle_selector(event):
    if toggle_selector.RS.active:
        print ' RectangleSelector deactivated.'
        toggle_selector.RS.set_active(False)
    if not toggle_selector.RS.active:
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

        global beenTransf
        if beenTransf:
            phaseData()
        else:
            fourierSection()
            beenTransf = True

    def saveFile(self, event):
        outputFile = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
        writer = csv.writer(outputFile, delimiter=',')
        #check if we've done a Fourier transform and flag the file properly
        if beenPhased:
            global f_max
            f_max_string = str(f_max)
            writer.writerows(f_max_string)
        if beenTransf:
            writer.writerow("F")
        else:
            writer.writerow("R")
        writer.writerows(zip(currentX,currentY))
        outputFile.close()


#the section that processes doing the Fourier Transform and plotting it to screen
def fourierSection():
    global time, flux  #this is how we modify global variables
    x1 = findClosest(selectedDataRange[0], time)  #find variables in flux array
    x2 = findClosest(selectedDataRange[1], time)
    newArr = flux[x1:x2]  #slicing the array
    newArr = [float(i) for i in newArr]
    mean = np.mean(newArr)
    newArr2 = []
    newArr2[:] = [x - mean for x in newArr]
    newTime = time[x1:x2]
    #everything is already a float but we need to cast it anyway
    newTime2 = [float(i) for i in newTime]
    #creating a variable frequency array
    f = createArrOfSize(0.0225, 10, size(newTime2))
    newTime2 = np.asarray(newTime2)
    newArr2 = np.asarray(newArr2)
    f = np.asarray(f)
    newFlux = dft(newTime2, newArr2, f)

    #and we start re-plotting
    l.set_ydata(np.abs(newFlux))
    ymax = np.amax(np.abs(newFlux))
    l.set_xdata(f)
    ax.set_ylim([0,ymax+1000])
    ax.set_xlim([0,10])
    ax.set_title("Transformed Data", fontsize=20)
    ax.set_xlabel('Frequency', fontsize=16)
    ax.set_ylabel('Flux', fontsize=16)
    selectData.label.set_text("Phase Data")
    fig.canvas.draw()
    #update the global x and y for use throughout the rest of the program
    global currentX, currentY, time, frequency
    currentX = newTime2
    currentY = np.abs(newFlux)
    time = newTime2
    flux = newArr
    frequency = f

#create a frequency array of the size specified
def createArrOfSize(start, stop, size):
    increment = float(stop-start)/float(size)
    arr = arange(start, stop, increment)
    return arr

#Discrete Fourier Transform, taken directly from Dr. Buzasi's MATLAB function
def dft(t, x, f):
    N = t.size
    i = 1j
    W = np.exp((-2 * math.pi * i)*np.dot(f.reshape(N,1),t.reshape(1,N)))
    X = np.dot(W,x.reshape(N,1))
    out = X.reshape(f.shape).T
    return out

def phaseData():
    global currentY, time, frequency, flux
    peak = np.argmax(currentY)
    print peak
    global f_max
    f_max = frequency[peak]
    phasedTime = time
    phasedTime[:] = [x*f_max for x in time]
    #modulus operator is % in Python as well as other languages
    #normal programmers actually use (meaning languages with C-like syntax)
    phasedTime[:] = [x%1 for x in time]
    yx = zip(phasedTime, flux)
    yx.sort()
    flux = [x for y, x in yx]
    phasedTime.sort()
    l.set_ydata(flux)
    ymax = np.amax(flux)
    ymin = np.amin(flux)
    xmax = np.amax(phasedTime)
    l.set_xdata(phasedTime)
    ax.set_ylim([ymin-10,ymax+10])
    ax.set_xlim([0,xmax])
    ax.set_title("Phased Data", fontsize=20)
    global beenPhased
    beenPhased = True
    fig.canvas.draw()

# the rectangle drawer
class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0, 0), 1, 1)
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
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
l, = plt.plot(time, flux, lw=2)
plt.grid(True)

plt.xlabel('Time', fontsize=16)
plt.ylabel('Flux', fontsize=16)

a = Annotate()  #the rectangle
cursor = Cursor(ax, useblit=True, color='black', linewidth=2)  #the crosshair

callback = Index()  #button handler
togglePlacement = plt.axes([0.65, 0.05, 0.3, 0.055])
rectToggle = Button(togglePlacement, 'Rectangle Select Toggle')
rectToggle.on_clicked(callback.toggle)

selectDataPlacement = plt.axes([0.45, 0.05, 0.15, 0.055])
selectData = Button(selectDataPlacement, 'Select Data')
selectData.on_clicked(callback.select)

savePlacement = plt.axes([0.1, 0.05, 0.1, 0.055])
saveData = Button(savePlacement, 'Save')
saveData.on_clicked(callback.saveFile)

toggle_selector.RS = RectangleSelector(ax, onselect, drawtype='line')
toggle_selector.RS.set_active(False)

plt.grid(True)

plt.show()