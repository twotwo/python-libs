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
	def gen_command(dev_id, app_id, event_filter, columns, lines):
		'''生成要执行的查询命令
		'''
		# tail -n20000 /data/logs/fltranslog/2016-08-05.log |awk 'BEGIN{FS="\\\\x02"} {if($3==".." && $20=="..") print $0}'|awk -v Col="c17" -f trimcells.awk
		template_cmd = 'tail -n%(lines)s %(log_file)s %(grep_pattern)s%(awk_match_pattern)s|awk %(awk_value)s -f trimcells.awk'

		log_file = date.today().strftime('/data/logs/fltranslog/%Y-%m-%d.log')
		if not os.access(log_file, os.F_OK):
			log_file = '~/app/python/web/web.py/2016-07-27.log'
		
		grep_pattern = ''
		# 'fl_login', 'fl_logout', 'fl_payRequest', 'fl_paySucc'
		if event_filter == 'account': grep_pattern = '|grep fl_log '
		if event_filter == 'payment': grep_pattern = '|grep fl_pay '

		awk_match_pattern = ''
		if dev_id or app_id:
			'$3=="%s"' % app_id
			if dev_id and app_id: awk_match_pattern = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($3=="%s" && $20=="%s") print $0}\'' % (app_id, dev_id)
			elif app_id: awk_match_pattern = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($3=="%s") print $0}\'' % app_id # print all match columns
			elif dev_id: awk_match_pattern = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($20=="%s") print $0}\'' % dev_id
			if not lines: lines = '5000'
		else:
			lines = '100'
		#-v Col="all"
		awk_value='-v Col="%s"' % columns
		values_cmd = {'lines':lines,
			'log_file':log_file,
			'grep_pattern':grep_pattern,
			'awk_match_pattern':awk_match_pattern,
			'awk_value':awk_value,
			# '':,
		}
		
		return template_cmd % values_cmd

	@staticmethod
	def excute(dev_id, app_id, event_filter, columns, lines='100', show_lines='100', reversed=False):
		start_point = time.time()
		cmd = CommandUtil.gen_command(dev_id, app_id, event_filter, columns, lines)
		print cmd
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		out, err = process.communicate()

		# c17
		titles = [u'EventID',u'ReceiveTime', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS','IP Addr', u'MacAddr', u'DevID', u'AccountID', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName', u'EventValue',]
		if columns=='all': titles = [u'EventID', u'ReceiveTime', u'Log Time', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS','IP Addr', u'MacAddr', u'BrandName', u'Serial', u'DevID', u'IDFA', u'IDFV', 'Screen', u'Lang', u'GPS', u'Net', 'Machine', u'AccountID', u'AccountName', u'AccountType', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName', u'EventValue', u'DataSrouce', u'Reserved',]
		raws = [line.split('\\x02') for line in codecs.decode(out.strip('\n'), 'utf-8').split('\n')]
		if columns=='c10': titles = [u'EventID' ,u'ReceiveTime', u'AppID', u'UID', u'ChannelID', u'DevID', u'AccountID', u'RoleID', u'RoleName', u'EventValue']
		raws = [line.split('\\x02') for line in codecs.decode(out.strip('\n'), 'utf-8').split('\n')]

		if reversed:
			raws.reverse()
			print 'reversed@excute'

		if len(raws) > int(show_lines): raws = raws[0:int(show_lines)]

		return Result(cmd, out, err, titles, raws, time.time()-start_point)

if __name__ == '__main__':
	print CommandUtil.excute()