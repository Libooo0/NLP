dict_keyword = {
    "身份证明":["中华人民共和国居民身份证","公民身份号码","常住人口登记卡"],
    "出生证明":["出生医学证明"],
    "户籍证明":["户籍证明"],
    "入院记录": ["入院记录","人院记录","住院记录"],
    "入院通知书":["入院通知","住院通知","入院告知","入院登记","入院证","住院证","住院登记证"], # 保险人不在
    "诊断证明书":["诊断证明","诊疗证明","门诊诊断","疾病证明"], # 保险人不在
    # "住院病历首页":["住院病历首页","住院病案首页","门诊病历"],
    "病理报告":["病理报告","病理会诊报告","病理检查报告","病理标本检查报告","病理诊断报告","病理号"],
    "影像检查报告":["检查所见","影像描述","影像表现","超声描述","放射科CT报告","放射科MR报告","放射科检查报告","放射诊疗报告","影像检查报告","影像学检查","影像学（CT）报告","影像学（MR)诊断报告","影像学（DR）诊断报告","MR检查","DR检查","X线检查报告","超声报告","超声诊断报告","超声检查报告","DR影响诊断","CT诊断报告","CT检查","CT报告","CT扫描"],
    # "残疾/失能鉴定书":["残疾鉴定书","失能鉴定书"],
    "交通事故认定书":["道路交通事故认定书"],
    "工伤证明":["工伤事故证明"],
    "行驶/驾驶证":["中华人民共和国机动车行驶证","中华人民共和国机动车驾驶证"],
    "银行卡":["持卡人签名","PyUnion","闪付Pass"]
}

for key in dict_keyword:
    for word in dict_keyword[key]:
        if word in text and '保险人' not in text:
            cls = dict_keyword[key]


# 类型判断
dict_keyword = {
    "身份证明": ["中华人民共和国居民身份证", "公民身份号码", "常住人口登记卡"],
    "出生证明": ["出生医学证明"],
    "户籍证明": ["户籍证明"],
    "入院记录": ["入院记录", "人院记录", "住院记录"],
    "入院通知书": ["入院通知", "住院通知", "入院告知", "入院登记", "入院证", "住院证", "住院登记证"],  # 保险人不在
    "诊断证明书": ["诊断证明", "诊疗证明", "门诊诊断", "疾病证明"],  # 保险人不在
    # "住院病历首页":["住院病历首页","住院病案首页","门诊病历"],
    "病理报告": ["病理报告", "病理会诊报告", "病理检查报告", "病理标本检查报告", "病理诊断报告", "病理号"],
    "影像检查报告": ["检查所见", "影像描述", "影像表现", "超声描述", "放射科CT报告", "放射科MR报告", "放射科检查报告", "放射诊疗报告", "影像检查报告", "影像学检查",
               "影像学（CT）报告", "影像学（MR)诊断报告", "影像学（DR）诊断报告", "MR检查", "DR检查", "X线检查报告", "超声报告", "超声诊断报告",
               "超声检查报告", "DR影响诊断", "CT诊断报告", "CT检查", "CT报告", "CT扫描"],
    # "残疾/失能鉴定书":["残疾鉴定书","失能鉴定书"],
    "交通事故认定书": ["道路交通事故认定书"],
    "工伤证明": ["工伤事故证明"],
    "行驶/驾驶证": ["中华人民共和国机动车行驶证", "中华人民共和国机动车驾驶证"],
    "银行卡": ["持卡人签名", "PyUnion", "闪付Pass"]
}

for key in dict_keyword:
    for word in dict_keyword[key]:
        if word in text and '保险人' not in text:
            cls = dict_keyword[key]
        else:
            cls = '其他'

        # 结果添加进data
        data.append([j,qxd,cls,text])

# 类型判断
# # 身份证明判断
# if '中华人民共和国居民身份证' in text or '公民身份号码' in text or '常住人口登记卡' in text:
#     cls = '身份证'
# # 出生证明
# elif '出生医学证明' in text:
#     cls = '出生证明'
# # 户籍证明
# elif '户籍证明' in text:
#     cls = '户籍证明'
# # elif ('住院病历首页' in text or '住院病案首页' in text or '门诊病历' in text) and ("入院日期" in text or "入院时间" in text):
# #     cls = '住院病历首页' # 不要
# # 入院记录
# elif '入院记录' in text or "人院记录" in text or "住院记录" in text:
#     cls = '入院记录'
# # 入院通知书
# elif ('入院通知' in text or '住院通知' in text or '入院告知' in text or '入院登记' in text or '入院证' in text or '住院证' in text or '住院登记证' in text) and ("保险人" not in text):
#     cls = '入院通知书'
# # 诊断证明
# elif ('诊断证明' in text or '诊疗证明' in text or '门诊证明' in text or '疾病证明' in text) and '保险人' not in text:
#     cls = '诊断证明书'
# # 病理报告
# elif '病理报告' in text or '病理会诊报告' in text or '病理检查报告' in text or '病理标本检查报告' in text or '病理诊断报告' in text or "病理号" in text:
#     cls = '病理报告'
# # 影像检查报告
# elif "镜检所见" in text or "检查所见" in text or "影像描述" in text or "影像表现" in text or "超声描述" in text or "放射科CT报告" in text or "放射科MR报告" in text or "放射科检查报告" in text or "放射诊疗报告" in text or "影像检查报告" in text or "影像学" in text or "MR检查" in text or "MR" in text or "MRI诊断报告" in text or "DR检查" in text or "X线检查报告" in text or "超声报告" in text or "超声诊断报告" in text or "超声检查报告" in text or "DR影响诊断" in text or "CT诊断报告" in text or "CT检查" in text or "CT报告" in text or "CT扫描" in text:
#     cls = '影像检查报告'
# # 交通事故认定书
# elif '道路交通事故' in text:
#     cls = '交通事故认定书'
# # 工伤证明
# elif '工伤事故证明' in text:
#     cls = '工伤证明'
# # 行驶证/驾驶证
# elif "中华人民共和国机动车行驶证" in text or "中华人民共和国机动车驾驶证" in text:
#     cls = '行/驾驶证'
# # 银行卡
# elif '持卡人签名' in text or '闪付Pass' in text or 'PayUnion' in text:
#     cls = '银行卡'
# # 其他
# else:
#     cls = '其他'