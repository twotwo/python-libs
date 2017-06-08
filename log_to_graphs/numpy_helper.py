#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
numpy_helper.py
load and save day log data

https://docs.scipy.org/doc/numpy-dev/reference/routines.io.html

Copyright (c) 2016年 li3huo.com All rights reserved.
"""
import argparse, logging
import ConfigParser
from datetime import date

from subprocess import Popen, PIPE
import numpy as np

class Helper(object):
	def __init__(self, npz_file):
		self.npz_file = npz_file
		self.day_responses = []
		self.day_responses_err = []

	@staticmethod
	def parse(config_file, section, save=False):
		"""根据配置文件中的配置信息，读取日志，分析出用于出图的数据
		"""
		config = ConfigParser.ConfigParser()
		config.read(config_file)
		npz_file = config.get(section, 'npz_file')
		log_file = config.get(section, 'log_file', 0, {'timestamp': date.today().strftime('%m%d')})
		request_cmd = config.get(section, 'request_cmd', 0, {'log_file': log_file})

		print 'npz_file = ', npz_file
		print 'log_file = ', log_file
		print 'request_cmd = ', request_cmd

		day_requests = Helper.parse_requests(request_cmd)
		(resp_time, resp_err) = Helper.parse_response_by_hour(log_file)

		if save:
			np.savez(npz_file, day_requests=day_requests, 
				day_resp_time_by_hour=resp_time,
				day_resp_err_by_hour=resp_err)

	@staticmethod
	def parse_requests(cmd):
		"""
		命令获取 “计数 时:分:秒”结构的数据
		记录24小时中每秒的请求数量；生成一个长度为86400的一维数组
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

	@staticmethod
	def parse_response_by_hour(file):
		"""按小时解析请求的响应速度(last 1000/100/10)和失败数量
		"""
		#### log format
		# 20170502235959, 10.163.29.39, [/api/LoginAuth/] [ch=UC, code=0] r = 0.000s, p = 0.166s, w = 0.166s
		#### parse to
		# int( line[8:10] ) //小时
		# float( line.split('w = ')[1][0:-1] ) * 1000 // 响应时间(ms)
		# int( line.find('code=0')>0 and '0' or 1 ) //服务状态: 0 成功，其余失败

		day_responses = {}
		day_responses_err = {}
		# init hours
		for i in range(24):
			day_responses[i] = []
			day_responses_err[i] = []

		with open(file) as f:
			for line in f:
				try:
					# hour = int( line.split('\\x02')[0][11:13] )
					# cost = int( line.split('\\x02')[7] )
					# day_responses[hour].append(cost)
					# code = int( line.split('\\x02')[8] )
					hour = int( line[8:10] )
					cost = line.split('w = ')[1].strip('\n')[0:-1]
					try:
						cost = float( cost ) * 1000
					except ValueError as e:
						cost = float( cost.split(':')[-1] ) * 1000
					day_responses[hour].append(cost)
					code = int( line.find('code=0')>0 and '0' or 1 )
					if code != 0:
						day_responses_err[hour].append( [code, cost] )
					else:
						day_responses_err[hour].append([0,0])
				except IndexError as e:
					print 'IndexError:', e.message,  len(line.split('\\x02')), 'line =',line.split('\\x02')
				except ValueError as e:
					print 'ValueError:', e.message,  'line=[', line, ']'
					print 'cost=',line.split('w = ')[1].strip('\n')[0:-1]

				# break
		resp_time = []
		resp_err = []
		for i in range(24):
			resp_time.append(day_responses[i])
			resp_err.append(len(day_responses_err[i])>0 and day_responses_err[i] or [0,0])
		return resp_time, resp_err

	@staticmethod
	def load_requests(args):
		"""记录24小时中每秒的请求数量；长度为86400的一维数组
		"""
		if args.log != None or args.cmd != None :
			# load requst from file
			cmd='cat %s' % args.log
			if args.cmd != None: cmd = args.cmd
			day_requests = Helper.parse_requests(cmd)

			return day_requests

		elif args.dest != None:
			# load requst from npz
			with np.load(args.dest) as data:
				return data['day_requests']
				# self.day_responses = data['day_responses']
				# self.day_responses_err = data['day_responses_err']
		else:
			logging.warn('load_requests: set src or dest for load!')
			print 'load_requests: set src or dest for load!'

	def load_response_status_by_hour(self, file):
		"""按小时解析请求的响应时间和失败数量
		"""
		# 20170502235959, 10.163.29.39, [/api/LoginAuth/] [ch=UC, code=0] r = 0.000s, p = 0.166s, w = 0.166s
		# int( line[8:10] ) //小时
		# float( line.split('w = ')[1][0:-1] ) * 1000 // 响应时间(ms)
		# int( line.find('code=0')>0 and '0' or 1 ) //服务状态: 0 成功，其余失败

		# init hours
		for i in range(24):
			day_responses[i] = []
			day_responses_err[i] = []

		with open(file) as f:
			for line in f:
				try:
					# hour = int( line.split('\\x02')[0][11:13] )
					# cost = int( line.split('\\x02')[7] )
					# day_responses[hour].append(cost)
					# code = int( line.split('\\x02')[8] )
					hour = int( line[8:10] )
					cost = float( line.split('w = ')[1].strip('\n')[0:-1] ) * 1000
					day_responses[hour].append(cost)
					code = int( line.find('code=0')>0 and '0' or 1 )
					if code != 0:
						day_responses_err[hour].append( [code, cost] )
					else:
						day_responses_err[hour].append([0,0])
				except IndexError as e:
					print 'IndexError:', e.message,  len(line.split('\\x02')), 'line =',line.split('\\x02')
				except ValueError as e:
					print 'ValueError:', e.message,  'line=[', line, ']'
				# break
		self.day_responses = []
		self.day_responses_err = []
		for i in range(24):
			self.day_responses.append(day_responses[i])
			self.day_responses_err.append(len(day_responses_err[i])>0 and day_responses_err[i] or [0,0])
		

	def save_npz_file(self, npz_file):
		np.savez(npz_file, day_requests=self.day_requests, 
			day_responses=self.day_responses,
			day_responses_err=self.day_responses_err)

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

			try:
				self.day_requests = data['day_requests']
			except:
				logging.warn('npz_to_data: failed to load day_requests!')
				print 'npz_to_data: failed to load day_requests!'
				self.day_requests = None

			try:
				self.day_resp_time_by_hour = data['day_resp_time_by_hour']
			except:
				logging.warn('npz_to_data: failed to load day_resp_time_by_hour!')
				print 'npz_to_data: failed to load day_resp_time_by_hour!'
				self.day_resp_time_by_hour = None

			try:
				self.day_resp_err_by_hour = data['day_resp_err_by_hour']
			except:
				logging.warn('npz_to_data: failed to load day_resp_err_by_hour!')
				print 'npz_to_data: failed to load day_resp_err_by_hour!'
				self.day_resp_err_by_hour = None
			

	def __parse_requests(self, file):
		"""
		parse log requests
		return throughput each second
		"""
		# 1  23:59:59
		cmd='cut -c11-19 %s |sort | uniq -c' % file
		return Helper.parse_requests(cmd)



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

