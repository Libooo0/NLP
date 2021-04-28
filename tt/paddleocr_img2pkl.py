import os
import cv2
from paddleocr import PaddleOCR
from math import asin
import pandas as pd
import pickle
import math
import numpy as np
import re
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


paddle_cls = r'D:\paddle_server_model\ch_ppocr_mobile_v1.1_cls_infer'
paddle_det = r'D:\paddle_server_model\ch_ppocr_server_v1.1_det_infer'
paddle_rec = r'D:\paddle_server_model\ch_ppocr_server_v1.1_rec_infer'
ocr = PaddleOCR(cls=True, use_angle_cls=False, use_space_char=False, use_gpu=False,
                    rec_model_dir=paddle_rec,
                    cls_model_dir=paddle_cls,
                    det_model_dir=paddle_det,
                    det_max_side_len=960, det_db_thresh=0.1, det_db_box_thresh=0., det_db_unclip_ratio=1.5,
                    ggpu_mem=1400, rec_batch_num=3, cls_batch_num=3) # 5500 12 12
def run_ocr(img):
    # ocr = PaddleOCR(cls=True, use_angle_cls=False, use_space_char=False, use_gpu=True,
    #                 rec_model_dir=paddle_rec,
    #                 cls_model_dir=paddle_cls,
    #                 det_model_dir=paddle_det,
    #                 det_max_side_len=960, det_db_thresh=0.1, det_db_box_thresh=0., det_db_unclip_ratio=1.5,
    #                 ggpu_mem=1400, rec_batch_num=3, cls_batch_num=3) # 5500 12 12
    result = ocr.ocr(img, det=True, rec=True, cls=False)
    return result

def read_img(imgpath):
    img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    r = -1
    if len(cv2.split(img)) == 4:
        b, g, r, d = cv2.split(img)
    if len(cv2.split(img)) == 3:
        b, g, r = cv2.split(img)
    if len(cv2.split(img)) == 2:
        b, r = cv2.split(img)
    if len(cv2.split(img)) == 1:
        r = img
    # #### 原图叠加
    print(len(cv2.split(img)))
    # r = cv2.add(-r, -r)
    r = -r
    imgadd = cv2.merge([-r, -r, -r]).astype('f4')
    return imgadd


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    if not np.isnan((h * sin) + (w * cos)):
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))

def nextlevel(level1_p,file_list):
    if os.path.isdir(level1_p):
        # print(level1_p)
        level1_list = os.listdir(level1_p)
        for file1 in level1_list:
            level2_p = os.path.join(level1_p, file1)
            nextlevel(level2_p,file_list)
    if os.path.isfile(level1_p):
        file_path = level1_p
        if file_path not in file_list:
            # if file_path[-4:] == '.png':
                file_list.append(file_path)
    return file_list

def write_txt(better_filename, result):
    result = x1_close(result)
    with open(better_filename.replace('.png', '.txt').replace('.jpg', '.txt'), 'w',
              encoding='utf8') as f:
        # f.writelines(''.join([i[1][0]+'\n' for i in result]))
        f.writelines(x1_text(result))

def xy_near2same(y1, last_y1, default_limit):
    if not last_y1:
        last_y1 = y1
    if last_y1:
        if abs(y1 - last_y1) < default_limit:
            y1 = last_y1
        if abs(y1 - last_y1) > default_limit:
            last_y1 = y1
    return y1,last_y1

# y1 = one[0][3][1]
# x1 = one[0][3][0]
# x2 = one[0][2][0]
def x1_close(result):
    x1list = []
    x2list = []
    ylist = []
    last_x1 = 0
    last_x2 = 0
    last_y1 = 0
    default_limit = 6

    result2 = result.copy()
    for idx in range(len(result)):
        result2[idx].append(idx)
    result = result2
    
    result = sorted(result, key=lambda x:x[0][3][0])
    for idx in range(len(result)):
        x1 = result[idx][0][3][0]
        result[idx][0][3][0], last_x1 = xy_near2same(x1, last_x1, default_limit)
        x1list.append(result[idx][0][3][0])

    result = sorted(result, key=lambda x:x[0][2][0])
    for idx in range(len(result)):
        x2 = result[idx][0][2][0]
        result[idx][0][2][0], last_x1 = xy_near2same(x2, last_x2, default_limit)
        x2list.append(result[idx][0][2][0])

    result = sorted(result, key=lambda x:x[0][3][1])
    for idx in range(len(result)):
        y1 = result[idx][0][3][1]
        result[idx][0][3][1], last_y1 = xy_near2same(y1, last_y1, 25)
        ylist.append(result[idx][0][3][1])
    result = sorted(result, key=lambda x: x[2])
    return result

