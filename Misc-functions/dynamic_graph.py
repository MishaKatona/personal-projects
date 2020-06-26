# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

x = 100
y = 100

plt.ion()
ax = plt.gca()
plt.xlim(-60, 200)
plt.ylim(-50, 1000)
ax.plot([0,200],[0,0])
ax.plot([0,0],[0,1000])
line, = ax.plot(x, y, "ro")
yt = 50
xt = 0


for i in range(80):
    line.set_ydata(y)
    line.set_xdata(x)
    plt.draw()
    if y >= 1000:
        y = 1000
        xt = -3
        yt = - yt
    if x < 0:
        x = 0
        xt = -xt
    if y < 0:
        y = 0
        yt= -yt
    y += yt
    x += xt
    plt.pause(0.1)