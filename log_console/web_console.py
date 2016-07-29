# -*- coding: utf8 -*-

import os
import web
from jinja2 import Environment, FileSystemLoader

from command_helper import CommandUtil, Result


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

myform = web.form.Form( 
	# web.form.Textbox("IMEI"),
	web.form.Textbox("DevID"),
	web.form.Textbox("Lines", 
    web.form.notnull,
    web.form.regexp('\d+', 'Must be a digit'),
    web.form.Validator('Not more than 100000', lambda x:int(x)<100001)),
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

		result = CommandUtil.excute(devID=form.d.DevID, lines=form.d.Lines)

		return render_template('list.html',form=form, result=result)
		
		# return render_template('list.html', headers=result.titles, records=raws, cmd=cmd, form=form)

if __name__ == "__main__":
	app.run()