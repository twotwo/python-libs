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
	web.form.Textbox("DevID", description=u'设备ID(IMEI/IDFA)'),
	web.form.Textbox("AppID", description=u'游戏唯一标识(AppID)'),
	web.form.Textbox("Lines", 
		web.form.notnull,
		web.form.regexp('\d+', 'Must be a digit'),
		web.form.Validator('Not more than 100000', lambda x:int(x)<100001),
		description=u'指定搜索的行数', 
		value="20000", 
	),
	web.form.Textbox("ShowLines", 
		web.form.notnull,
		web.form.regexp('\d+', 'Must be a digit'),
		web.form.Validator('Not more than 200', lambda x:int(x)<201),
		description=u'显示的条数', 
		value="100", 
	),
	web.form.Dropdown('Columns', ['all', 'c17', 'c10'], description=u'显示字段', value="c17", ),
	web.form.Dropdown('EventId', ['all', 'fl_init', 'fl_login', 'fl_logout', 'fl_payRequest', 'fl_paySucc'], description=u'筛选指定的EventId', value="All", multiple=True),
	# web.form.Checkbox('ShortColumns', description=u'精简字段', value='True'), 
	web.form.Checkbox('Reversed', description=u'是否倒序', value=True, checked=True), 
	# web.form.Dropdown('OS', ['all', 'iOS', 'Android']),
	)

class Console:
	def GET(self):
		form = myform()
		return render_template('index.html', form=form)

	def POST(self):
		form = myform()
		if form.validates():
			result = CommandUtil.excute(dev_id=form.d.DevID, app_id=form.d.AppID, columns=form.d.Columns, lines=form.d.Lines, show_lines=form.d.ShowLines, reversed=form.d.Reversed)
			return render_template('list.html',form=form, result=result)
		return render_template('index.html', form=form)
		# return render_template('list.html', headers=result.titles, records=raws, cmd=cmd, form=form)

if __name__ == "__main__":
	app.run()