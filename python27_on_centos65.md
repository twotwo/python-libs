# Installing Python 2.7 on Centos 6.5

Centos 6.\* comes with Python 2.6, but we can't just replace it with v2.7 because it's used by the OS internally (apparently) so you will need to install v2.7 (or 3.x, for that matter) along with it. Fortunately, CentOS made this quite painless with their [Software Collections Repository](http://wiki.centos.org/AdditionalResources/Repositories/SCL)

```bash
# yum update # update yum
# yum install centos-release-scl # install SCL
# yum install python27 # install Python 2.7
# /opt/rh/python27/root/usr/bin/python2.7 -V
/opt/rh/python27/root/usr/bin/python2.7: error while loading shared libraries: libpython2.7.so.1.0: cannot open shared object file: No such file or directory
```

To make 2.7 work, config `/etc/ld.so.conf.d/python27.conf`:

```bash
# /sbin/ldconfig -v |grep python
/sbin/ldconfig: /etc/ld.so.conf.d/kernel-2.6.32-642.el6.x86_64.conf:6: duplicate hwcap 1 nosegneg
/sbin/ldconfig: Path `/lib' given more than once
/sbin/ldconfig: Path `/usr/lib' given more than once
	libpyglib-2.0-python.so.0 -> libpyglib-2.0-python.so.0.0.0
	libpython2.6.so.1.0 -> libpython2.6.so.1.0
# find / -name libpython2.7.so.1.0
/opt/rh/python27/root/usr/lib64/libpython2.7.so.1.0
# echo '/opt/rh/python27/root/usr/lib64/' > /etc/ld.so.conf.d/python27.conf
# /sbin/ldconfig -v |grep python
/sbin/ldconfig: /etc/ld.so.conf.d/kernel-2.6.32-642.el6.x86_64.conf:6: duplicate hwcap 1 nosegneg
/sbin/ldconfig: Path `/lib' given more than once
/sbin/ldconfig: Path `/usr/lib' given more than once
/opt/rh/python27/root/usr/lib64:
	libpython2.7.so.1.0 -> libpython2.7.so.1.0
	libpyglib-2.0-python.so.0 -> libpyglib-2.0-python.so.0.0.0
	libpython2.6.so.1.0 -> libpython2.6.so.1.0
/opt/rh/python27/root/usr/lib64/tls: (hwcap: 0x8000000000000000)
/opt/rh/python27/root/usr/lib64/sse2: (hwcap: 0x0000000004000000)
# /opt/rh/python27/root/usr/bin/python2.7 -V
Python 2.7.13
```

To install additional libraries, you will need to install PIP:

```bash
# wget https://bootstrap.pypa.io/get-pip.py
# /opt/rh/python27/root/usr/bin/python2.7 get-pip.py
```

once installed, you can install PIP using `pip2.7`, e.g.:

```bash
# pip2.7 install requests
# /opt/rh/python27/root/usr/bin/pip -V
pip 18.0 from /opt/rh/python27/root/usr/lib/python2.7/site-packages/pip (python 2.7)
```

(Hack)Add in `~/.bash_profile` or `~/.zshrc`

```bash
alias python=/opt/rh/python27/root/usr/bin/python
alias pip=/opt/rh/python27/root/usr/bin/pip
export PATH=/opt/rh/python27/root/usr/bin:$PATH
```

`pip install -U pip # Update pip`

## Reference

- [Installing Python 2.7 on Centos 6.5](https://gist.github.com/dalegaspi/dec44117fa5e7597a559)
- [CentOS6系统安装Python2.7](https://www.jianshu.com/p/b8792a7b5350)