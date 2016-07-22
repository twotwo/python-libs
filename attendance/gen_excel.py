# -*- coding: utf8 -*-
import ConfigParser, logging

import xlrd, xlwt

import datetime, sys, os

from jinja2 import Template
import codecs

import send_mail

import random #only for test
"""
Load Attendance Register, create Absent Records

Powered by Liyan @ 2016-05-24
"""

#debug, show records details
debug_name = u''

class DtoRecord(object):
	"""数据传输对象: 一条具体的考勤记录
	"""
	def __init__(self, date, week_num, time_in, time_out, time_work, status, desc):
		self.date = date
		self.week_num = week_num #周几
		self.time_in = time_in #上班打卡时间
		self.time_out = time_out #下班打卡时间
		self.time_work = time_work #当天工时
		self.status = status #考勤状态
		self.desc = desc

	def __str__(self):
		return 'DtoRecord: ' + self.date + ' '+ self.status + ' '+ self.time_work

class PersonRecord(object):
	"""数据存储对象：一个人所有的打卡记录
	"""
	def __init__(self, datarange):
		# 加载考勤周期
		self.datarange = datarange
		self.util = DateUtil()

	def put_3_values(self, department, name, timestamp):
		"""第一次初始化dailyrecords，部门、姓名和时间戳
		"""
		self.count = 0
		self.department = department
		self.name = name
		self.dailyrecords = {} #日签到记录字典对象：{date as Key: List<timestamp in this day>}
		self.put_timestamp(timestamp)

	def put_timestamp(self, timestamp):
		"""同一个人，不需要再添加部门和姓名信息了
		"""
		self.count = self.count + 1
		d, t = DateUtil.parse_date_and_time(timestamp)
		#debug somebody
		if self.name == debug_name:
			print timestamp, (d, t)
		if d in self.dailyrecords:
			self.dailyrecords[d].append(t)
		else:
			self.dailyrecords[d] = [t]

