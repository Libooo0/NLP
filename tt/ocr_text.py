# coding:utf-8
from paddleocr import PaddleOCR, draw_ocr
import cv2
import os
import pandas as pd
import xlrd
import xlwt


def Ocr_run(root_path):
    # 清晰度写入excel文件中
    data = []
    # 写入txt文件中
    with open('test.txt', 'w',encoding='utf-8') as f:
        f.write('label\ttext\n')
        # 文件路径
        # root_path = r"C:\Users\86182\Desktop\tt\test_acc\test_picture"
        for i in os.walk(root_path):
            for j in i[2]:
                img_path = os.path.join(i[0], j)

                # ocr识别
                ocr = PaddleOCR(use_pdserving=False, use_angle_cls=False, det=True, cls=True, use_gpu=False, lang="ch",
                                det_max_side_len=1500, det_db_thresh=0.2, det_db_box_thresh=0.3,
                                det_db_unclip_ratio=2.0,
                                gpu_mem=4000, rec_batch_num=10, cls_batch_num=10)
                result = ocr.ocr(img_path, det=True, rec=True, cls=False)

                # 将识别出的文字整合成文本
                list = []
                for line in result:
                    list.append(line[1][0])
                text = ''.join(list)

                # 写入到txt文件中
                f.write("0\t{}\n".format(text))

                # 图片清晰度的判定
                # 图片清晰度检测,拉普拉斯边缘检测，返回方差值，越大越清晰
                image = cv2.imread(img_path)
                img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()

                if imageVar <= 10:
                    qxd = '模糊'
                elif 10 < imageVar < 175:
                    # 计算平均置信度
                    count = 0
                    sum = 0
                    for line in result:
                        l = line[1][1]
                        sum += l
                        count += 1
                    if count != 0:  # 图片有无文字判断
                        zx_value = sum / count
                        if zx_value > 0.7:
                            qxd = '清晰'
                        else:
                            qxd = '模糊'
                    else:
                        qxd = '模糊'
                else:
                    qxd = '清晰'

                data.append([j,qxd])

    # 写入excel
    head = ['图片', '清晰判断']

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
    work_book.save('基于模型分类结果.xlsx')

if __name__ == "__main__":
    root_path = r'C:\Users\86182\Desktop\tt\test_acc\test5'
    Ocr_run(root_path)
