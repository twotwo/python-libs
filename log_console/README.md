日志查看控制台
==============


依赖
-------
 * [git](http://wiki.li3huo.com/Git)
 * [python v2.7.x](https://www.python.org/downloads/release/python-2711/)
 * [supervisor](http://wiki.li3huo.com/supervisor):  pip install --upgrade pip; pip install --upgrade --force-reinstall setuptools supervisor pip Distribute
 * [web.py](http://wiki.li3huo.com/webpy)
 * [Jinja2](http://wiki.li3huo.com/Python_Template_Engine#Jinja2)

安装
-------

 	mkdir -p /srv/src /srv/www; cd /srv/src; git clone https://github.com/twotwo/tools-python.git
 	ln -s /srv/src/tools-python/log_console/ /srv/www/console
 	cd /srv/www/console; pip install virtualenv --upgrade
 	virtualenv env; source env/bin/active
 	pip install web.py jinja2
 	mkdir /etc/supervisord; ln -s /srv/www/console/supervisor.conf /etc
 	ln -s /srv/www/console/supervisor_console.ini /etc/supervisord/console.ini

功能描述
--------
### 默认显示最后100条统计日志

### 根据DevID查询指定设备的日志

 1. DevID对应Android版的IMEI或iOS的IDFA

 2. 可以指定tail的行数：默认5000行，最大100000行

 3. 可以翻转记录的排序方式

 4. 支持显示不同的字段：全部，19个字段和12个字段

 5. 支持对EventId的筛选


配置说明
--------

### supervisor

 1. 

### nginx

### 日常运维
cd tools-python/log_console/; git pull
[root@localhost ~]# supervisorctl restart console
console: stopped
console: started



