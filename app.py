import pytesseract
import requests
import json
import os

from flask import Flask, request, jsonify, send_from_directory, make_response
from werkzeug.utils import secure_filename
from io import StringIO, BytesIO

import appRunOCR as appRunOCR
import getLocalIP as getLocalIP

UPLOAD_FOLDER = r'LocalSave/'   # 上传路径
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])   # 允许上传的文件类型
_VERSION = 1  # API version
# COUNT表示标记
# IMAGE_LIST用来模拟队列，队列会删除元素
# 而List设置一个循环，方便查询调用图片生成的记录
COUNT = 1
LIST_SIZE = 1000
IMAGE_LIST = []

app = Flask(__name__)
# 设置编码
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def _get_image():
    # 接收图片
    upload_file = request.files['file']
    print("successful get file")
    # 获取图片名,并放入List
    file_name = upload_file.filename
    IMAGE_LIST.append(file_name)
    # 图片存在则保存
    if upload_file:
        file_paths = os.path.join(UPLOAD_FOLDER, file_name)
        upload_file.save(file_paths)
        return file_paths, file_name
    else:
        return "can't not get image.", "error"


def check_folder_path(path):
    # 判断文件夹存在性，否则就自动创建
    if os.path.exists(path):
        os.makedirs(path)
    else:
        pass


def allowed_file(filename):
    # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/v{}/ocr'.format(_VERSION), methods=['POST'])
def ocr():
    global COUNT
    cnt = str(COUNT)
    print("Get a post for OCR server.")
    try:
        # get image
        local_img_path, file_name = _get_image()
        print(local_img_path, file_name)
        # check image
        if not allowed_file(file_name):
            os.remove(file_name)
            return jsonify({
                "error": "Only support .jpeg .jpg .png style. Pealse sent right pic"
            })

        # 获取ocr识别文字
        content = appRunOCR.appRunOCR(local_img_path, cnt).start()

        #如果你需要部署服务器，可以把公网IP修改为本地址
        base_server_url = "http://127.0.0.1"  # 本地测试用地址

        _port = 5000
        server_url = base_server_url + ":" + str(_port)

        local_files = "RuningFolder/" + cnt + '/'

        '''
        # 输出文字
        local_text = local_files+"/out.txt"
        with open(local_text, 'r') as f:
            content = f.read()
        print("The contecnt is: ", content)
        '''

        # http://127.0.0.1:5000/download/
        download_url = server_url + "/download/" + cnt+'/'
        # 三个图片 -- 下载API
        download_output_Auto = download_url+"Auto.png"
        download_output_BlackWhite = download_url+"BlackWhite.png"
        download_output_Grayscale = download_url+"Grayscale.png"

        #http://127.0.0.1:5000/api/
        web_url = server_url + "/api/" + cnt+'/'
        # 三个图片 -- 网页展示API
        web_output_Auto = web_url+"Auto.png"
        web_output_BlackWhite = web_url+"BlackWhite.png"
        web_output_Grayscale = web_url+"Grayscale.png"

        COUNT = COUNT+1  # 计数标记+1
        if COUNT == LIST_SIZE:  # 在本地保留1000个处理记录,本程序必须保持常开
            COUNT = 1

        return jsonify({
            # "DOWNLOAD_Image": [download_output_Auto, download_output_BlackWhite, download_output_Grayscale],
            "API_Image": [web_output_Auto, web_output_BlackWhite, web_output_Grayscale],
            "OUT_text_string": content,
        })

    except:
        return jsonify(
            {"error": "Did you mean to send:{'image_url':'something_image_url'}"}
        )

# http://47.96.128.130:5000/download/1/Auto.png
@app.route('/download/<string:cnt>/<string:filename>', methods=['GET'])
def download(cnt, filename):
    if request.method == "GET":
        root_path = os.path.join(app.root_path, 'RuningFolder')
        base_path = root_path + "/"+cnt+"/"
        if os.path.isfile(os.path.join(base_path, filename)):
            print(os.path.join(base_path, filename))
            return send_from_directory(base_path, filename, as_attachment=True)
        pass

# http://47.96.128.130:5000/api/1/Auto.png
# RuningFolder\1\Auto.png
@app.route('/api/<string:cnt>/<string:filename>', methods=['GET'])
def display_img(cnt, filename):
    base_path = "RuningFolder/"+cnt+"/"
    imgfile_path = base_path + filename
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(imgfile_path, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)


'''
思路：
先完成了基本的核心算法：图像的识别tesseract，直接看效果，预处理，排除干扰和噪声（预处理-opencv）。
运行算法，规范：限制不正常的内容传入。（appRunOCR.py）
服务器，传输内容
'''