#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt


x1 = np.arange(24)
y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)

x2 = np.arange(24)
y2 = np.cos(2 * np.pi * x2)

x3 = np.arange(24)
y3 = [0] * 24


# init the figure
fig = plt.figure()

# picture title
fig.suptitle('A tale of 3 subplots', fontsize=16, fontweight=900)

# the width of the bars
width = 0.35

axes = plt.subplot(3,1,1)
plt.grid()
plt.plot(x1, y1, 'b')
bars = axes.bar(x1+width, y1, width, label=u'All Requests', color='g')
# attach some text labels
for bar in bars:
	height = bar.get_height()
	axes.text(bar.get_x() + bar.get_width()/2., 1.05*height,
			'%d' % int(height), ha='center', va='bottom')
plt.ylabel('Daily Processes by Hours')


plt.subplot(3, 1, 2)
plt.grid()
plt.plot(x2, y2, 'ko-')
plt.ylabel('Damped oscillation')

plt.subplot(3, 1, 3)
plt.grid()
plt.plot(x3, y3, 'r.-')
plt.ylabel('Undamped')

plt.xlabel('time (s)')



plt.show()
