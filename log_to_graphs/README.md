# 日志转图工具

## Environment

[Installing Python 2.7 on Centos 6.5](../python27_on_centos65.md)

`pip install matplotlib numpy cairocffi`
 * matplotlib: http://wiki.li3huo.com/matplotlib
 * NumPy: http://wiki.li3huo.com/NumPy
 * cairo(EC2): py2cairo, cairo, cairocffi

## 功能描述

### 帮助脚本: gen_report.sh

- pay

		#!/bin/sh
		rm /data/daily_report/pay-log/gamepay_daily_report.png
		yesterday=`date -d last-day +%Y%m%d`;
		logfile="/data/daily_report/pay-log/report/pay_perform.log.${yesterday}";
		rsync -avzp -e "ssh -p 2188" 10.75.0.167:/backup/pay-log/pay_perform.log.${yesterday} /data/daily_report/pay-log/10.75.0.167/
		rsync -avzp -e "ssh -p 2188" 10.75.1.139:/backup/pay-log/pay_perform.log.${yesterday} /data/daily_report/pay-log/10.75.1.139/
		sort -m /data/daily_report/pay-log/10.75.0.167/pay_perform.log.${yesterday} /data/daily_report/pay-log/10.75.0.167/pay_perform.log.${yesterday} -o ${logfile}
		picfile="/data/daily_report/pay-log/report/daily-report-${yesterday}.png";
		python /data/daily_report/daily_log_plot.py -f "${logfile}" -p ${picfile} -t "GamePay Daily Report(${yesterday})" --not-show
		cp ${picfile} /data/daily_report/pay-log/gamepay_daily_report.png

- logon_v4

		#!/bin/sh
		rm /data/daily_report/logon_v4-log/logon_daily_report.png
		basedir=/data/daily_report/logon_v4-log
		yesterday=`date -d last-day +%Y%m%d`;
		logfile="${basedir}/report/gamesdk_conn.log.${yesterday}";
		for ip in 10.75.1.47 10.75.0.71 10.75.1.20; do
		rsync -avzp -e "ssh -p 2188" ${ip}:/backup/sdk-log/gamesdk/gamesdk_conn.log.${yesterday} ${basedir}/${ip}/
		done
		sort -m ${basedir}/10.75.1.47/gamesdk_conn.log.${yesterday} ${basedir}/10.75.0.71/gamesdk_conn.log.${yesterday} ${basedir}/10.75.1.20/gamesdk_conn.log.${yesterday} -o ${logfile}
		picfile="${basedir}/report/daily-report-${yesterday}.png";
		cmd="cut -c11-19 ${logfile} |sort | uniq -c"
		python /data/daily_report/daily_log_plot.py -c "${cmd}" -p ${picfile} -t "GameLogon(V4) Daily Report(${yesterday})" --not-show
		cp ${picfile} ${basedir}/logon_daily_report.png

		# clean used data
		for ip in 10.75.1.47 10.75.0.71 10.75.1.20; do
		rm ${basedir}/${ip}/gamesdk_conn.log.`date -d "-2 day" +%Y%m%d`
		done
		rm ${basedir}/report/gamesdk_conn.log.*


		# 本机定期执行，激活生成昨日日志
		1 0 * * * curl -X POST http://localhost:8081/feiliupay4j/gateway/newtrade/0/
		tail -f /backup/pay-log/pay_perform.log
- sdk-agent(/data/sdk-agent-data/daily_logs/send_report.sh)

		#!/bin/sh
		cd /data/sdk-agent-data/daily_logs
		rm -rf agent.npz agent.png
		yesterday=`date -d last-day +%Y-%m-%d`;
		python numpy_helper.py -c parse -i helper.ini -s agent # parse agent log & save data
		python daily_log_plot.py -n agent.npz -p agent.png --not-show -t "Project SDK-Agent on Date ${yesterday}" #load agent.npz & paint to agent.png
		python mail_tool.py


		20 2 * * * sh /data/sdk-agent-data/daily_logs/send_report.sh


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


## 生成日报表的过程(./gen-report.sh)

### 1. 日志汇总&合并

```bash
#!/bin/sh

yesterday=`date -d last-day +%Y%m%d`
logfile="/var/log/platform/access.log-${yesterday}"
store_dir=/data0/monitor/daily_logs/platform_log

# load logs to ${store_dir}
for ip in 10.163.61.176 10.163.57.246; do
  rsync -avzp -e "ssh -p 22" ${ip}:${logfile} ${store_dir}/${yesterday}_${ip}.log
done

# merge logs to ${store_dir}/${yesterday}.log
sort -m ${store_dir}/${yesterday}_*.log -o ${store_dir}/${yesterday}.log

merge_filter=$1
if [ -n "${merge_filter}" ]; then
	sort -m ${store_dir}/${yesterday}_*.log |grep ${merge_filter} > ${store_dir}/${yesterday}.log
else
  sort -m ${store_dir}/${yesterday}_*.log -o ${store_dir}/${yesterday}.log
fi

```

### 2. log to data(numpy_helper.py)

```bash
# 准备python脚本执行环境
pip install virtualenv
virtualenv env
source env/bin/activate
# 安装需要的类库
pip install matplotlib numpy cairocffi
```

```bash
src_dir=/data0/monitor/daily_logs
ini_file=/data0/monitor/daily_logs/helper.ini
pic_file="/data0/monitor/daily_logs/report/daily-report-${yesterday}.png";
PATH=${src_dir}/env/bin:$PATH
python ${src_dir}/numpy_helper.py -c parse -i ${ini_file} -s platform
```

### 3. data to graphs(daily_log_plot.py)

```bash
python ${src_dir}/daily_log_plot.py -n ${src_dir}/platform.npz -p ${pic_file} -tt
 "Web Platform Daily Report(${yesterday})" --not-show
cp ${pic_file} ${src_dir}/platform_daily_report.png
```


### 4. add to crontab

```bash
crontab -e
# generate report on 2:00 am
0 2 * * * sh /data0/monitor/daily_logs/gen-report.sh
#30 11 * * * sh /data0/monitor/daily_logs/gen-report.sh
# send mail on 2:20 am
20 2 * * * python /data0/monitor/daily_logs/mail_tool.py platform
#05 17 * * * python /data0/monitor/daily_logs/mail_tool.py platform
```