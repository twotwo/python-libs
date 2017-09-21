#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
daily_log_plot.py
parse day log to 3 figs: 1. requests count; 2. requests throughput; 3. responses time

Copyright (c) 2016年 li3huo.com All rights reserved.
"""

import argparse,logging
from subprocess import Popen, PIPE

import numpy as np
import matplotlib.pyplot as plt

# labels = (u'0点', u'1点', u'2点', u'3点', u'4点', u'5点', u'6点', u'7点', u'8点', u'9点', u'10点', u'11点', u'12点',
# 	u'13点', u'14点', u'15点', u'16点', u'17点', u'18点', u'19点', u'20点', u'21点', u'22点', u'23点'
# 	)
labels = []
N = 24

def sample_by_group(requests, n):
	"""最大值/中位值/平均值/最小值 max/median/mean/min
	根据n值取一个区间的四种数值
"""	
	max_count = []
	median_count = []
	mean_count = []
	min_count = []

	num = 0
	group = []
	for c in requests:
		num += 1
		group.append(c)
		
		if num % n == 0:
			max_count.append(np.max(group))
			median_count.append(np.median(group))
			mean_count.append(np.mean(group))
			min_count.append(np.min(group))
			group = []

	return (max_count, median_count, mean_count, min_count)


def autolabel(bars, axes):
	# attach some text labels
	for bar in bars:
		height = bar.get_height()
		if '%f' % float(height) == 'nan': height = 0
		axes.text(bar.get_x() + bar.get_width()/2., 1.05*height,
				'%d' % int(height), ha='center', va='bottom')

def text(axes, xs, ys, values):
	for x, y, value in zip(xs, ys, values):
		axes.text(x, 1.05*y, '%d' % int(value), fontsize=10, fontweight=800, bbox=dict(facecolor='green', alpha=0.8),
			ha='right', va='baseline')

def paint(helper, picturename, title, show=True):

	for i in range(N):	# init x labels
		labels.append( str(i)+':00' )

	width = 0.35        # the width of the bars

	day_requests = helper.day_requests
	day_resp_time_by_hour = helper.day_resp_time_by_hour
	resp_errs = helper.day_resp_err_by_hour


	##################################################
	# Plot to Chart
	##################################################
	group = 60
	fig = plt.figure(figsize=(15, 15))
	# plt.style.use('classic')
	# 设置图的底边距
	plt.subplots_adjust(bottom = 0.15)
	#开启网格
	plt.grid()
	# picture title
	fig.suptitle(title, fontsize=16, fontweight=900)

	##################################################
	# subplot 1: 
	##################################################
	count_by_hours = []
	for a in np.array(day_requests).reshape(24, 60*60):
		count_by_hours.append(np.sum(a))

	axes = plt.subplot(3,1,1)
	bars1 = axes.bar(np.arange(24)+width, count_by_hours, width, label=u'All Requests', color='g')
	autolabel(bars1, axes)

	if resp_errs.any() != None:
		bars2 = axes.bar(np.arange(24)+width*2, [len(err) for err in resp_errs], width, label=u'Errors', color='r')
		autolabel(bars2, axes)

	plt.ylabel('Daily Processes by Hours')
	plt.xticks(np.arange(24), labels)
	
	
	plt.legend( loc='best', fontsize='x-small' )


	#####################################################
	# subplot 2: plot throughput by helper.day_requests
	#####################################################
	(max_count, median_count, mean_count, min_count) = sample_by_group(helper.day_requests, 60)

	plt.subplot(3, 1, 2)
	plt.plot(np.arange(group * 24), max_count, label=u'Max Requests', color='r')
	plt.plot(np.arange(group * 24), median_count, label=u'Median Requests', color='g')
	plt.plot(np.arange(group * 24), mean_count, label=u'Mean Requests', color='y')
	plt.plot(np.arange(group * 24), min_count, label=u'Min Requests', color='b')
	plt.xlabel('time (h)')
	plt.ylabel('Daily Throughput(requests/s)')

	# the x locations for one day: 24 * group
	ind = list(xrange(0, 24 * group, group))
	plt.xticks(ind, labels)
	plt.legend( loc='best', fontsize='x-small' )

	#####################################################
	# subplot 3: plot response time by helper.day_responses
	#####################################################
	if day_resp_time_by_hour.any() != None:
		# Sorted by Response Time
		resps_sorted = [np.sort(resp) for resp in day_resp_time_by_hour]

		axes = plt.subplot(3, 1, 3)
		bars1 = axes.bar(np.arange(24), [np.mean(resp[-1000:]) for resp in resps_sorted], width, label=u'Last 1000', color='g')
		bars2 = axes.bar(np.arange(24)+width, [np.mean(resp[-100:]) for resp in resps_sorted], width, label=u'Last 100', color='b')
		bars3 = axes.bar(np.arange(24)+width*2, [np.mean(resp[-10:]) for resp in resps_sorted], width, label=u'Last 10', color='r')
		plt.ylabel('Average Response Time(ms)')
		plt.xticks(np.arange(24), labels)
		autolabel(bars1, axes)
		autolabel(bars2, axes)
		autolabel(bars3, axes)
		plt.legend( loc='best', fontsize='x-small' )


	#自动调整label显示方式，如果太挤则倾斜显示
	fig.autofmt_xdate()

	plt.savefig(picturename)
	logging.info('save to %s' % picturename)


	if show: plt.show()

def main():
	parser = argparse.ArgumentParser(description='Create Bar Chart from log.')

	parser.add_argument('-n', dest='npz', type=str, default='data.npz',
											help='NumPy binary file')
	parser.add_argument('-t', dest='title', type=str, default='Project xx on Date yy',
											help='the image title')
	parser.add_argument('-p', dest='picturename', type=str, default='request.png',
											help='The name of the chart picture.')
	parser.add_argument('--show', dest='show', action='store_true')
	parser.add_argument('--not-show', dest='show', action='store_false')
	parser.set_defaults(show=True)

	args = parser.parse_args()

	##################################################
	# Load Response Data
	##################################################
	# requests = load_requests(file)
	from numpy_helper import Helper
	logging.basicConfig(filename='./l2g.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

	helper = Helper(args.npz)
	helper.load_npz_data()

	paint(helper, picturename=args.picturename, title=args.title, show=args.show)

if __name__ == '__main__':
	'''
	python daily_log_plot.py -h
	python daily_log_plot.py -n agent.npz -p agent.png --not-show -t "Project SDK-Agent on Date 2017-05-02"
	'''
	main()

	