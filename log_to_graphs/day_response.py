#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
day_response.py
a bar plot for day log response

http://matplotlib.org/examples/api/barchart_demo.html

Copyright (c) 2016年 li3huo.com All rights reserved.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

# labels = (u'0点', u'1点', u'2点', u'3点', u'4点', u'5点', u'6点', u'7点', u'8点', u'9点', u'10点', u'11点', u'12点',
# 	u'13点', u'14点', u'15点', u'16点', u'17点', u'18点', u'19点', u'20点', u'21点', u'22点', u'23点'
# 	)
labels = []


N = 24



def load_resposne(file):
	day_response = {}
	# init hours
	for i in range(N):
		day_response[i] = []
		labels.append( str(i)+':00' )

	# int( line.split('\x02')[0][11:13] )
	# int( line.split('\x02')[7] ) // 响应时间(ms)
	# int( line.split('\x02')[8] ) //服务状态
	with open(file) as f:
		for line in f:
			try:
				hour = int( line.split('\\x02')[0][11:13] )
				day_response[hour].append(int( line.split('\\x02')[7] ))
			except IndexError as e:
				print 'IndexError', e.message,  len(line.split('\\x02')), 'line =',line.split('\\x02')
			except ValueError as e:
				print 'ValueError', e.message,  'line=[', line, ']'
			# break
	return day_response

def range_mean(array, n):
	"""
	响应速度排序，分段中值
	举例：最慢的5% n=.95
	"""
	index = int( len(array) * n )
	sorted_array = np.sort(array)
	return np.mean(sorted_array[index:]), np.std(sorted_array[index:])

# respMeans = (20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35)
# menStd =  (13, 15, 20, 15, 17, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35, 27, 20, 35, 30, 35)
# rangeMeans = (250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200, 100, 250, 302, 300, 200)
# rangeStd = (3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3, 3, 3, 5, 2, 3)


def autolabel(bars, axes):
	# attach some text labels
	for bar in bars:
		height = bar.get_height()
		axes.text(bar.get_x() + bar.get_width()/2., 1.05*height,
				'%d' % int(height),
				ha='center', va='bottom')

def text(axes, xs, y, values):
	for x, value in zip(xs, values):
		axes.text(x, y, '%d' % int(value), fontsize=8, bbox=dict(facecolor='blue', alpha=0.1),
			ha='center', va='bottom')

def paint(file, picturename='bar.png', show=True):

	##################################################
	# Load Response Data
	##################################################
	day_response = load_resposne(file)

	##################################################
	# Calculate Needed Values
	##################################################
	respMeans = []
	respStd = []
	rangeMeans = []
	rangeStd = []

	respCount = []
	errorCount = []

	for i in range(N):
		# respMeans.append(np.median(day_response[i]))
		# respStd.append(np.std(day_response[i]))
		m, s = range_mean(day_response[i], 0.995)
		respMeans.append(m)
		respStd.append(s)
		# m, s = range_mean(day_response[i], 0.998)
		# rangeMeans.append(m)
		# rangeStd.append(s)
		rangeMeans.append(np.max(day_response[i]))
		print i, (np.median(day_response[i]),np.std(day_response[i]) ), range_mean(day_response[i], 0.995), np.max(day_response[i]), len(day_response[i])

	for i in range(N):
		respCount.append(np.sum(day_response[i]))

	##################################################
	# Plot to Bar Chart
	##################################################
	plt.style.use('fivethirtyeight')
	ind = np.arange(N)  # the x locations for the groups
	width = 0.35        # the width of the bars

	fig, ax = plt.subplots(figsize=(18, 5))
	bars1 = ax.bar(ind, respMeans, width, color='r', yerr=respStd)


	bars2 = ax.bar(ind + width, rangeMeans, width, color='y')

	# add some text for labels, title and axes ticks
	ax.set_ylabel(u'Response Time(ms)')
	ax.set_title(u'Monkey Daily Response Log')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(labels)

	# add handles' lables
	ax.legend((bars1[0], bars2[0]), (u'99.5% Means', u'Max Resp Time'), loc='best', fontsize='x-small')

	autolabel(bars1, ax)
	autolabel(bars2, ax)
	height = np.max(rangeMeans) * 0.85
	text(ax, ind + width, height, respCount)

	plt.savefig(picturename)
	if show: plt.show()

def main():
	parser = argparse.ArgumentParser(description='Create Bar Chart from log.')
	parser.add_argument('-f', dest='logfile', type=str, default='',
											help='the sdk log file')
	parser.add_argument('-p', dest='picturename', type=str, default='chart.png',
											help='The name of the chart picture.')
	parser.add_argument('--show', dest='show', action='store_true')
	parser.add_argument('--not-show', dest='show', action='store_false')
	parser.set_defaults(show=True)

	args = parser.parse_args()

	print "logfile: " + args.logfile
	print "picturename: " + args.picturename

	paint(file=args.logfile, picturename=args.picturename, show=args.show)

if __name__ == '__main__':
	'''
	python day_response.py -f sdk_perform.log -p bar.png
	python2 day_response.py -f /data/monkey-rsyslog/perfom.2016-10-19.log -p monkey-sdk-response.png
	'''
	main()
	# paint(file='sdk_perform.log')