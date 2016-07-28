# -*- coding: utf8 -*-

import os
import web
from jinja2 import Environment, FileSystemLoader

import subprocess, codecs
from datetime import date

urls = ("/.*", "Console")
app = web.application(urls, globals())

def render_template(template_name, **context):
	'''
	用来引入jinja2的方法
	'''
	extensions = context.pop('extensions', [])
	globals = context.pop('globals', {})

	jinja_env = Environment(
			loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
			extensions=extensions,
			)
	jinja_env.globals.update(globals)

	return jinja_env.get_template(template_name).render(context)

def gen_command(devID, lines):
	'''生成要执行的查询命令
	'''
	log_file = date.today().strftime('/data/logs/fltranslog/%Y-%m-%d.log')
	if not os.access(log_file, os.F_OK):
		log_file = '~/app/python/web/web.py/2016-07-27.log'
	

	match = ''
	if devID:
		match = '|awk \'BEGIN{FS="\\\\\\\\x02"} {if($20=="%s") print $0}\'' % devID # print all match columns
		if not lines: lines = '100'
	else:
		lines = '100'
	
	return 'tail -n%s %s %s|awk -f trimcells.awk' % (lines, log_file, match)

def excute(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	return process.communicate()

myform = web.form.Form( 
	# web.form.Textbox("IMEI"),
	web.form.Textbox("DevID"),
	web.form.Textbox("Lines", 
    web.form.notnull,
    web.form.regexp('\d+', 'Must be a digit'),
    web.form.Validator('Not more than 50000', lambda x:int(x)<50000)),
	web.form.Checkbox(u'short columns'), 
	web.form.Dropdown('OS', ['all', 'iOS', 'Android']))

class Console:
	def GET(self):
		form = myform()
		return render_template('index.html', form=form)

	def POST(self):
		form = myform()
		if form.validates():
			print "IDFA = %s, OS = %s" % (form.d.DevID, form.d.OS)
			# return "IDFA = %s, OS = %s" % (form.d.DevID, form.d.OS)
		cmd = gen_command(devID=form.d.DevID, lines=form.d.Lines)
		out, err = excute(cmd)
		if(err):
			return render_template('list.html', err=err, cmd=cmd)

		out = codecs.decode(out, 'utf-8')
		raws = [line.split(',') for line in out.split('\n')]
		titles = [u'EventID', u'logtime', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'OS', u'DevID', u'AccountID', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName',]
		return render_template('list.html', headers=titles, records=raws, cmd=cmd, form=form)

if __name__ == "__main__":
	app.run()