# # coding=utf-8

import sys
import ssl
from urllib import request, parse

# client_id 为官网获取的AK， client_secret 为官网获取的SK
# 获取token


def get_token():
    client_id = "rvgADQ1rL191isalHyiyU5UA"
    client_secret = "9pgLKpDVdAoZeFie7OQvT3Df74ArKmBq"
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        client_id, client_secret)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    content = response.read()
    content = bytes.decode(content)
    # 转化为字典
    content = eval(content[:-1])
    return content['access_token']


# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(filepath):
    import base64
    f = open(r'%s' % filepath, 'rb')
    pic = base64.b64encode(f.read())
    f.close()
    params = {"image": str(pic, 'utf-8'), "image_type": "BASE64"}
    return params


def faceDetec(filepath):
    # 调用百度人脸检测API
    token = get_token()
    # 人脸识别API
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token
    params = imgdata(filepath)
    data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    content = response.read()
    content = bytes.decode(content)
    content = eval(content)
    return content


if __name__ == '__main__':
    filepath = 'C:\\Users\\liule\\Desktop\\Pytho练手脚本\\40.jpg'
    res = faceDetec(filepath)
    # res['result']['face_list']
    print(res)


res = {'error_code': 0,
       'error_msg': 'SUCCESS',
       'log_id': 304592814459130621,
       'timestamp': 1551445913,
       'cached': 0,
       'result': {
           'face_num': 1,
           'face_list': [{
               'face_token': 'f27146ec411681bacc5dea0df6523134',
               'location': {
                   'left': 84.44,
                   'top': 122.54,
                   'width': 159,
                   'height': 140,
                   'rotation': -9},
               'face_probability': 1,
               'angle': {
                   'yaw': -35.21,
                   'pitch': 4.92,
                   'roll': -10.17
               }
           }]
       }
       }
