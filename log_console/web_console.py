# -*- coding: utf8 -*-

import os
import web
from jinja2 import Environment, FileSystemLoader

import subprocess, codecs

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

	#jinja_env.update_template_context(context)
	return jinja_env.get_template(template_name).render(context)

def excute(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout, stderr = process.communicate()

	if(stderr):
		print "==Error Info ==", stderr
		return

	return stdout

aa = '2016-07-26 14:23:18\x0200\x02100287\x0282934955191469514198944\x022.0.4.150119\x022016-07-26 14:23:15\x02\x02300122\x021.2.7\x02Android\x024.4.2\x02cn\x021\x027c:7d:3d:bb:29:fc\x02867376027290754\x02460026768632234\x02HUAWEI MT7-TL00\x02Huawei\x02898600F7201491447834\x02867376027290754\x02\x02\x021812,1080\x02zh-hans\x02\x025\x02GSM\x02\x02\x02\x02\x020\x02\x02\x020\x021\x02DataSource1\x02DataSource2\x02DataSource3\x02DataSource4\x02reserve1\x02reserve2\x02reserve3\x02reserve4\x02reserve5\x02fl_init\x02{}'

myform = web.form.Form( 
	web.form.Textbox("idfa"), 
	web.form.Checkbox(u'short columns'), 
	web.form.Dropdown('os', ['all', 'ios', 'android']))

class Console:
	def GET(self):
		form = myform()
		return render_template('index.html', form=form)

	def POST(self):
		# You can use a relative path as template name, for example, 'ldap/hello.html'.
		# raws = []
		# raws.append(aa.split('\x02'))
		cmd = 'tail -n+9999 2016-07-27.log |awk -f trimcells.awk'
		out = excute(cmd)
		out = codecs.decode(out, 'utf-8')
		raws = [line.split(',') for line in out.split('\n')]
		for raw in raws: print raw
		titles = [u'logtime', u'AppID', u'UID', u'SDK Ver', u'ChannelID', u'Game Ver', u'IMEI', u'IDFA', u'AccountID', u'ServerID', u'RoleLevel', u'RoleID', u'RoleName',]
		return render_template('list.html', headers=titles, records=raws)

if __name__ == "__main__":
	app.run()