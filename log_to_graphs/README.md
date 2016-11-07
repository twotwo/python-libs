# 日志转图工具 #



## 依赖

 * matplotlib: http://wiki.li3huo.com/matplotlib
 * NumPy: http://wiki.li3huo.com/NumPy
 * cairo(EC2): py2cairo, cairo

## 功能描述

### 帮助脚本: gen_report.sh
multitail --no-repeat -z -u 1 -l 'ssh 10.75.1.139 -p2188 "cat /backup/pay-log/pay_perform.log"' > 1.txt
rsync -avzp -e "ssh -p 2188" 10.75.1.139:/backup/pay-log/pay_perform.log /data/daily_report/pay-log/10.75.1.139/pay_perform.log
sort -m /data/pay-log/10.75.1.139/pay_perform.log -o /data/pay-log/pay_perform.log

	#!/bin/sh
	rm /data/daily_report/pay-log/gamepay_daily_report.png
	yesterday=`date -d last-day +%Y%m%d`;
	logfile="/data/daily_report/pay-log/report/pay_perform.log.${yesterday}";
	rsync -avzp -e "ssh -p 2188" 10.75.1.139:/backup/pay-log/pay_perform.log.${yesterday} /data/daily_report/pay-log/10.75.1.139/
	sort -m /data/daily_report/pay-log/10.75.1.139/pay_perform.log.${yesterday} -o ${logfile}
	picfile="/data/daily_report/pay-log/report/daily-report-${yesterday}.png";
	python /data/daily_report/daily_log_plot.py -f "${logfile}" -p ${picfile} -t "GamePay Daily Report(${yesterday})" --not-show
	cp ${picfile} /data/daily_report/pay-log/gamepay_daily_report.png

### numpy_helper.py
日志解析和存储

* 业务日志格式

		[boss@ip-10-75-0-25 monkeysdk]$ head /data/monkeysdk/logs/sdk_perform.log 
		2016-10-17 00:00:01 ip-10-75-0-24 \x02300001\x02100288\x02725790\x0288CD388A-D878-4B0C-90C2-CC7D00F55E88\x025000\x02\x022\x020

		\x02分隔符，依次为： 渠道ID, 游戏ID， 设备ID，IDFA, 协议ID， userId, 响应时间(ms)，返回状态码（0成功，1失败）


		[feiliu-user@ip-10-75-1-139 pay-log]$ head /backup/pay-log/pay_perform.log
		2016-11-07 14:59:58\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02newtrade\x02420\x020\x02

* 解析概述

		# 解析response
		line.split('\x02')[0][11:19] //时间
		int( line.split('\x02')[0][11:13] )
		int( line.split('\x02')[7] ) // 响应时间(ms)
		int( line.split('\x02')[8] ) //服务状态

		# 解析thoughput
		cmd='cut -c11-19 sdk_perform.log |sort | uniq -c'

		from subprocess import Popen, PIPE
		for line in Popen(cmd, shell=True, bufsize=102400, stdout=PIPE).stdout:
			print line.strip()

		with open('hello.txt') as f:
		    for line in f:
		        print line,


### daily_log_plot.py
把numpy_helper.py中解析出来的数据进行处理和出图


### Others: ../smtp/mail_tool.py 把报告以邮件形式进行发送



