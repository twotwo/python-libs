# -*- coding: utf8 -*-

###########################
# [xlrd api](http://xlrd.readthedocs.io/en/latest/api.html)
#
###########################

import xlrd, os, time

def read_excel(file_path):
	file_name = os.path.basename(file_path)
	workbook = xlrd.open_workbook(file_path, encoding_override='gb2312')
	# print 'loading sheets: ' + ', '.join(workbook.sheet_names())
	for sheet_name in workbook.sheet_names():
		sheet = workbook.sheet_by_name(sheet_name)
		num_rows = sheet.nrows
		num_cells = sheet.ncols
		print '-- file = %s, sheet = %s, rows = %d, cells = %d' % (file_name, sheet_name, num_rows, num_cells)
		for num_row in range(0,num_rows):
			values = sheet.row_values(num_row) #sheet.cell_value(num_row, 1)
			# print 'file = %s, sheet = %s, value = %s' % (file_name, sheet_name, ''.join(values))
			format_sql(file_name, sheet_name, ''.join(values))
			break

def format_sql(f, s, v):
	# gift_id对应文件名f？ 
	gift_id = get_gift_id(f)
	# 开始、结束时间对应sheet名称s
	(s_time, e_time) = get_timerange(s)
	print 'insert into papa2_activity_giftcode(gift_id,code,start_time,end_time,status) values(%s, "%s", %d, %d, 0)' % (gift_id, v, s_time, e_time)
	print '...'

def get_gift_id(f):
	if len(f)>10:
		return f[7:10]
	else:
		return '0'

# 开始日期换算成秒数
base_time = time.mktime(time.strptime("2018-2-23","%Y-%m-%d"))
time_range =24*60*60 # 1天的秒数
def get_timerange(s):
	d = int(s[-1])
	start_time = base_time + d*time_range
	return(start_time, start_time+time_range)

def main():
	for file in os.listdir('/tmp/code'):
		if file.endswith(".xlsx"):
			read_excel(file)


if __name__ == '__main__':
	main()