class DateUtil(object):
	D_week = {0:u'周一',1:u'周二', 2:u'周三',3:u'周四', 4:u'周五',5:u'周六', 6:u'周日'}
	# D_week = {0:u'Mon.',1:u'Tue.', 2:u'Wed.',3:u'Thu.', 4:u'Fri.',5:u'Sat.', 6:u'Sun.'}

	# 员工考勤状态：休息日工作(加班)、正常、迟到、早退(18:00前下班或工时不足9小时)、漏打卡、缺勤
	Attendance_Status = {'over_time':u'休息日工作','normal':u'正常','be_late':u'迟到', 'leave_early':u'早退', 'missing':u'漏打卡', 'absence':u'缺勤', }

	"""计算工作日、工作状态和工时的工具类
	"""
	@staticmethod
	def create_daterange(start, end, working_days=[], holidays=[]):
		"""生成工作日历
		比如，start='2016-05-24', end='2016-06-27'，则生成含起始日期的工作区间表
		还可以制定调休情况：working_days，需要工作的周末；holidays，放假的工作日
		注：这个表在代码中作为字典表使用，不要往表内做任何更新！

Sample return
('2016-04-30', datetime.date(2016, 4, 30), u'Sat.', True)
('2016-05-01', datetime.date(2016, 5, 1), u'Sun.', False)
('2016-05-02', datetime.date(2016, 5, 2), u'Mon.', False)
('2016-05-03', datetime.date(2016, 5, 3), u'Tue.', False)
		"""
		# working_days = self.config.get('check info','working_days').split(',')
		# holidays = self.config.get('check info','holidays').split(',')
		oneday = datetime.timedelta(days=1)
		day_start = datetime.datetime.strptime(start,"%Y-%m-%d").date()
		day_end = datetime.datetime.strptime(end,"%Y-%m-%d").date()
		datarange = [] # (str, datatime, week number, is_working_day)
		if day_end < day_start:
			print 'wrong date range!'
			return
		
		# format working_days & holidays
		tmp_days = []
		for day in working_days:
			day = datetime.datetime.strptime(day.strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
			tmp_days.append(day)
		working_days = tmp_days
		tmp_days = []
		for day in holidays:
			day = datetime.datetime.strptime(day.strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
			tmp_days.append(day)
		holidays = tmp_days
		print "working_days = ", working_days, " holidays = ", holidays

		day_next = day_start
		while day_end >= day_next:
			is_working_day = True
			if day_next.strftime('%Y-%m-%d') in working_days:
				is_working_day = True
			elif day_next.strftime('%Y-%m-%d') in holidays:
				is_working_day = False
			else:
				is_working_day = (day_next.weekday() < 5)
			datarange.append( (day_next.strftime('%Y-%m-%d'), day_next, DateUtil.D_week[day_next.weekday()], is_working_day) ) 
			day_next = day_next + oneday

		return datarange

	@staticmethod
	def parse_date_and_time(timestamp): # 2008/1/25 12:22:00
		"""把打卡记录字串转换成日期和时间
		注：从excel中读取原始打卡记录时使用
		"""
		obj = datetime.datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
		return obj.strftime('%Y-%m-%d'), obj.strftime('%H:%M:%S')
	
	@staticmethod
	def calc_workinghours(start, end):
		"""计算当日工时和工作状态
		比如，19:00:00 - 9:45:00，得出一天的工作时长
		"""
		status = 'normal'
		is_late=False
		is_early=False
		time_in = datetime.datetime.strptime(start, '%H:%M:%S')
		time_out = datetime.datetime.strptime(end, '%H:%M:%S')
		# update: 10:00:59前不算迟到
		if time_in > datetime.datetime.strptime('10:00:59', '%H:%M:%S'): is_late = True
		if time_out < datetime.datetime.strptime('18:00:00', '%H:%M:%S'): is_early = True
		if (time_out - time_in)< datetime.timedelta(hours=9): is_early = True
		
		#双重状态也记录成早退
		if is_late: status = 'be_late'
		if is_early: status = 'leave_early'

		return str(time_out - time_in), status

	@staticmethod
	def gen_person_records(datarange, dailyrecords, debug=False):
		"""根据考勤周期和个人打卡记录，生成员工考勤表
		考勤日类型：工作日、休息日
		"""
		records = [] # date, check in & out, check in, check out, working hours, status, desc
		for d in datarange: # (str, datatime, week number, is_working_day)
			date = d[0]
			c_in = ''
			c_out = ''
			workinghours = ''
			status = 'normal'
			today_record = dailyrecords.get(date)

			if today_record==None or len(today_record) == 0:# 无记录
				if d[3]: # is_working_day
					status = 'absence' # 缺勤
			elif len(today_record) > 1: # 考勤周期内有2条以上打卡记录
				c_in = dailyrecords.get(date)[0]
				c_out = dailyrecords.get(date)[-1]
				workinghours, status = DateUtil.calc_workinghours(c_in, c_out)
				if not d[3]: status = 'over_time' #休息日工作
			else: # 漏打卡 len(today_record) == 1
				c_in = dailyrecords.get(date)[0]
				#update 工作日，一条记录才是漏打卡
				if d[3]: status = 'missing' # 漏打卡

			record = DtoRecord(date, d[2], c_in, c_out, workinghours, status, DateUtil.Attendance_Status.get(status))
			records.append(record)

		if debug:
			print 'DateUtil.gen_person_records: ', len(records)
			for r in records: print r

		return records

class AttendanceProcessor(object):
	"""考勤记录处理逻辑
		1、从配置文件读取考勤开始日和截止日，生成并加载考勤周期
		2、初始化考勤汇总表：生成写excel对象，写表头
		3、生成读excel对象，读取每条考勤记录
		3.1 合成日签到记录
		3.2 对比考勤周期，生成完整周期的考勤
		3.3 写入汇总表

	存储结构
		- self.datarange: 考勤周期(从开始日到截止日) - [(str, datatime, isweekend, isholiday), ...]
		- 以姓名为key的日签到记录： 详见PersonRecord -- 如果有重名会出bug
			日签到记录字典对象：{date as Key: List<timestamp in this day>}
	
	"""
	def __init__(self, ini_file):
		self.config = ConfigParser.RawConfigParser(allow_no_value=True)
		self.config.read(ini_file)
		# 服务基础路径：
		self.base_dir = self.config.get('basic','base_dir')
		if sys.platform == 'win32': #decode to unicode
			self.base_dir = self.base_dir.decode('utf-8')
		if not os.access(self.base_dir,os.F_OK): 
			os.makedirs(self.base_dir)
			logging.info('create base_dir: %s'%self.base_dir)
		print 'base_dir = ', self.base_dir, type(self.base_dir)
		# 初始化日志服务
		log_file = os.path.join(self.base_dir, 'excel.log')
		logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
		logging.info('init gen excel tool...')
		# 加载考勤周期
		self.datarange = self.__daterange()
		# 加载邮件地址: {姓名_部门:address, }
		self.mails = self.__load_email_address()
		# 加载通知邮件的内容模板
		self.template = Template(codecs.open('template.html', encoding='utf-8').read())
		# print self.datarange
		self.row_write = 0 #当前写入excel的行数
		self.__summary_sheet_init()
		self.style_red = xlwt.easyxf(
			"font: name Arial;"
			"pattern: pattern solid, fore_colour red;"
			)

	def __daterange(self):
		start = self.config.get('check info','start')
		end = self.config.get('check info','end')
		logging.info('daterange: from %s to %s' % (start, end))
		print('daterange: from %s to %s' % (start, end))
		working_days = self.config.get('check info','working_days').split(',')
		holidays = self.config.get('check info','holidays').split(',')
		return DateUtil.create_daterange(start, end, working_days, holidays)

	def __load_email_address(self):
		"""读取mail.xlsx中姓名、部门、邮箱信息
		select department, name, email from fl_users;
		"""
		workbook = xlrd.open_workbook('mail.xlsx', encoding_override='gb2312')
		print '__load_email_address - loading sheets: ' + ', '.join(workbook.sheet_names())
		sheet = workbook.sheet_by_index(0)
		num_rows = sheet.nrows
		num_cells = sheet.ncols
		print 'rows =%d, cells =%d' % (num_rows, num_cells)
		mails = {}

		for num_row in range(1,num_rows):
			(department, name, mail) = (sheet.cell_value(num_row, 0), sheet.cell_value(num_row, 1), sheet.cell_value(num_row, 2))
			mails[name+'_'+department] = mail
			mails[name] = mail
			# print (department, name, mail)
		return mails

	def __summary_sheet_init(self):
			style = xlwt.easyxf(
				"font: bold on; align: wrap on, vert centre, horiz center;"
				)
			self.book = xlwt.Workbook(encoding="utf-8")
			self.sheet = self.book.add_sheet('Sheet 1')

			self.sheet.write(self.row_write, 0, u'姓名', style) # row, column, value
			self.sheet.write(self.row_write, 1, u'部门', style)
			self.sheet.write(self.row_write, 2, u'日期', style)
			self.sheet.write(self.row_write, 3, u'上下班', style)
			self.sheet.write(self.row_write, 4, u'上班', style)
			self.sheet.write(self.row_write, 5, u'下班', style)
			self.sheet.write(self.row_write, 6, u'工时', style)
			self.sheet.write(self.row_write, 7, u'描述', style)

			# for num_row in range(1,10):
			# 	self.sheet.write(num_row, 0, u'姓名'+str(num_row),style) # row, column, value

	def __summary_sheet_writebyperson(self, name, department, records, debug=False):
			m_records = [] #考勤异常记录

			try:

				for record in records: # date, check in & out, check in, check out, working hours, desc
					self.row_write = self.row_write + 1
					# print '============write at ',self.row_write, record
					self.sheet.write(self.row_write, 0, name) 
					self.sheet.write(self.row_write, 1, department)
					self.sheet.write(self.row_write, 2, record.date+record.week_num)
					self.sheet.write(self.row_write, 3, (record.time_in + ' ' + record.time_out).strip())
					self.sheet.write(self.row_write, 4, record.time_in)
					self.sheet.write(self.row_write, 5, record.time_out)
					self.sheet.write(self.row_write, 6, record.time_work)
					self.sheet.write(self.row_write, 7, record.desc)
					# self.sheet.write(self.row_write, 8, record.status)

					if record.status !='normal':
						#update 增加关心提醒
						if record.status =='over_time': record.desc = u'休息日工作，要注意身体噢'
						m_records.append(record)
					if debug: print name, self.row_write+1, record

			except:
				print "Unexpected error:", sys.exc_info()[0]
				raise
			self.sheet.flush_row_data()

			if debug:
				print '__summary_sheet_writebyperson(all & abnormal): ', len(records), len(m_records)
				for r in records: print r

			if len(m_records) > 0:
				mail = None
				try:
					mail = self.mails.get(name+'_'+department) # 根据姓名和部门获得邮箱地址
					if mail == None: mail = self.mails.get(name) # 当前需求，只根据姓名获得邮箱地址
				except UnicodeEncodeError as e:
					logging.error('UnicodeEncodeError({0}): on writebyperson name={1}, department={2}'.format(e.message, name, self.department))
				if mail == None or len(mail) == 0: mail = 'unknow'
				self.__write_person_mail(name, department, mail, m_records)
				m_records = []


	def __write_person_mail(self, name, department, mail, records):
		file_path = os.path.join(self.base_dir, self.config.get('check info','outbox'))

		try:
			if not os.access(file_path,os.F_OK): 
				os.mkdir(file_path)
				logging.info('create outbox dir[%s]' % file_path)
			file_path = file_path.decode('utf-8')
		except: pass

		# 写个人html文件
		file_path = os.path.join(file_path, name +'_'+ department +'_'+ mail +'_.html')
		body = self.template.render(name=name, department=department, records=records)
		try:
			codecs.open(file_path, 'w', encoding='utf-8').write(body)
		except: 
			logging.error('failed to write mail for %s_%s: %s' % (name, department, mail))


	def generate_excels(self):
			file_path = self.config.get('check info','raw_excel')

			#add at 2016-07-21 如果存在${base_dir}/sent_box或${base_dir}/mail.log，不再重新生成相关记录
			if os.access(self.base_dir+'/sent_box',os.F_OK) or os.access(self.base_dir+'/mail.log',os.F_OK): 
				logging.warn(u'[Regenerate Error] 错误的执行逻辑，开始执行邮件发送后就不要再执行生成命令！')
				print '[Regenerate Error] Can not generate excels after sending!'
				return

			# file_path = '/tmp/11.xls'
			workbook = xlrd.open_workbook(file_path, encoding_override='gb2312')
			print 'loading sheets: ' + ', '.join(workbook.sheet_names())
			sheet = workbook.sheet_by_index(0)
			num_rows = sheet.nrows
			num_cells = sheet.ncols
			print 'rows =%d, cells =%d' % (num_rows, num_cells)
			
			##################################################
			# load (department, name, timestamp) line by line
			##################################################
			# 1 line: title
			# 2 line: real first line, only put
			record = PersonRecord(self.datarange)
			num_row = 1
			record.put_3_values(sheet.cell_value(num_row, 0), sheet.cell_value(num_row, 1), sheet.cell_value(num_row, 2))

			# 3 line to last-1 line: check different, write or put
			for num_row in range(1+1,num_rows-1):

				try:
					(department, name, timestamp) = (sheet.cell_value(num_row, 0), sheet.cell_value(num_row, 1), sheet.cell_value(num_row, 2))
					# print name, timestamp
					if record.name == name:
						if record.department != department:
							print "same name but different department!", name, department
						record.put_timestamp(timestamp)
					else:
						# 新名字出现了，把当面员工的考勤写入汇总表
						# records = record.get_person_records()
						# debug 查看产出内容
						debug = False
						if record.name == debug_name:
							print '\n'.join(["%s=%s" % (k, v) for k, v in record.dailyrecords.items()])
							print record.name, 'all record size = ', record.count
							debug = True
						if debug_name != None:
							print record.name, ' write from row: ', self.row_write+2
						records = DateUtil.gen_person_records(self.datarange, record.dailyrecords, debug)
						# 写文件
						self.__summary_sheet_writebyperson(record.name, record.department, records, debug)
						record.dailyrecords = {}

						# 开始下一个人
						record.put_3_values(department, name, timestamp)
				except IndexError as e:
					print 'IndexError({0}): on read row {1}/write row {2}'.format(e.message, num_row, self.row_write)
					# print "I/O error({0}): {1}".format(e.errno, e.strerror)
				except NameError as e:
					print 'NameError({0}): on read row {1}/write row {2}'.format(e.message, num_row, self.row_write)
				except Exception as e:
					# print "Unexpected error:", sys.exc_info()[0]
					print 'Exception({0}): on read row {1}/write row {2}'.format(e.message, num_row, self.row_write)
					# raise e

			try:
				# last line: write last person
				(department, name, timestamp) = (sheet.cell_value(num_rows-1, 0), sheet.cell_value(num_rows-1, 1), sheet.cell_value(num_rows-1, 2))
				if record.name == name: record.put_timestamp(timestamp)
				records = DateUtil.gen_person_records(self.datarange, record.dailyrecords)
				self.__summary_sheet_writebyperson(record.name, record.department, records, True)
				record.dailyrecords = {}
			except Exception as e:
				# print "Unexpected error:", sys.exc_info()[0]
				print 'Exception({0}): on write row {1}'.format(e.message, self.row_write)

			# 生成考勤汇总表	
			file_path = os.path.join(self.base_dir, self.config.get('check info','summary_sheet'))
			self.book.save(file_path)
			print 'Write to ', file_path
			logging.info('Write to %s' % file_path)


def test_xls_read():
	file_path = '/tmp/raw.xlsx'
	# file_path = '/tmp/11.xls'
	workbook = xlrd.open_workbook(file_path, encoding_override='gb2312')
	print 'loading sheets: ' + ', '.join(workbook.sheet_names())
	sheet = workbook.sheet_by_index(0)
	num_rows = sheet.nrows
	num_cells = sheet.ncols
	print 'rows =%d, cells =%d' % (num_rows, num_cells)
	for num_row in range(0,num_rows):
		values = sheet.row_values(num_row) #sheet.cell_value(num_row, 1)
		print ', '.join(values)

def test_xls_write(file_path):
	book = xlwt.Workbook(encoding="utf-8")
	sheet = book.add_sheet('Sheet 1')
	num = 0
	# 编辑单元格
	sheet.write(num, 0, u'姓名') # row, column, value
	sheet.write(num, 1, u'部门')
	sheet.write(num, 2, u'日期')
	sheet.write(num, 3, u'上下班')
	sheet.write(num, 4, u'上班')
	sheet.write(num, 5, u'下班')
	sheet.write(num, 6, u'工时')
	sheet.write(num, 7, u'描述')

	style = xlwt.easyxf(
	"font: name Arial;"
	"pattern: pattern solid, fore_colour red;"
	)


	for num in range(1,10):
		sheet.write(num, 0, u'姓名'+str(num),style) # row, column, value

	book.save(file_path)

def test_gen_html(file_path):
	# file_path = os.path.join('.', 'template.html')
	template = Template(codecs.open('template.html', encoding='utf-8').read())

	# DtoRecord(date, week_num, time_in, time_out, time_work, status, desc)
	records = []
	records.append(DtoRecord(u'2016-6-17',u'周五','9:50','18.40','8:50','',u'迟到'))
	body = template.render(name=u'张三', department=u'平台业务部', records=records)
	# print body
	codecs.open(file_path, 'w', encoding='utf-8').write(body)

def xls_write_mail_address(departments, persons, file_path):
	book = xlwt.Workbook(encoding="utf-8")
	sheet = book.add_sheet('Sheet 1')
	num = 0
	# 编辑单元格
	sheet.write(num, 0, u'部门') # row, column, value
	sheet.write(num, 1, u'姓名')
	sheet.write(num, 2, u'邮件地址')

	for person in persons:
		num = num +1
		sheet.write(num, 0, departments[num/150%4]) # row, column, value
		sheet.write(num, 1, person)
		sheet.write(num, 2, str(num)+'@mail.com')
	
	book.save(file_path)

def xls_write_raw_data(drange, departments, persons, file_path):
	'''
	生成模拟考勤文件
'''
	book = xlwt.Workbook(encoding="utf-8")
	sheet = book.add_sheet('Sheet 1')
	num = 0
	# 编辑单元格
	sheet.write(num, 0, u'部门') # row, column, value
	sheet.write(num, 1, u'姓名')
	sheet.write(num, 2, u'日期时间')

	# 部门和姓名集合
	d_and_ps = []
	for person in persons:
		num = num +1
		d_and_ps.append( (person, departments[num/150%4]) )

	num = 0
	for (p, d) in d_and_ps:
		for dd in drange: # ('2016-04-30', datetime.date(2016, 4, 30), u'Sat.', True)
			num = num +1
			sheet.write(num, 0, d) # row, column, value
			sheet.write(num, 1, p)
			#随机上班打卡时间： 8:00 ~ 10:59
			sheet.write(num, 2, dd[1].strftime('%Y/%m/%d') + datetime.time(random.randint(8, 10), random.randint(0, 59), 0).strftime(' %H:%M:%S') )

			if random.randint(1, 10) > 3: #随机漏打卡，30%
				num = num +1
				sheet.write(num, 0, d) # row, column, value
				sheet.write(num, 1, p)
				#随机下班打卡时间： 18:00 ~ 19:59
				sheet.write(num, 2, dd[1].strftime('%Y/%m/%d') + datetime.time(random.randint(18, 19), random.randint(0, 59), 0).strftime(' %H:%M:%S') )

		# if num > 100000: break

	book.save(file_path)

def generate_test_data():
	departments = [u'青龙组', u'白虎组', u'朱雀组', u'玄武组',]
	# 姓名生成
	persons = []
	name_first = u'赵 钱 孙 李 周 吴 郑 冯 陈 楮 卫 蒋 沈 韩 朱 秦 尤 许 何 吕 施 孔 曹 严 华 金 魏 陶 戚 谢 邹 喻 柏 水 窦 云 苏 潘 葛 奚 范 彭 鲁 韦 昌 马 苗 凤 花 俞 任 袁 柳 酆 鲍 史 费 廉 岑 薛 雷 贺 倪 滕 殷 罗 毕 郝 邬 安 乐 于 时 傅 皮 卞 齐 伍 余 元 卜 顾 孟 平 和 穆 萧 尹 姚 邵 湛 祁 毛 禹 狄 米 贝 明 计 伏 成 戴 谈 宋 茅 熊 纪 舒 屈 项 祝 董 杜 阮 蓝 闽 席 季 麻 贾 路 娄 危 江 童 颜 梅 盛 林 刁 锺 徐 丘 高 夏 蔡 田 樊 胡 凌 虞 万 支 柯 昝 管 卢 经 房 裘 缪 干 解 应 丁 宣 贲 邓 郁 单 杭 包 诸 左 石 崔 吉 钮 程 嵇 邢 滑 裴 陆 荣 荀 羊 於 惠 甄 麹 家 芮 羿 储 靳 汲 邴 糜 井 段 富 巫 乌 焦 巴 牧 隗 山 谷 车 侯 宓 全 郗 班 仰 秋 仲 伊 宁 仇 栾 暴 甘 斜 厉 祖 武 符 刘 景 詹 束 叶 幸 司 韶 郜 黎 蓟 印 宿 白 怀 蒲 邰 从 索 咸 籍 赖 卓 蔺 屠 池 乔 阴 郁 胥 能 苍 闻 莘 党 翟 谭 贡 劳 姬 申 扶 堵 冉 宰 郦 郤 璩 桑 桂 濮 牛 寿 边 扈 燕 冀 郏 浦 尚 温 别 庄 晏 柴 瞿 阎 慕 连 茹 习 宦 艾 鱼 向 古 易 慎 戈 廖 庾 暨 居 衡 步 都 耿 满 匡 国 文 寇 广 禄 阙 欧 殳 沃 利 蔚 越 夔 师 巩 厍 聂 晁 勾 敖 冷 訾 辛 阚 那 简 饶 曾 毋 沙 乜 养 鞠 须 巢 关 蒯 相 查 后 荆 游 竺 权 逑 盖 益 桓 万俟 司马 上官 欧 夏侯 诸葛 闻人 东 赫连 皇甫 尉迟 公 澹台 公冶 宗政 濮 淳于 单于 太叔 申 公孙 仲孙 轩辕 令 锺离 宇文 长孙 慕 鲜于 闾丘 司徒 司 丌官 司寇 仉 督 子 颛孙 端木 巫马 公 漆雕 乐正 壤驷 公 拓拔 夹谷 宰父 谷 晋 楚 阎 法 汝 鄢 涂 段干 百里 东郭 南 呼延 归 海 羊舌 微 岳 帅 缑 亢 况 后 有 梁丘 左丘 东门 西 商 牟 佘 佴 伯 赏 南 墨 哈 谯 笪 年 爱 阳 第五 言 福'
	name_last = u'老大 老二 老三 老四 老五 老六'
	for name in name_first.split():
		for nick in name_last.split():
			persons.append( name + nick )

	if not os.access('mail.xlsx',os.R_OK): 
		# 生成测试邮件列表文件
		print 'generate test mail address.'
		xls_write_mail_address(departments, persons, 'mail.xlsx')

	if not os.access('raw.xls',os.R_OK): 
		# 生成测试用打卡文件
		print 'generate test raw data.'
		xls_write_raw_data(DateUtil.create_daterange('2016-6-27','2016-7-8'), departments, persons, 'raw.xls')


def gen_excel():
	"""生成考勤汇总表(summary.xls)和考勤异常同事的异常记录表(outbox/*.xls)
	"""
	
	ini_file = 'mail.ini'
	if not os.access(ini_file,os.R_OK): 
		ini_file = 'mail_ini.sample'
		print 'try to read mail_ini.sample...'
		generate_test_data()
	elif not os.access(ini_file,os.R_OK):
		print 'mail.ini or mail_ini.sample not existed.'
		return
	p = AttendanceProcessor(ini_file)
	p.generate_excels()

def main():
	# test_xls_write('/tmp/example.xls')
	# test_gen_html('/tmp/somebody.html')

	# # 测试工时计算
	# print DateUtil.calc_workinghours('9:45:00', '19:00:00')
	# print DateUtil.calc_workinghours('9:45:00', '18:00:00')
	# print DateUtil.calc_workinghours('7:45:00', '17:00:00')

	# start = '2016-4-21'
	# end = '2016-5-20'
	# # 节假日调休安排：需要上班的周末和放假的工作日，用逗号(,)分割
	# working_days = '2016-4-30'.split(',')
	# holidays = '2016-5-2, 2016-5-3'.split(',')
	# for line in DateUtil.create_daterange(start, end, working_days, holidays):
	# 	print line

	gen_excel()

if __name__ == '__main__':
	main()
	raw_input("Press Enter to Exit:)")