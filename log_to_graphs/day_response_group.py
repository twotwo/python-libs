#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================
Paint Daily Response in Group
=============================

Copyright (c) 2017年 li3huo.com All rights reserved.
"""
import numpy as np
import matplotlib.pyplot as plt

from numpy_helper import Helper

import sys, os

def paint_horizantal_bar_chart(group_name, date_str, resp_group, resp_group_err):
	"""Make a horizontal bar plot
	"""
	height = 0.35       # the height of the bars
	labels = ('Average Response Time(ms)', 'Last 100 Response Time(ms)')
	groups = resp_group.keys() # tag name
	ind = np.arange(len(groups))  # the y locations for the groups

	#开启网格
	plt.grid()
	# fig, ax = plt.subplots()
	fig = plt.figure(figsize=(12, 12))
	ax = fig.add_subplot(111)
	# add some text for labels, title and axes ticks
	ax.set_ylabel(group_name)
	ax.set_title('Response Time group by %s(%s)' % (group_name, date_str))
	ax.set_yticks(ind + height / 2)
	ax.set_yticklabels(groups)

	# rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std, label='Men')
	# mean of all
	performance = [np.mean(resp) for resp in resp_group.values()]
	error = [len(err) for err in resp_group_err.values() ]

	for rect in ax.barh(ind, performance, height, color='g', label=labels[0]):
		lenth = int(rect.get_width())
		x = rect.get_width()
		if x < 500 : x = 500
		ax.text(x, rect.get_y() + height/2.,
				'%d' % lenth,
				horizontalalignment='right',
				verticalalignment='center')

	# rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std, label='Women')
	# mean of last 100
	resps_sorted = [np.sort(resp) for resp in resp_group.values() ]
	performance = [np.mean(resp[-100:]) for resp in resps_sorted]
	for rect in ax.barh(ind + height, performance, height, color='r', label=labels[1]):
		lenth = int(rect.get_width())
		x = rect.get_width()
		if x < 500 : x = 500
		ax.text(x, rect.get_y() + height/2.,
				'%d' % lenth,
				horizontalalignment='right',
				verticalalignment='center')

	plt.legend( loc='best', fontsize='small' )

	counts = ['all: %d\nerr: %d'%(len(resp),len(err)) for resp, err in zip(resp_group.values(), resp_group_err.values())]
	# Set the right-hand Y-axis ticks and labels
	ax2 = ax.twinx()
	# set the tick locations
	ax2.set_yticks(ind)
	# make sure that the limits are set equally on both yaxis so the
	# ticks line up
	ax2.set_ylim(ax.get_ylim())
	# set the tick labels
	ax2.set_yticklabels(counts)
	ax2.set_ylabel('All Response')
	ax2.yaxis.grid(True, which="both", color='k', linestyle='-.', linewidth=0.7)

	# plt.show()
	date_str=''
	plt.savefig('channel_auth_%s.png'%date_str, dpi = 300)
	print 'save as channel_auth_%s.png'%date_str

def test(date_str):
	helper = Helper('helper.ini', 'agent')
	log_file = 'logs/perf.log.'+date_str
	cmd = """grep "/api/LoginAuth/" %s | sed -n 's/.*ch=\\(.*\\), code=\\([0-9]\\+\\).*w = \\(.*\\)s/\\1 \\3 \\2/p'"""% log_file
	print 'cmd =',cmd
	(resp_group, resp_group_err) =Helper.parse_response_groupbytag(
		cmd, 
		'string',
		ignore_err=False)
	# data =Helper.load('agent.npz')

	group_name = 'Channels'
	paint_horizantal_bar_chart(group_name, date_str, resp_group, resp_group_err)

def main(argv):
	ini_file = 'helper.ini'
	section = 'agent'
	if len(argv) > 1: ini_file = argv[1]
	if len(argv) > 2: section = argv[2]
		
	print 'config file =', ini_file
	if not os.path.exists(ini_file):
		# use ini in python dir
		ini_file=os.path.join(os.path.abspath(os.path.dirname(argv[0])),ini_file)
		print('try to use another place', ini_file)
	helper = Helper(ini_file, section)
	(resp_group, resp_group_err) =Helper.parse_response_groupbytag(
		helper.auth_resp_groupby_ch_cmd, 
		helper.cost_type,
		ignore_err=False)

	paint_horizantal_bar_chart('Channels', helper.yesterday, resp_group, resp_group_err)

if __name__ == '__main__':
	# for date in ['2017-09-19', '2017-09-20', '2017-09-21', '2017-09-22', '2017-09-23', '2017-09-24', '2017-09-25', '2017-09-26']:
	# # for date in ['2017-09-19']:
	# 	test(date)
	main(sys.argv) # python day_response_group.py helper.ini platform