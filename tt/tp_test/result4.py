"""
只使用关键字对模型分类结果train.xlsx里的text进行分类
用于与基于模型和关键字分类的结果做对比
"""



# coding:utf-8
import xlrd
import xlwt
#打开excel
wb = xlrd.open_workbook(r'train.xlsx')
#按工作簿定位工作表
sh = wb.sheet_by_name('Sheet1')
# print(sh.row_values(570)[1])
# 按行读取
nrows = sh.nrows
data = []
for i in range(1,nrows):
    label = sh.row_values(i)[0]
    text = str(sh.row_values(i)[1])
    if '中华人民共和国居民身份证' in text or '公民身份号码' in text or '常住人口登记卡' in text:
        cls = '身份证'
    # 出生证明
    elif '出生医学证明' in text:
        cls = '出生证明'
    # 户籍证明
    elif '户籍证明' in text:
        cls = '户籍证明'
    # 入院通知书
    elif ('入院通知' in text or '住院通知' in text or '入院告知' in text or '入院登记' in text or '入院证' in text or '住院证' in text or '住院登记证' in text) and ("保险人" not in text):
        cls = '入院通知书'
    # 交通事故认定书
    elif '道路交通事故认定书' in text:
        cls = '交通事故认定书'
    # 工伤证明
    elif '工伤事故证明' in text:
        cls = '工伤证明'
    # 行驶证/驾驶证
    elif "中华人民共和国机动车行驶证" in text or "中华人民共和国机动车驾驶证" in text:
        cls = '行/驾驶证'
    # 银行卡
    elif '持卡人签名' in text or '闪付Pass' in text or 'PayUnion' in text:
        cls = '银行卡'
    # 入院记录
    elif '入院记录' in text or "人院记录" in text or "住院记录" in text:
        cls = '入院记录'
    elif ('诊断证明' in text or '诊疗证明' in text or '门诊证明' in text or '疾病证明' in text) and '保险人' not in text:
        cls = '诊断证明书'
    # 影像检查报告
    elif "镜检所见" in text or "检查所见" in text or "影像描述" in text or "影像表现" in text or "超声描述" in text or "放射科CT报告" in text or "放射科MR报告" in text or "放射科检查报告" in text or "放射诊疗报告" in text or "影像检查报告" in text or "影像学" in text or "MR检查" in text or "MR" in text or "MRI诊断报告" in text or "DR检查" in text or "X线检查报告" in text or "超声报告" in text or "超声诊断报告" in text or "超声检查报告" in text or "DR影响诊断" in text or "CT诊断报告" in text or "CT检查" in text or "CT报告" in text or "CT扫描" in text:
        cls = '影像检查报告'
    # 病理报告
    elif '病理报告' in text or '病理会诊报告' in text or '病理检查报告' in text or '病理标本检查报告' in text or '病理诊断报告' in text or "病理号" in text:
        cls = '病理报告'
    # 其他
    else:
        cls = '其他'
    print([label,cls,text])
    data.append([label, cls, text])

# 写入excel
head = ['label','class','ocr图片识别结果']

work_book = xlwt.Workbook(encoding='utf-8')
sheet = work_book.add_sheet(sheetname='sheet1')
# 写表头
for i in range(len(head)):
    sheet.write(0, i, head[i])
# 写内容
for i in range((len(data))):
    for j in range(len(data[i])):
        sheet.write(i + 1, j, data[i][j])
# 5.保存
work_book.save('关键字分类结果1.xlsx')