def main():
	parser = argparse.ArgumentParser(prog='Numpy Helper', usage='%(prog)s [options]')
	parser.add_argument('-a', dest='app', type=str, default='qzgs',
											help='the apk name')
	parser.add_argument('-t', dest='type', type=str, default='request',
											help='Data Parsing Type')
	parser.add_argument('-l', dest='log', type=str, default=None,
											help='read from log file')
	parser.add_argument('-c', dest='cmd', type=str, default=None,
											help='read from command')
	parser.add_argument('-n', dest='npz', type=str, default='data.npz',
											help='NumPy binary file')
	parser.add_argument('-v', dest='verbose', action='store_true',
											help='List Data in NumPy binary file')
	# parser.add_argument('-h', dest='help', type=bool, default=False,
	# 										help='print help')
	parser.add_argument('--dry-run', dest='dry_run', action='store_true',
											help='Dry Run Mode: do not excute time-consuming operation')
	parser.set_defaults(verbose=False)
	parser.set_defaults(dry_run=False)
	# config a log
	logging.basicConfig(filename='./l2g.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

	args = parser.parse_args()

	# print "source : " + args.log
	# print "dest : " + args.dest
	# print "cmd : " + args.cmd
	if args.dry_run: print 'in dry-run mode'

	Helper.parse('helper.ini', 'agent', save=True)

	print 'NumPy binary file = ', args.npz
	helper = Helper(args.npz)
		
	# if 'request' == args.type:
	# 	helper.day_requests = helper.load_requests(args)

	# 	helper.save_npz_file(args.npz)
	# elif 'load' == args.type:
	# 	pass
	
	# if args.verbose:
	# 	print len(helper.day_requests)
	# 	if len(helper.day_requests) > 60:
	# 		# each column in the first 60 rows
	# 		print helper.day_requests[0:60]
	# 	print helper.day_requests[-1]

"""
python numpy_helper.py -t request -l logs/perf_20170502.log -v #load from file
python numpy_helper.py -t request -c 'cat logs/perf_20170502.log' -v #load from cmd
python numpy_helper.py -t request -c "awk '{print substr($0,9,2)":"substr($0,11,2)":"substr($0,13,2) }' logs/perf_20170518.log |sort | uniq -c" -v #load from cmd
python numpy_helper.py -t request -n data.npz -v #load from data.npz
"""
if __name__ == '__main__':
	main()

	# req_per_second.cmd=awk '{print substr($0,9,2)":"substr($0,11,2)":"substr($0,13,2) }' perf.log |sort | uniq -c
	# 
	
	# helper.log_to_data()
	# # print len(helper.day_requests), len(helper.day_responses), len(helper.day_responses_err)
	# # helper.npz_to_data()
	# print len(helper.day_requests)
	# print [len(resp) for resp in helper.day_responses]
	# print [np.sum(err[0]) for err in helper.day_responses_err]