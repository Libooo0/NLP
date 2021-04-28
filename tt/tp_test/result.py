'''
先进行清晰度判别，再在不同阈值下进行ocr识别，逻辑较混乱
'''
# coding:utf-8
from paddleocr import PaddleOCR, draw_ocr
import cv2
import os
import pandas as pd
import xlwt

def init(root_path):
    data = []

    # 文件路径
    # root_path = r"C:\Users\86182\Desktop\tt\test_acc\test_picture"
    # 遍历图片路径
    for i in os.walk(root_path):
        print(i)
        for j in i[2]:
            img_path = os.path.join(i[0], j)

            # 图片清晰度的判定
            # 图片清晰度检测,拉普拉斯边缘检测，返回方差值，越大越清晰
            image = cv2.imread(img_path)
            img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()


            if imageVar <= 10:
                print(j,'模糊')
                data.append([j,'模糊'])

            elif 10 < imageVar < 175:
                # ocr图像文本识别
                ocr = PaddleOCR(use_pdserving=False, use_angle_cls=False, det=True, cls=True, use_gpu=False, lang="ch",
                                det_max_side_len=1500, det_db_thresh=0.2, det_db_box_thresh=0.3,
                                det_db_unclip_ratio=2.0,
                                gpu_mem=4000, rec_batch_num=10, cls_batch_num=10)
                result = ocr.ocr(img_path, det=True, rec=True, cls=False)

                # 计算平均置信度
                count = 0
                sum = 0
                for line in result:
                    l = line[1][1]
                    sum += l
                    count += 1
                if count != 0: # 识别不出文字
                    zx_value = sum / count
                    if zx_value > 0.7:
                        print(j,'清晰')

                        # 识别出文字整合文本
                        list = []
                        for line in result:
                            list.append(line[1][0])
                        text = ''.join(list)
                        print(j,text)

                        # 类型判断
                        if '中华人民共和国居民身份证' in text or '公民身份号码' in text or '常住人口登记卡' in text:
                            cls = '身份证明'
                        elif '出生医学证明' in text:
                            cls = '出生证明'
                        elif '户籍证明' in text:
                            cls = '户籍证明'
                        elif ('住院病历首页' in text or '住院病案首页' in text or '门诊病历' in text) and ("入院日期" in text or "入院时间" in text):
                            cls = '住院病历首页'
                        elif '入院记录' in text or "人院记录" in text:
                            cls = '入院记录'
                        elif ('入院通知' in text or '住院通知' in text or '入院告知' in text or '入院登记' in text or '入院证' in text or '住院证' in text or '住院登记证' in text) and ("保险" not in text):
                            cls = '入院通知书'
                        elif ('诊断证明' in text or '诊疗证明' in text or '门诊证明' in text or '疾病证明' in text) and '保险人' not in text:
                            cls = '诊断证明书'
                        elif '病理报告' in text or '病理会诊报告' in text or '病理检查报告' in text or '病理标本检查报告' in text or '病理诊断报告' in text:
                            cls = '病理报告'
                        elif "放射科CT报告" in text or "放射科MR报告" in text or "放射科检查报告" in text or "放射诊疗报告" in text or "影像检查报告" in text or "影像学" in text or "MR检查" in text or "DR检查" in text or "X线检查报告" in text or "超声报告" in text or "超声诊断报告" in text or "超声检查报告" in text or "DR影响诊断" in text or "CT诊断报告" in text or "CT检查" in text or "CT报告" in text or "CT扫描" in text:
                            cls = '影像检查报告'
                        elif '交通事故认定书' in text:
                            cls = '交通事故认定书'
                        elif '工伤事故证明' in text:
                            cls = '工伤证明'
                        elif "中华人民共和国机动车行驶证" in text or "中华人民共和国机动车驾驶证" in text:
                            cls = '行/驾驶证'
                        elif '持卡人签名' in text or '闪付Pass' in text or 'PayUnion' in text:
                            cls = '银行卡'
                        else:
                            cls = '其他'
                        print(j, cls)
                        data.append([j,'清晰',cls,text])
                    else:
                        print(j,'模糊')
                        data.append([j,'模糊'])
                else:
                    print(j,'模糊')
                    data.append([j, '模糊'])

            else:
                # ocr图像文本识别
                ocr = PaddleOCR(use_pdserving=False, use_angle_cls=False, det=True, cls=True, use_gpu=False, lang="ch",
                                det_max_side_len=1500, det_db_thresh=0.2, det_db_box_thresh=0.3,
                                det_db_unclip_ratio=2.0,
                                gpu_mem=4000, rec_batch_num=10, cls_batch_num=10)
                result = ocr.ocr(img_path, det=True, rec=True, cls=False)

                print(j,'清晰')

                # 识别出文字整合文本
                list = []
                for line in result:
                    list.append(line[1][0])
                text = ''.join(list)
                print(j,text)

                # 类型判断
                if '中华人民共和国居民身份证' in text or '公民身份号码' in text or '常住人口登记卡' in text:
                    cls = '身份证明'
                elif '出生医学证明' in text:
                    cls = '出生证明'
                elif '户籍证明' in text:
                    cls = '户籍证明'
                # elif ('住院病历首页' in text or '住院病案首页' in text or '门诊病历' in text) and ("入院日期" in text or "入院时间" in text):
                #     cls = '住院病历首页' # 不要
                elif '入院记录' in text or "人院记录" in text:
                    cls = '入院记录'
                elif ('入院通知' in text or '住院通知' in text or '入院告知' in text or '入院登记' in text or '入院证' in text or '住院证' in text or '住院登记证' in text) and ("保险" not in text):
                    cls = '入院通知书'
                elif ('诊断证明' in text or '诊疗证明' in text or '门诊证明' in text or '疾病证明' in text) and '保险人' not in text:
                    cls = '诊断证明书'
                elif '病理报告' in text or '病理会诊报告' in text or '病理检查报告' in text or '病理标本检查报告' in text or '病理诊断报告' in text:
                    cls = '病理报告'
                elif "放射科CT报告" in text or "放射科MR报告" in text or "放射科检查报告" in text or "放射诊疗报告" in text or "影像检查报告" in text or "影像学" in text or "MR检查" in text or "DR检查" in text or "X线检查报告" in text or "超声报告" in text or "超声诊断报告" in text or "超声检查报告" in text or "DR影响诊断" in text or "CT诊断报告" in text or "CT检查" in text or "CT报告" in text or "CT扫描" in text:
                    cls = '影像检查报告'
                elif '交通事故认定书' in text:
                    cls = '交通事故认定书'
                elif '工伤事故证明' in text:
                    cls = '工伤证明'
                elif "中华人民共和国机动车行驶证" in text or "中华人民共和国机动车驾驶证" in text:
                    cls = '行/驾驶证'
                elif '持卡人签名' in text or '闪付Pass' in text or 'PayUnion' in text:
                    cls = '银行卡'
                else:
                    cls = '其他'
                print(j,cls)
                data.append([j,'清晰',cls,text])
    for i in data:
        print(i)
    # 写入excel
    head = ['图片名', '清晰否', '类别', 'ocr图片识别结果']

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
    work_book.save('图片分类结果.xlsx')

if __name__ == "__main__":
    root_path = r'C:\Users\86182\Desktop\tt\test_acc\test3'
    init(root_path)
