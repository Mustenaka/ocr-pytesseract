import requests
import json

# API地址
#url = "http://127.0.0.1:5000/v1/ocr"
url = "http://47.96.128.130:5000/v1/ocr"
# 图片地址
file_path='ImageTest/english.jpg'
# 图片名
file_name=file_path.split('/')[-1]
# 二进制打开图片
file=open(file_path,'rb')
# 拼接参数 ---如果图片是jpg格式结尾使用这个，jpeg是'image/jpeg'，同理png
files = {'file':(file_name,file,'image/jpg')}
# 发送post请求到服务器端
data = requests.post(url,files = files)
#json_data = json.loads(data.text)
print(data.text)
#print(json_data)
