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
from datetime import date, timedelta

from subprocess import Popen, PIPE
import numpy as np

def log(info):
	logging.info(info)
	print info

class Helper(object):
	def __init__(self, npz_file):
		self.npz_file = npz_file

	@staticmethod
	def parse(config_file, section, save=False):
		"""根据配置文件中的配置信息，读取日志，分析出用于出图的数据
		"""
		# yesterday
		timestamp = ( date.today()-timedelta(1) ).strftime('%Y-%m-%d')

		config = ConfigParser.ConfigParser()
		config.read(config_file)
		npz_file = config.get(section, 'npz_file')
		log_file = config.get(section, 'log_file', 0, {'timestamp': timestamp})
		request_cmd = config.get(section, 'request_cmd', 0, {'log_file': log_file})

		log( 'npz_file = %s, log_file = %s'% (npz_file,log_file) )
		log( 'request_cmd = %s'% request_cmd )

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


	def load_npz_data(self):
		"""
		load data from self.npz_file(.npz format file)
		"""
		with np.load(self.npz_file) as data:

			try:
				self.day_requests = data['day_requests']
			except:
				log('npz_to_data: failed to load day_requests!')
				self.day_requests = None

			try:
				self.day_resp_time_by_hour = data['day_resp_time_by_hour']
			except:
				log('npz_to_data: failed to load day_resp_time_by_hour!')
				self.day_resp_time_by_hour = None

			try:
				self.day_resp_err_by_hour = data['day_resp_err_by_hour']
			except:
				log('npz_to_data: failed to load day_resp_err_by_hour!')
				self.day_resp_err_by_hour = None

	def __parse_responses(self, file):
		"""根据日志具体格式，获取对应的响应时间和服务状态
		"""
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

	parser.add_argument('-c', dest='cmd', type=str, default='parse', choices=['parse', 'load'], 
											help='command for helper')
	parser.add_argument('-i', dest='ini', type=str, default='helper.ini',
											help='NumPy binary file')
	parser.add_argument('-s', dest='section', type=str, default='agent',
											help='section in .ini file')
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

	save=True
	if args.dry_run: 
		print 'in dry-run mode'
		save=False

	if args.cmd == 'parse':
		log( 'parse for %s [%s]'% (args.ini, args.section) )
		Helper.parse(args.ini, args.section, save=save)
	elif args.cmd == 'load':
		print 'load from ', args.npz
		helper = Helper(args.npz)
		helper.load_npz_data()
		if args.verbose:
			print len(helper.day_requests), len(helper.day_resp_time_by_hour), len(helper.day_resp_err_by_hour)
			print 'day_requests[0:60] =', helper.day_requests[0:60]
			print '================ day_resp_time_by_hour[0:23] ================'
			for resp in helper.day_resp_time_by_hour:
				print len(resp), resp[0:10], '...'
			print '================ day_resp_err_by_hour[0:23] ================'
			for resp in helper.day_resp_err_by_hour:
				print len(resp), resp[0:10], '...'

if __name__ == '__main__':
	"""python numpy_helper.py -h
python numpy_helper.py -c parse -i helper.ini -s agent # parse log & save data
python numpy_helper.py -c load -n agent.npz -v #load from data.npz
"""
	main()

