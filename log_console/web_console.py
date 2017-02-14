# -*- coding: utf8 -*-

import os
import web
from jinja2 import Environment, FileSystemLoader

from command_helper import CommandUtil, Result


urls = (
		"/", "Statistic",
		"/gas", "GameAd"	)
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
		web.form.Dropdown('Columns', ['all', 'c17', 'c10'], description=u'显示字段', value="c17", link="http://172.16.100.90/confluence/pages/viewpage.action?pageId=12517799"),
		# 'fl_login', 'fl_logout', 'fl_payRequest', 'fl_paySucc'
		web.form.Dropdown('EventFilter', ['all', 'account', 'payment'], description=u'筛选特定事件', value="All",),
		# web.form.Checkbox('ShortColumns', description=u'精简字段', value='True'), 
		web.form.Checkbox('Reversed', description=u'是否倒序', value=True, checked=True), 
		# web.form.Dropdown('OS', ['all', 'iOS', 'Android']),
		class_="fancyTable", #css settings
	)

class Statistic:
	"""统计服务日志
	"""
	def GET(self):
		form = myform()
		return render_template('list.html', form=form, result = None)

	def POST(self):
		form = myform()
		result = None
		if form.validates():
			result = CommandUtil.excute1(dev_id=form.d.DevID, app_id=form.d.AppID, event_filter=form.d.EventFilter, columns=form.d.Columns, lines=form.d.Lines, show_lines=form.d.ShowLines, reversed=form.d.Reversed)
			
		return render_template('list.html',form=form, result=result)
		# return render_template('list.html', headers=result.titles, records=raws, cmd=cmd, form=form)

class GameAd:
	"""游戏广告服务日志
	"""
	def GET(self):
		form = web.form.Form( 
			web.form.Textbox("queryStr", description=u'AppID、IDFA任意关键字'),
		)
		return render_template('gas.html', form=form, result = None)

	def POST(self):
		form = web.form.Form( 
			web.form.Textbox("queryStr", description=u'AppID？IDFA？'),
		)
		result = None
		if form.validates():
			result = CommandUtil.excute2(cmd_id='cmd_1', queryStr=form.d.queryStr)
			
		return render_template('gas.html',form=form, result=result)

if __name__ == "__main__":
	app.run()