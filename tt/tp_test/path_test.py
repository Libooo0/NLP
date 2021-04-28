import cv2
import glob
import os


# # 利用拉普拉斯
# def getImageVar(imgPath):
#
#     image = cv2.imread(imgPath)
#     img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
#     return imageVar
#
# # 主文件夹路径
# root_path = r"C:\Users\86182\Desktop\tp_test\202002\202002"
# count = 0
# for i in os.walk(root_path):
#     for j in i[2]:
#         path = os.path.join(i[0],j)
#         count += 1
#         print("{}\t方差值：{}\t图{}".format(path,getImageVar(path),count))


# 利用拉普拉斯
def getImageVar(imgPath):

    image = cv2.imread(imgPath)
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar

# 主文件夹路径
root_path = r"C:\Users\86182\Desktop\tp_test\202002\202002"
count = 0
for i in os.walk(root_path):
    for j in i[2]:
        path = os.path.join(i[0],j)
        count += 1
        print("{} \t路径：{} ".format(count,path))