# -*- coding: utf8 -*-

import time #计算命令执行时长
import subprocess, codecs, os
from datetime import date

class Result(object):
	def __init__(self, cmd, out, err, titles, raws, cost_time):
		self.cmd = cmd
		self.out = out
		self.err = err
		self.titles = titles
		self.raws = raws
		self.cost_time = cost_time

	def __str__(self):
		return 'Result(%s [%s]s): \n%s\n%s'% (self.cmd, self.cost_time, self.out, self.err)

class CommandUtil(object):

	@staticmethod
	def gen_command(devID, lines):
		'''生成要执行的查询命令
		'''
		log_file = date.today().strftime('/data/logs/fltranslog/%Y-%m-%d.log')
		if not os.access(log_file, os.F_OK):
			log_file = '~/app/python/web/web.py/2016-07-27.log'

		match = ''
		if devID:
			match = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($20=="%s") print $0}\'' % devID # print all match columns
			if not lines: lines = '5000'
		else:
			lines = '100'
		
		return 'tail -n%s %s %s|awk -f trimcells.awk' % (lines, log_file, match)

	@staticmethod
	def excute(devID=None, lines='100'):
		start_point = time.time()
		cmd = CommandUtil.gen_command(devID, lines)
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out, err = process.communicate()

		titles = [u'EventID', u'Log Time', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS','IP Addr', u'MacAddr', u'DevID', u'AccountID', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName',]
		raws = [line.split(',') for line in codecs.decode(out, 'utf-8').split('\n')]

		return Result(cmd, out, err, titles, raws, time.time()-start_point)

if __name__ == '__main__':
	print CommandUtil.excute()