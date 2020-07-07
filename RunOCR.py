# ############coding=utf-8

import os
import argparse
from PIL import Image

import baseOCR as baseOCR

# 尾椎，图片存在性，图片色彩模式判断验证
# 返回值：
# 0-验证成功，正确，自动将色彩模式转换成了RGB
# 1-输入图片格式不对，目前仅支持png,jpg,jpeg等格式
# 2-图片尾椎输入正确，但是图片不存在


def checkImage(imagePath):
    # 尾缀判别
    path, tail = imagePath.split('.')
    checkTail = ["png", "jpg", "jpeg"]
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


#### 处理传递参数 ####

print("The pid is:",os.getpid(),"\nThe ppid is:",os.getppid())

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")

ap.add_argument("-r", "--runningid", required=True, type=int,
                help="Specify the queue number of the generated content,default is 1")

ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done. 1.thresh 2.blur Default is thresh")

args = vars(ap.parse_args())

checkCode = checkImage(args["image"])

if checkCode == 0:
    baseOCR.ocr(args["image"], args["preprocess"], args["runningid"]).start()
elif checkCode == 1:
    print("error:输入图片格式不对，目前仅支持png,jpg,jpeg等格式")
elif checkCode == 2:
    print("error:图片文件不存在")
