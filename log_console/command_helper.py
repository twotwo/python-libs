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
	def gen_command(dev_id, app_id, columns, lines):
		'''生成要执行的查询命令
		'''
		log_file = date.today().strftime('/data/logs/fltranslog/%Y-%m-%d.log')
		if not os.access(log_file, os.F_OK):
			log_file = '~/app/python/web/web.py/2016-07-27.log'

		match = ''
		if dev_id or app_id:
			'$3=="%s"' % app_id
			if dev_id and app_id: match = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($3=="%s" && $20=="%s") print $0}\'' % (app_id, dev_id)
			elif app_id: match = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($3=="%s") print $0}\'' % app_id # print all match columns
			elif dev_id: match = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($20=="%s") print $0}\'' % dev_id
			if not lines: lines = '5000'
		else:
			lines = '100'
		#-v Col="all"
		vars='-v Col="%s"' % columns
		
		return 'tail -n%s %s %s|awk %s -f trimcells.awk' % (lines, log_file, match, vars)

	@staticmethod
	def excute(dev_id, app_id, columns, lines='100', show_lines='100', reversed=False):
		start_point = time.time()
		cmd = CommandUtil.gen_command(dev_id, app_id, columns, lines)
		print cmd
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out, err = process.communicate()

		titles = [u'EventID', u'Log Time', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS','IP Addr', u'MacAddr', u'DevID', u'AccountID', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName', u'EventValue',]
		if columns=='all': titles = [u'EventID', u'Log Time', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS','IP Addr', u'MacAddr', u'BrandName', u'Serial', u'DevID', u'IDFA', u'IDFA', 'Screen', u'Lang', u'GPS', u'Net', 'Machine', u'AccountID', u'AccountName', u'AccountType', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName', u'EventValue', u'DataSrouce', u'Reserved',]
		raws = [line.split('\\x02') for line in codecs.decode(out.strip('\n'), 'utf-8').split('\n')]
		if columns=='c10': titles = [u'EventID' ,u'logtime', u'AppID', u'UID', u'ChannelID', u'DevID', u'AccountID', u'RoleID', u'RoleName', u'EventValue']
		raws = [line.split('\\x02') for line in codecs.decode(out.strip('\n'), 'utf-8').split('\n')]

		if reversed:
			raws.reverse()
			print 'reversed@excute'

		if len(raws) > int(show_lines): raws = raws[0:int(show_lines)]

		return Result(cmd, out, err, titles, raws, time.time()-start_point)

if __name__ == '__main__':
	print CommandUtil.excute()