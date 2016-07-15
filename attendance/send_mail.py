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
			print self.client.ehlo()
			print self.client.login(user, password)
			# 设置邮件服务的发送者为发送账号
			self.sender = user
		except SMTPConnectError as e:
			logging.error('SMTPConnectError({0}): on {1}:{2}'.format(e.message, host, port))
		except SMTPAuthenticationError as e:
			logging.error('SMTPAuthenticationError({0}): on {1}:{2}'.format(e.message, user, password))
			print e
			raw_input("Mail Account Authentication Failed! Press Enter to Quit:(")
			exit(-1)

		self.client.set_debuglevel(1) # debug=True

	def close(self):
		"""释放连接
		"""
		self.client.close()
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

		if len(content) > 0:
			part = MIMEText(content, 'html', 'utf8')
			# print 'content:', content
			msg.attach(part)

		if files != None:
			for f in files:
				part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
				part.set_payload(open(f, 'rb').read())
				encoders.encode_base64(part)

				# 如果附件名称含有中文, 则 filename 要转换为gb2312编码, 否则就会出现乱码
				# unicode转换方法:  basename.encode('gb2312')  
				# utf-8转换方法:    basename.decode('utf-8').encode('gb2312')  
				filename = os.path.basename(f)
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename.encode('gb2312'))
				msg.attach(part)

		logging.info('gen msg for '+ reply_to)
		return msg

	def _message_id(self, reply):
		message_id = None

		if str(reply[0]) == '250': 
			message_id = str(reply[1]).split('#')[1]

		return message_id


	def send(self, msg):

		self.client.mail(self.sender)
		self.client.rcpt(msg['to'])
		
		# print msg.as_string()
		try:
			(code, resp) = self.client.data(msg.as_string())
			self.client.rset()

			logging.info('send %s' % resp)

			if code == 250:
				logging.info('send to %s' % msg['to'])
				return True
			logging.error('code=%d, msg=%s' % (code, resp))
			return False

		except:
			return False

		# err = self.client.sendmail(msg['from'], msg['to'], msg.as_string())
		# if err:
		# 	logging.error(err)
		# 	return False
		# logging.info('send to %s' % msg['to'])
		# return True

def init():
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read('mail.ini')
	base_dir = config.get('basic', 'base_dir')
	if sys.platform == 'win32': #decode to unicode
		base_dir = base_dir.decode('utf-8')
	log_file = os.path.join(base_dir, 'mail.log')
	logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
	logging.info('init send mail tool...')

	host = config.get('mail_account', 'host')
	port = config.get('mail_account', 'port')
	user = config.get('mail_account', 'user')
	password = config.get('mail_account', 'password')

	return MailTool(host, port, user, password), base_dir

def send_mail():
	"""考勤通知邮件发送
	"""
	tool, base_dir = init()

	if None == tool:
		logging.warn('init failed!')
		raw_input("Fatal Mistake! Press Enter to Quit:(")
		exit(-1)
	
	# 读取待发送内容：
	outbox_path = os.path.join(base_dir,'outbox')
	sent_path = os.path.join(base_dir,'sent_box')
	logging.info('reading from %s' % outbox_path)
	if not os.access(sent_path,os.F_OK): 
		os.mkdir(sent_path)
		logging.info('create sent_box dir[%s]' % sent_path)
	for mail_file in os.listdir(outbox_path):
		# 张一荻_网秦_zhangyidi@feiliu.com_.html
		try:
			(name, d , email, ft) = mail_file.split('_')
			content = codecs.open(os.path.join(outbox_path, mail_file)).read()
			ffrom = formataddr((str(Header(u'考勤系统通知', 'utf-8')), tool.sender))
			if email.find('@')<0 :
				logging.info('Wrong email address:[%s] in %s' % (email, mail_file))
				continue
			rcpt_tos = [email, ]
			reply_to = tool.sender
			# print type(u'[考勤异常提醒]'), type(name)
			subject = u'[考勤异常提醒]'
			try:
				if sys.platform == 'win32': #decode to unicode
					subject = subject + name.decode('GBK')
				else:
					subject = subject + name.decode('utf-8')
			except: pass
			files = None
			msg = MailTool.msg(ffrom, rcpt_tos, reply_to, subject, content, files)
			if tool.send(msg):
				print 'move to sent box...'
				os.rename(os.path.join(outbox_path,mail_file), os.path.join(sent_path,mail_file))
				logging.info('sent to %s[%s]' % (name, email))

		except Exception as e:
			logging.error('Exception({0}): on sending {1}'.format(e.message, mail_file))

	tool.close()

def test_send():
	"""邮件发送测试
	"""
	tool, base_dir = init()

	if None == tool:
		logging.warn('init failed!')
		exit(-1)
	
	# formataddr(realname, email_address)
	ffrom = formataddr((str(Header(u'考勤系统通知', 'utf-8')), "liyan@feiliu.com"))
	rcpt_tos = ['liyan@feiliu.com', 'liumingfei@feiliu.com']
	reply_to = 'liyan@feiliu.com'
	subject = u'考勤异常提醒'
	content = codecs.open(u'/opt/e_disk/doc/NetQin/2015-Feiliu/当前工作/AttendanceRegister/work/outbox/乐号_网秦_lehao@feiliu.com_.html', encoding='utf-8').read()
	files = [u'/opt/e_disk/doc/NetQin/2015-Feiliu/当前工作/AttendanceRegister/work/outbox/乐号_网秦_lehao@feiliu.com_.html', ]
	files = None
	msg = MailTool.msg(ffrom, rcpt_tos, reply_to, subject, content, files)
	if tool.send(msg):
		print 'move to sent box...'
	tool.close()


def main():
	# test_send()

	send_mail()

if __name__ == '__main__':
	main()
	raw_input("Press Enter to Exit:)")



