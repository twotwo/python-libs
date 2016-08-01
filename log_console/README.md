日志查看控制台
==============


依赖库
-------
 * python v2.7.x: https://www.python.org/downloads/release/python-2711/
 * web.py: http://wiki.li3huo.com/webpy
 * Jinja2: http://wiki.li3huo.com/Python_Template_Engine#Jinja2


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
[root@localhost ~]# supervisorctl restart console
console: stopped
console: started



