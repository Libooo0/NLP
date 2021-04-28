# 工作簿
# 表单 - sheet
# 单元格 - cell
# 行 - row
# 列 - col

import xlrd
# 读取excel
# 1.打开一个工作簿
work_book = xlrd.open_workbook(r'学生信息.xlsx')
# 2.获取一个sheet表单
sheet_names = work_book.sheet_names()
sheet_first = work_book.sheet_by_name(sheet_names[0])
# 3.通过sheet表单进行按行或按列读取
# 按行读取
nrows = sheet_first.nrows
# print(nrows)
for i in range(nrows):
    print(sheet_first.row_values(i))
# 按列读取
ncols = sheet_first.ncols
for j in range(ncols):
    print(sheet_first.col_values(j))

# 获取单元格内容
print(sheet_first.cell_value(1,0))
