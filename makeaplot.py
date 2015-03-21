import numpy as np
import matplotlib.pyplot as plt
import csv

time = []
least = []
most = []
for x in range(0, 4):
    least.append([])
    most.append([])

f = open("time.csv")
for row in csv.reader(f):
    print row
    time.append(row)

f2 = open("data.csv")
for row in csv.reader(f2):
    for i in range(0,4):
        least[i].append(row[i])
        most[i].append(row[4+i])


plt.subplot(2,1,1)
for p in range(0,3):
    plt.plot(time[0], least[p], 'r')

plt.subplot(2,1,2)
plt.plot(time[0], most[0], 'r')
plt.plot(time[0], most[1], 'b')
plt.plot(time[0], most[2], 'g')
plt.plot(time[0], most[3], 'y')

plt.show()
