# ocr-pytesseract

ocr-pytesseract是一个基于opencv以及pytesseract的简单ocr文字识别模块，并且引用flask框架做服务，服务器部署可以在windows和linux端运行，皆已测试完毕，在运行程序前，你需要先安装opencv和pytesseract，如果你需要完全相同的环境（Python3.7），你可以使用pip install -r requirements.txt进行安装

##### 运行方式：

### Windows：

python app.py

### Linux：

bash SERVER.sh



### 文件格式说明。

文件夹：

​	doc					说明文档，前期录入的，可删

​	ImageTest		测试图片文件夹，用来测试算法的图片，可删

​	LocalSave		本地保存图片文件夹，用来从网络中获取访问的图片保存地点

​	RuningFolder	运行文件夹，生成所需要的各类图片

.py文件

​	核心：

​		app.py					网络服务，提供POST和GET接口，采用flask框架

​		appRunOCR.py	运行OCR文件，提供文件检验和报错处理功能

​		baseOCR.py			基础OCR算法文件，采用pytesseract进行ocr处理

​	自主运行算法程序调用:

​		RunOCR.py			通过argparse进行命令行多行读取处理，直接控制台调用baseOCR.py

​	其他：

​		getLocalIP.py		获取本机IP地址

​		testcli.py				测试网络上传文件模块	



### 接口说明

使用POST发送一张图片给http://127.0.0.1:5000/v1/ocr，可以参考testcli.py的发送方式

使用GET获取图片http://127.0.0.1:5000/download/可以直接下载json，http://127.0.0.1:5000/api/可以网页的方式展示json

返回的格式代码为：

​        return jsonify({

​            \# "DOWNLOAD_Image": [download_output_Auto, download_output_BlackWhite, download_output_Grayscale],

​            "API_Image": [web_output_Auto, web_output_BlackWhite, web_output_Grayscale],

​            "OUT_text_string": content,

​        })



### 其他说明：

如果需要公网访问，请修改app.py的第79行

base_server_url = "http://127.0.0.1"  # 本地测试用地址

修改为你的公网访问的IP，端口则可以修改app.py的第152行

port=5000

