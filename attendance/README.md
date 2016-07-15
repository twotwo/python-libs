考勤通知系统 V2.0
==============


依赖库
-------
 * python v2.7.x: https://www.python.org/downloads/release/python-2711/
 * xlrd/xlwt: http://wiki.li3huo.com/python_lib_excel
 * Jinja2: http://wiki.li3huo.com/Python_Template_Engine#Jinja2
 * py2exe: http://wiki.li3huo.com/py2exe

### 可执行程序生成
python setup.py py2exe

使用说明
--------

### [生成考勤记录汇总表] 原始考勤记录表(考勤机导出的xls) -> 考勤记录汇总表

 1. 配置文件(mail.ini)：配置考勤生成路径、本次考勤开始和结束日期；发送邮件所有的邮箱账号等
 2. 执行汇总命令: gen_excel.exe；检查生成日志
 3. 检查考勤汇总表和待通知邮件(${base_dir}/outbox)

### [发送考勤异常提醒邮件] 把考勤记录汇总表中的异常记录发送给对应员工

 1. 配置邮箱等相关信息: gen_excel
 2. 点击发送邮件命令:send_mail.exe
 3. 查看邮件发送状态
 	Outbox(待发送): ${base_dir}/outbox
 	sent(已发送): ${base_dir}/sent_box


### 一般问题

 1. [生成考勤记录汇总表]执行文件闪退
	检查配置文件(mail.ini)，base_dir路径是否已经存在

 2. [生成考勤记录汇总表]待通知邮件显示unknow字样
	正确生成的待通知邮件格式是：文件名是<姓名>_<部门>_邮件地址_.html

	<姓名>_<部门>_unknow_.html说明，按照姓名搜索出来的地址为空或者没有记录，请让姓名和邮件地址匹配
	
	举个例子：例如，张三_部门_unknow_.html
	打开mail.xlsx，找到： 张三;没有
	
	添加一条记录：
	部门随便	张三	88888@qq.com

	然后清空outbox目录后再次生成通知邮件，对应记录变成：
	张三_部门_88888@qq.com_.html
	

 3. [发送考勤异常提醒邮件]游戏账号配置错误
    请找系统部重置邮箱密码

 4. [发送考勤异常提醒邮件]邮件状态查看
    检查outbox(待发送)目录，此目录存放待发送内容
    sent_box是已发送目录，存放已经成功发送的内容
    在点击发送前检查生成的内容是否正常；
    发送后查看待发送目录是否有发送失败的邮件
