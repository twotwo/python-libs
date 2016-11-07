#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
numpy_helper.py
load and save day log data

https://docs.scipy.org/doc/numpy-dev/reference/routines.io.html

Copyright (c) 2016年 li3huo.com All rights reserved.
"""
from subprocess import Popen, PIPE

import numpy as np

class Helper(object):
	def __init__(self, log_file, npz_file):
		self.log_file = log_file
		self.npz_file = npz_file

	def log_to_data(self):
		"""
		parse data from log file and save data to .npz format file
		"""
		self.day_requests = self.__parse_requests(self.log_file)
		(self.day_responses, self.day_responses_err) = self.__parse_responses(self.log_file)

		np.savez(self.npz_file, day_requests=self.day_requests, 
			day_responses=self.day_responses,
			day_responses_err=self.day_responses_err)

	def npz_to_data(self):
		"""
		load data from .npz format file
		"""
		with np.load(self.npz_file) as data:
			self.day_requests = data['day_requests']
			self.day_responses = data['day_responses']
			self.day_responses_err = data['day_responses_err']

	def __parse_requests(self, file):
		"""
		parse log requests
		return throughput each second
		"""
		# 1  23:59:59
		cmd='cut -c11-19 %s |sort | uniq -c' % file
		return Helper.parse_requests(cmd)

	@staticmethod
	def parse_requests(cmd):
		"""
		parse log requests through cmd
		return throughput each second

		ssh 10.75.1.12 -p 2188 "cut -c11-19 /data/logs/fusdk-rsyslog/fusdkhttp.2016-11-06.log |sort | uniq -c"
		#FUSDK
		"""
		day_requests = []
		
		buff = {}
		for line in Popen(cmd, shell=True, bufsize=102400, stdout=PIPE).stdout:
			try:
				buff[line.strip().split()[1]] = line.strip().split()[0]
			except IndexError as e:
				print 'IndexError', e.message,  len(line.strip().split()), 'line =',line.strip().split()
			except ValueError as e:
				print 'ValueError', e.message,  'line=[', line, ']'
				# break
		for h in range(24):
			for m in range(60):
				for s in range(60):
					if buff.has_key( '%02d:%02d:%02d' % (h, m, s) ):
						day_requests.append( int(buff['%02d:%02d:%02d' % (h, m, s)]) )
					else:
						day_requests.append(0)

		return day_requests

	def __parse_responses(self, file):
		day_responses = {}
		day_responses_err = {}
		# init hours
		for i in range(24):
			day_responses[i] = []
			day_responses_err[i] = []

		# int( line.split('\x02')[0][11:13] )
		# int( line.split('\x02')[7] ) // 响应时间(ms)
		# int( line.split('\x02')[8] ) //服务状态
		with open(file) as f:
			for line in f:
				try:
					hour = int( line.split('\\x02')[0][11:13] )
					cost = int( line.split('\\x02')[7] )
					day_responses[hour].append(cost)
					code = int( line.split('\\x02')[8] )
					if code != 0:
						day_responses_err[hour].append( [code, cost] )
					else:
						day_responses_err[hour].append([0,0])
				except IndexError as e:
					print 'IndexError', e.message,  len(line.split('\\x02')), 'line =',line.split('\\x02')
				except ValueError as e:
					print 'ValueError', e.message,  'line=[', line, ']'
				# break
		resp = []
		resp_err = []
		for i in range(24):
			resp.append(day_responses[i])
			resp_err.append(len(day_responses_err[i])>0 and day_responses_err[i] or [0,0])
		return resp, resp_err

if __name__ == '__main__':
	helper = Helper('pay_perform.log.20161106', 'monkey.npz')
	
	helper.log_to_data()
	# print len(helper.day_requests), len(helper.day_responses), len(helper.day_responses_err)
	# helper.npz_to_data()
	print len(helper.day_requests)
	print [len(resp) for resp in helper.day_responses]
	print [np.sum(err[0]) for err in helper.day_responses_err]