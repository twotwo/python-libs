#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
a bar plot with errorbars

http://matplotlib.org/examples/api/barchart_demo.html
"""
import numpy as np
import matplotlib.pyplot as plt

N = 24

labels = (u'0点', u'1点', u'2点', u'3点', u'4点', u'5点', u'6点', u'7点', u'8点', u'9点', u'10点', u'11点', u'12点',
	u'13点', u'14点', u'15点', u'16点', u'17点', u'18点', u'19点', u'20点', u'21点', u'22点', u'23点'
	)

menMeans = (20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35)
menStd =  (13, 15, 20, 15, 17, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots(figsize=(12, 5))
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200)
womenStd = (3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3)
rects2 = ax.bar(ind + width, womenMeans, width, color='y', yerr=womenStd)

# add some text for labels, title and axes ticks
ax.set_ylabel(u'毫秒数')
ax.set_title(u'服务响应时间')
ax.set_xticks(ind + width)
ax.set_xticklabels(labels)

# add handles' lables
ax.legend((rects1[0], rects2[0]), (u'Means', u'Last10%'))


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

# plt.savefig('bar.png')
plt.show()
