from PIL import Image

import numpy as np
import cv2

import pytesseract
import argparse
import os

# ocr mode path
tessdata_dir_config = '--tessdata-dir "D:/Program Files/Tesseract-OCR/tessdata"'

# 二值化：全局阈值
def threshold_demo(image):
    # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv2.threshold(
        gray, 180, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    print("threshold value %s" % ret)
    return binary

# 二值化：OTSU
# 效果不理想，会将很多原本不属于这一片区域的内容给恢复为杂色，因此不使用
def otsu(gray):
    pixel_number = gray.shape[0] * gray.shape[1]
    mean_weigth = 1.0/pixel_number
    his, bins = np.histogram(gray, np.array(range(0, 256)))
    final_thresh = -1
    final_value = -1
    # This goes from 1 to 254 uint8 range (Pretty sure wont be those values)
    for t in bins[1:-1]:
        Wb = np.sum(his[:t]) * mean_weigth
        Wf = np.sum(his[t:]) * mean_weigth

        mub = np.mean(his[:t])
        muf = np.mean(his[t:])

        value = Wb * Wf * (mub - muf) ** 2

        #print("Wb", Wb, "Wf", Wf)
        #print("t", t, "value", value)

        if value > final_value:
            final_thresh = t
            final_value = value
    final_img = gray.copy()
    # print(final_thresh)
    final_img[gray > final_thresh] = 255
    final_img[gray < final_thresh] = 0
    return final_img

# 锐化图像:拉普拉斯算法
def sharpe(gray):
    lap_5 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    lap_9 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    dst = cv2.filter2D(gray, cv2.CV_8U, lap_9)
    return dst

# 形态学处理（膨胀腐蚀）--旧
def dilate(gray):
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(gray, kernel)
    dst = cv2.dilate(erosion, kernel)
    return dst

# 形态学处理（膨胀腐蚀）--新
def new_dilate(gray):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    eroded = cv2.erode(gray, kernel)
    return eroded


#### 处理传递参数 ####
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done. 1.thresh 2.blur Default is thresh")
args = vars(ap.parse_args())

#### 图片基本处理 ####
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 把输入图像灰度化

if args["preprocess"] == "thresh":
    ray = cv2.threshold(gray, 0, 255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# 锐化处理
after_img = sharpe(gray)

'''
color = (0, 255, 0)
contours, hierarchy = cv2.findContours(after_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)
'''

# apply OCR to it
filename = "{}.png".format(os.getpid())

cv2.imwrite(filename, after_img)

content = pytesseract.image_to_string(
    Image.open(filename), lang='chi_sim+eng')

print(content)
