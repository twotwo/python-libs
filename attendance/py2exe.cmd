python setup.py py2exe
rem 如果没有import新库，仅仅修改code，只更新exe就可以了
move dist\gen_excel.exe dist\1.考勤汇总.exe
move dist\send_mail.exe dist\2.发送邮件.exe
