# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import genetic

x,y,z = [0],[0],[0]

plt.ion()
ax = plt.gca()
xmax = 5
ymax = 10
plt.xlim(0, xmax)
plt.ylim(0, ymax)
line, = ax.plot(x, y, "ro-",)
line2, = ax.plot(x,z,"bo-")

num_iterations = 150
runs = 1
wait = 120

weights = genetic.init(100,[-0.5,0.5])

for i in range(num_iterations):
    fitnes,scores = genetic.iteration(weights,runs,wait)
    weights = genetic.evolution(weights,fitnes)
    max_score = max(scores) - 4
    avg_score = sum(scores)/len(scores) - 4

    xmax+=1
    x.append(x[-1]+1)
    y.append(max_score)
    z.append(avg_score)

    if y[-1]+2 > ymax:
        ymax = y[-1]+2
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    line.set_ydata(y)
    line.set_xdata(x)
    line2.set_ydata(z)
    line2.set_xdata(x)
    plt.draw()
    plt.pause(0.2)