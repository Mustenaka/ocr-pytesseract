文件格式说明。

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