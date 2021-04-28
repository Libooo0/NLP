from paddleocr import PaddleOCR, draw_ocr
import cv2
import os


def init():

    # img_path = r"C:\Users\86182\Desktop\tp_test\202002\202002\00b6a7dc890445bba59cfc8fb60a3c90\11edd47a1c47467ab27a2379e9562e46_24.png"
    img_path = r"C:\Users\86182\Desktop\tt\test_acc\test3\c (22).jpg"

    # ocr图像文本识别
    ocr = PaddleOCR(use_pdserving=False, use_angle_cls=False, det=True, cls=True, use_gpu=False, lang="ch",
                    det_max_side_len=1500, det_db_thresh=0.2, det_db_box_thresh=0.3,
                    det_db_unclip_ratio=2.0,
                    gpu_mem=4000, rec_batch_num=10, cls_batch_num=10)
    result = ocr.ocr(img_path, det=True, rec=True, cls=False)

    # 打印ocr结果
    list = []
    for line in result:
        print(line)
        list.append(line[1][0])
    text = ''.join(list)
    print(text)

    # 计算平均置信度
    count = 0
    sum = 0
    for line in result:
        l = line[1][1]
        sum += l
        count += 1
    if count != 0:
        zx_value = sum / count
        print("平均置信度：",zx_value)

        # 图片清晰度的判定
        # 图片清晰度检测,拉普拉斯边缘检测，返回方差值，越大越清晰
        image = cv2.imread(img_path)
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
        print("拉普拉斯方差值：",imageVar)

        if imageVar <= 10:
            print('图片模糊')

        elif 10 < imageVar < 175:
            if count != 0:
                if zx_value > 0.8:
                    print('清晰')
                else:
                    print('图片模糊')
            else:
                pass

        else:
            print('清晰')
    else:
        pass


if __name__ == "__main__":
    init()
