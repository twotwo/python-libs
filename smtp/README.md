# Mail Sending Tool

## Usa Guide

### 1. Write your own main.ini

```ini
[basic]
# Home Path for Mail Tool(include working log)
base_dir=/tmp/smtp

# smtp config
[smtp]
host=mail.server.com
port=25
# 超时时间设置为60s
timeout=60
user=
password=

debug_mode=False
use_ssl=False


[test]
from = sender@server.com
to = liyan@server.com
cc = liyan@server.com
reply_to = liyan@server.com
subject = [OnLine Daily Report]
content = generate by<pre>tools-python/smtp/mail_tool.py</pre>
files = ~/app/python/matplotlib/chart.png

# add your own section
```

### 2. Install Packages(only for Python 3.x)

```bash
virtualenv env
source env/bin/activate
pip install ConfigParser
```

### 3. Send Mail

```bash
python mail_tool.py test #[your section name]
```

### 4. Send Everyday

```bash
crontab -e
# excute on 2:20 am
20 2 * * * python /data0/monitor/daily_logs/mail_tool.py platform
```
