from PIL import Image

import numpy as np
import cv2

import pytesseract
import argparse
import os

# ocr mode path
tessdata_dir_config = '--tessdata-dir "D:/Program Files/Tesseract-OCR/tessdata"'


# 锐化图像:拉普拉斯算法
def sharpe(gray):
    lap_5 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    lap_9 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    dst = cv2.filter2D(gray, cv2.CV_8U, lap_9)
    return dst

# 形态学处理（膨胀腐蚀）--旧
def dilate(gray):
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(gray, kernel)
    dst = cv2.dilate(gray, kernel)
    return erosion

#形态学处理（膨胀腐蚀）
def new_dilate(gray):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    eroded = cv2.erode(gray, kernel)
    return eroded


#### 图片基本处理 ####
image = cv2.imread("final.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 把输入图像灰度化

gray = cv2.medianBlur(gray, 3)
ray = cv2.threshold(gray, 0, 255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


#after_img = sharpe(gray)
after_img = new_dilate(gray)




# mask_bin 是黑白掩膜
ret, mask_bin = cv2.threshold(after_img, 200, 255, cv2.THRESH_BINARY)
# mask_inv 是反色黑白掩膜
mask_inv = cv2.bitwise_not(mask_bin)

# 黑白掩膜 和 大图切割区域 取和
ans_image = cv2.bitwise_and(image, image, mask=mask_bin)

cv2.imshow("shown me your name:",ans_image)
cv2.waitKey(0)
cv2.destroyAllWindows()




color = (0, 255, 0)
contours, hierarchy = cv2.findContours(after_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)

# apply OCR to it
filename = "{}.png".format(os.getpid())

cv2.imwrite(filename, after_img)

content = pytesseract.image_to_string(
    Image.open(filename), lang='chi_sim+eng')

print(content)

cv2.imshow("shown me your name:",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
