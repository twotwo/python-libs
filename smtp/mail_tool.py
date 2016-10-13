# -*- coding:utf-8 -*-                                                          
"""
https://hg.python.org/cpython/file/2.7/Lib/smtplib.py
http://sendcloud.sohu.com/doc/email/code/#python
"""
from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, formataddr
from email import encoders

import base64, time, os, json
from datetime import datetime, date

try:
	import simplejson
except ImportError:
	import json as simplejson

import ConfigParser, logging
import codecs, sys
"""
一个简单的邮件发送工具

Powered by Liyan @ 2016-07-17
"""

class MailTool(object):
	"""一个发邮件的工具类
	"""

	def __init__(self, host, port, user, password, ssl=False):
		"""初始化客户端连接
		"""

		# #timeout=socket._GLOBAL_DEFAULT_TIMEOUT
		# self.timeout = timeout

		self.client = SMTP(host=host, port=port) 

		if ssl:
			self.client.starttls()

		try:
			self.client = SMTP(host, port)
			logging.info('smtp login ...')
			print self.client.ehlo()
			respons = self.client.login(user, password)
			print respons
			logging.info(respons)
			# 设置邮件服务的发送者为发送账号
			self.sender = user
		except SMTPConnectError as e:
			logging.error('SMTPConnectError({0}): on {1}:{2}'.format(e.message, host, port))
		except SMTPAuthenticationError as e:
			logging.error('SMTPAuthenticationError({0}): on {1}:{2}'.format(e.message, user, password))
			print e
			exit(-1)

		self.client.set_debuglevel(0) # 1: debug=True

	def close(self):
		"""释放连接
		"""
		self.client.close()
		logging.info('smtp close ...')
		# self.client.quit()

	@staticmethod
	def msg(ffrom, rcpt_tos, reply_to, subject, content, files):
		"""生成待发送内容
		"""

		msg = MIMEMultipart('alternative')
		msg['subject'] = subject
		msg['from'] = ffrom
		msg['reply-to'] = reply_to
		msg['to'] = ','.join(rcpt_tos).strip()

		if len(content.strip()) > 0:
			part = MIMEText(content, 'html', 'utf8')
			# print 'content:', content
			msg.attach(part)

		if files != None:
			for f in files:
				part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
				part.set_payload(open(f.strip(), 'rb').read())
				encoders.encode_base64(part)

				# 如果附件名称含有中文, 则 filename 要转换为gb2312编码, 否则就会出现乱码
				# unicode转换方法:  basename.encode('gb2312')  
				# utf-8转换方法:    basename.decode('utf-8').encode('gb2312')  
				filename = os.path.basename(f)
				print filename
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename.encode('gb2312'))
				msg.attach(part)

		logging.info('mail({0}) from[{1}] to[{2}] created.'.format(msg['subject'], msg['from'] , msg['to']))
		return msg

	def _message_id(self, reply):
		message_id = None

		if str(reply[0]) == '250': 
			message_id = str(reply[1]).split('#')[1]

		return message_id


	def send(self, msg):

		try:
			self.client.sendmail(msg['from'], msg['to'].split(','), msg.as_string())
			logging.info('mail({0}) from[{1}] to[{2}] sent'.format(msg['subject'], msg['from'] , msg['to']))
			return True
		except Exception as e:
			logging.error('mail({0}) to {1} sent failed: msg = {2}'.format(msg['subject'], msg['to'], e.message))
		
		return False

		# self.client.mail(self.sender)
		# self.client.rcpt(msg['to'].split(','))
		
		# try:
		# 	(code, resp) = self.client.data(msg.as_string())
		# 	self.client.rset()

		# 	# logging.info('send %s' % resp)

		# 	if code == 250:
		# 		logging.info('mail({0}) from[{1}] to[{2}] sent.\n\t{3}.'.format(msg['subject'], msg['from'] , msg['to'], resp))
		# 		return True
		# 	logging.error('mail({0}) to {1} sent failed: code = {2}, msg = {3}'.format(msg['subject'], msg['to'], code, resp))

		# 	return False

		# except:
		# 	return False


def init_smtp():
	"""Load basic and smtp config from mail.ini
	"""
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read('mail.ini')
	base_dir = config.get('basic', 'base_dir')
	if sys.platform == 'win32': #decode to unicode
		base_dir = base_dir.decode('utf-8')
	if not os.access(base_dir,os.F_OK):
		os.makedirs(base_dir)
		print 'now base dir created.'
	log_file = os.path.join(base_dir, 'mail.log')
	logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
	logging.info('init mail tool...')

	host = config.get('smtp', 'host')
	port = config.get('smtp', 'port')
	user = config.get('smtp', 'user')
	password = config.get('smtp', 'password')

	return MailTool(host, port, user, password), base_dir


def load_msg(section, conf_file='mail.ini'):
	"""加载指定配置对应的信息，并生成待发送邮件
	"""	
	# formataddr(realname, email_address)
	# ffrom = formataddr((str(Header(u'mail tool', 'utf-8')), "liyan@company.com"))
	# rcpt_tos = ['liyan@company.com', 'liumingfei@company.com']
	# reply_to = 'liyan@company.com'
	# subject = u'mail tool test'
	# content = codecs.open(u'/opt/local/ide/git_storage/github/tools-python/smtp/mail_tool.py', encoding='utf-8').read()
	# files = [u'/opt/local/ide/git_storage/github/tools-python/smtp/mail_tool.py', ]
	# files = None
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read(conf_file)

	ffrom = formataddr((str(Header(u'业务支撑中心技术组', 'utf-8')), config.get(section, 'from')))
	ffrom = config.get(section, 'from')
	rcpt_tos = config.get(section, 'to').split(',')
	reply_to = config.get(section, 'cc')
	subject = config.get(section, 'subject')
	# ToDo: load content from text file
	content = config.get(section, 'content')
	files = config.get(section, 'files').split(',')

	return MailTool.msg(ffrom, rcpt_tos, reply_to, subject, content, files)


def main():
	# init smtp tool
	tool, base_dir = init_smtp()

	# send one mail
	msg = load_msg('GameSDK V5')

	try:

		tool.send(msg)

	except Exception as e:
		logging.error('Exception({0}): on sending {1}'.format(e.message, msg['subject']))

	# release smtp connection
	tool.close()

if __name__ == '__main__':
	main()



