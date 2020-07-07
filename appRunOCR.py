# ############coding=utf-8

import os
from PIL import Image

import baseOCR as baseOCR

# 直接后端shell运行使用RunOCR.py
# 这个模块是由app模块调用的


class appRunOCR():
    def __init__(self,imagePath, count):
        self.imagePath = imagePath
        self.count = count

    def __del__(self):
        pass

    # 尾椎，图片存在性，图片色彩模式判断验证
    # 返回值：
    # 0-验证成功，正确，自动将色彩模式转换成了RGB
    # 1-输入图片格式不对，目前仅支持png,jpg,jpeg等格式
    # 2-图片尾椎输入正确，但是图片不存在
    def checkImage(self, imagePath):
        # 尾缀判别
        path, tail = imagePath.split('.')
        checkTail = ["png", "jpg", "jpeg"]
        # 色彩模式：1，二值（0|1），L：灰度图(0~255),'I',"RGB","RGBA"(ALPHA通道)，"CMYK"，--->RGB
        mode_list = ['1', 'L', 'I', 'F', 'P', 'RGB', 'RGBA', 'CMYK', 'YCbCr']
        if tail not in checkTail:
            # print("error:输入图片格式不对，目前仅支持png,jpg,jpeg等格式")
            return 1
        else:
            # 尾椎正确
            # 文件存在性验证
            if os.path.exists(imagePath):
                # print("文件存在")
                check = Image.open(imagePath)
                imgMode = check.mode
                # 图片格式验证
                if imgMode is not 'RGB':
                    final = check.convert('RGB')
                    final.save(imagePath)
                return 0
            else:
                return 2

    #### 启动运行 ####
    def start(self):
        imagePath = self.imagePath
        count = self.count

        checkCode = self.checkImage(imagePath)

        retrunString = "Nothing get."

        if checkCode == 0:
            retrunString = baseOCR.ocr(imagePath, "thresh", count).start()
        elif checkCode == 1:
            retrunString = "error:输入图片格式不对，目前仅支持png,jpg,jpeg等格式\nCode:01"
        elif checkCode == 2:
            retrunString = "error:图片文件不存在\nCode:02"
        
        return retrunString