def img2pkl(base, text_ed_path):
    print('img2pkl running....')
    file_list = []
    file_list = nextlevel(base, file_list)
    c = 0
    file_ed = []
    for file in file_list:
        if (file[-4:] == '.png') or (file[-4:] == '.jpg'):
            file = file.replace('\\'[0], '\\').replace('/', '\\')
            print(os.path.join(base, file))
            file_name = file.split('\\')[-1]
            last_dit = file.split('\\')[-2]
            # img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
            img = read_img(file)
            img_shape = img.shape
            print('img_shape', img_shape)
            betterpath = text_ed_path + '\\' + last_dit
            better_filename = betterpath + '\\' + file_name
            if not os.path.exists(betterpath):
                os.makedirs(betterpath)
            if os.path.exists(better_filename.replace('.png', '.pkl').replace('.jpg', '.pkl')):
                file_ed.append(betterpath)
                # 读PKL
                # print(betterpath+ '\\'+ file_name.replace('.png','.pkl').replace('.jpg','.pkl'))
                result = pickle.load(open(better_filename.replace('.png','.pkl').replace('.jpg','.pkl'), 'rb'))
                result = x1_close(result)
                write_txt(better_filename, result)
                c +=1
                print('111')
                continue

            try:
                result = run_ocr(img)
            except:
                file_ed.append(betterpath)
                print('222')
                continue

            # 二次识别
            resultr = sorted(result, key=lambda x: abs(x[0][2][0] - x[0][3][0]), reverse=True)
            resultr = resultr[:int(len(result) * 0.3)]
            offset = np.array([(x[0][2][1] - x[0][3][1]) / (x[0][2][0] - x[0][3][0]) for x in resultr]).mean()
            angle = 0
            try:
                angle = (asin(offset) * 100 - 1) * 3 / 5 + 0.5
            except:
                print('333')
                continue
            print('angle',angle)
            if abs(angle) <=0.04:

                pickle.dump(result,open(better_filename.replace('.png', '.pkl').replace('.jpg', '.pkl'),'wb'))
                # cv2.imwrite(better_filename.replace('.jpg', '.png'), img,
                #             [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                write_txt(better_filename, result)
                c +=1
                file_ed.append(betterpath)
                print('save to:', better_filename.replace('.png', '.txt').replace('.jpg', '.txt'))
                print("已提取%d张图片" % c)
                print('444')
                continue

            if abs(angle) >0.04:
                if not np.isnan(offset):
                    img = rotate_bound(img, angle)

                try:
                    result = run_ocr(img)
                except:
                    file_ed.append(betterpath)
                    print('555')
                    continue
                pickle.dump(result,open(better_filename.replace('.png','.pkl').replace('.jpg','.pkl'),'wb'))
                # cv2.imwrite(better_filename.replace('.jpg', '.png'), img,
                #             [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                write_txt(better_filename, result)
                c += 1

                file_ed.append(betterpath)

                print('save to:', better_filename.replace('.png', '.txt').replace('.jpg', '.txt'))
                print("已提取%d张图片" % c)

    if file_ed:
        return file_ed[0]


def have_any(data_col):
    flag = False
    for i in data_col:
        if i:
            if str(i).strip():
                flag = True
                # print(i,flag)
                break
    # print(flag)
    return flag

def get_ww_hh(results):
    x1min, x1max, y1min, y1max = 0, 0, 0, 0
    for one in results:
        y1 = int(one[0][3][1])
        x1 = int(one[0][3][0])
        if not x1min:
            x1min = x1
        if x1min > x1:
            x1min = x1
        if not y1min:
            y1min = y1
        if y1min > y1:
            y1min = y1
        if x1 > x1max:
            x1max = x1
        if y1 > y1max:
            y1max = y1
    ww = x1max - x1min
    hh = y1max - y1min
    return ww, hh

