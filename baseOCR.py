# #############coding=utf-8

from PIL import Image

# 矩阵处理模块，线性代数的内容
import numpy as np
import cv2

import pytesseract
import os


class ocr():

    # 图片地址，处理风格，ID
    def __init__(self, imagePath, preprocess, pid):
        print(os.getpid(),os.getppid())
        # ocr mode path
        # 如果你找不到tessdata-OCR的tessdata地址，就使用这个强制指定
        self.tessdata_dir_config = '--tessdata-dir "D:/Program Files/Tesseract-OCR/tessdata"'

        # 变量传递:图片地址，处理模式,ID号
        self.imagePath = imagePath
        self.preprocess = preprocess
        self.pid = pid
        # auto
        # Grayscale
        # Black and white
        self.foldname = "RuningFolder/"+str(pid)+"/"
        # 创建ocr使用文件夹
        if not os.path.exists(self.foldname):
            os.makedirs(self.foldname)
        # 固定三类返回图片的名字+一个产生文字的位置
        self.nameAuto = self.foldname+"Auto.png"
        self.nameGrayscale = self.foldname+"Grayscale.png"
        self.nameBlackWhite = self.foldname+"BlackWhite.png"
        self.textPath = self.foldname+"out.txt"

    def __del__(self):
        print("ocr处理完成-分配ID号为：{}".format(self.pid))

    # 二值化：全局阈值
    def threshold_demo(self, image):
        # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
        ret, binary = cv2.threshold(
            gray, 190, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
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
    def sharpe(self, gray):
        lap_5 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        # 用下面这个卷积核，5级的不够，11级的又太高
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

    def start(self):
        imagePath = self.imagePath
        preprocess = self.preprocess
        textPath = self.textPath

        #"RGB" ---> "L"
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 把输入图像灰度化


        # 产生黑白图片
        ret, BlackWhite = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # 根据preprocess处理模式分别进行处理，默认为 全局+OTSU 【混合模式】。
        # 统统都是 thresh 
        if preprocess == "thresh":
            filt = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        elif preprocess == "blur":
            filt = cv2.medianBlur(gray, 3)

        # 拉普拉斯-锐化
        shp = self.sharpe(filt)

        # 生成图片--自动处理（用于读出文字）
        cv2.imwrite(self.nameAuto, shp)
        # 生成图片--灰度图
        cv2.imwrite(self.nameGrayscale, gray)
        # 生成图片--黑白图处理（用于读出文字）
        cv2.imwrite(self.nameBlackWhite, BlackWhite)

        # 使用pytesseract调用tessdata进行ocr识别
        # 这属于简单的对比识别，就是对比文字和词库中的字是否相似，仅能够处理默认字体
        content = pytesseract.image_to_string(
            Image.open(self.nameAuto), lang='chi_sim+eng')

        #with open(textPath, "w") as f:
        #    f.write(content)

        return content

        print("ocr Done.")

#ocr("chinese.png", "thresh", "OCRoutput.txt").start()
