from distutils.core import setup
import py2exe

#send_mail.py, gen_excel.py
"""
python setup.py py2exe
"""
setup(console=['send_mail.py']) 
setup(console=['gen_excel.py'])