def x1_text(results):
    ww, hh = get_ww_hh(results)
    item_v = 20
    ## 网格
    col = int(ww / item_v)
    row = int(hh / item_v)
    data = pd.DataFrame({str(i) : [''] for i in range(col)})
    results = x1_close(results)

    for one in results:
        y1 = one[0][3][1]
        y2 = one[0][2][1]
        x1 = one[0][3][0]
        x2 = one[0][2][0]
        str1 = one[1][0]

        w_r = y1
        xx_r = x1
        if not np.isnan(w_r / item_v):
            w_row = math.floor(w_r / item_v)
            x_col = math.floor(xx_r / item_v)
            if x_col < 0:
                x_col = 0
            data.loc[w_row, str(x_col)] = str1

    col = data.columns
    data.index = range(len(data))
    for i1 in col:
        if not have_any(data[i1].tolist()):
            data = data.drop(i1, axis=1)
    for idx in range(len(data)):
        if not have_any(data.loc[idx].tolist()):
            data = data.drop(idx)
    # print(data.info)
    data.index = range(len(data))
    data = data.fillna('')
    row_list = []
    for idx in range(len(data)):
        rowlistd = data.loc[idx].tolist()
        row = []
        for i in rowlistd:
            if i:
                row.append(i)
            if not i:
                row.append(' ')
        row_list.append(''.join(row)+'\n')
        print(''.join(row))
    return row_list

def check_bingan( pkl_path, img_shape, results):
    print('#=' * 120)
    print('#=' * 120)
    total_text = []
    for one in results[:20]:

        str1 = one[1][0] + '\n'
        total_text.append(str1)

    if ('病案首页' in ''.join(total_text)) or ('住院病案' in ''.join(total_text)):
        return bingan_judge_info(pkl_path, img_shape, results)

def get_bingan_info(data, img_path, pkl_path, idx):
    img_shape = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED).shape
    bingan_dict = bingan_judge_info(pkl_path, img_shape)
    # t = ['']
    # d = {'图名': t, '内容': t, '目录名': t, 'text': t, '姓名': t, '性别': t, '年龄': t, '住院号': t, '类别': t
    #     , '入院日期': t, '入院相关日期': t, '科室': t, '生效日期': t, '主诉': t, '现病史': t, '既往史': t, '个人史': t
    #     , '家族史': t, '生育及月经史': t, '其他': t, '既往史结果': t, '健康告知疾病': t, '疾病时间': t, '手术': t, '手术时间': t
    #     , '患病日期': t, '手术日期': t, '诊断结果': t, '结果': t, '基本信息': t, '图片位置': t, '最终诊断结果': t, '参考': t
    #     , '诊断': t, '症状时间': t, '发生日期': t, 'diagnosis_prove': t, '出院日期': t}
    if (img_path[-4:] == '.png') or (img_path[-4:] == '.jpg'):
        text = data.loc[idx, '内容']
        for key, value in bingan_dict.items():
            if value:
                print('bingan_dict', key, value)
                data.loc[idx, key] = bingan_dict[key][0]
        if re.findall('主要诊断.*\n',text):
            main_diag = re.findall('主要诊断.*\n', text)[0].split('  ')[0].replace('主要诊断','').replace(':','').replace('：','')
            data.loc[idx, '诊断结果'] = main_diag
        print('bingan info complete !!!')
        return data

def merge_tabels(better, meragename):
    # print('run')
    file_list = []
    file_list = nextlevel(better, file_list)

    t = ['']
    colnames = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
    d = {col:t for col in colnames}
    df_data = pd.DataFrame(d)
    c = 0
    for file in file_list:
        if (file[-4:] == '.xls'):
            df2 = pd.read_excel(file)

            dfcols = pd.DataFrame({col:['','%s'%col] for col in df2.columns.tolist()})
            df2 = pd.concat([dfcols, df2], axis=0, ignore_index=True)
            collen = len(df2.columns.tolist())
            df2.columns = colnames[:collen]
            df_data = pd.concat([df_data, df2], axis=0, ignore_index=True)
            c += 1
            print('已合并:', c)
    df_data = df_data.drop(['0'], axis=1)
    df_data.to_excel(meragename, index=False)




if __name__ == '__main__':
    base = r'C:\Users\86182\Desktop\tt\test_acc\test5'
    better = r'C:\Users\86182\Desktop\tt\test_acc\test55'
    data = None
    img2pkl(base, better)
    # pkl2txt(better)
    # better = r'D:\image\test_12\new12\test220'
    # merge_tabels(better, meragename)