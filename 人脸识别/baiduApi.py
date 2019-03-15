# # coding=utf-8

import sys
import ssl
from urllib import request, parse


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    # 获取token
    # 请前往"http://ai.baidu.com/tech/face/detect"注册并获取
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
def imgdata(filepath):
    import base64
    f = open(r'%s' % filepath, 'rb')
    pic = base64.b64encode(f.read())
    f.close()
    # max_face_num为最多处理人脸的数目，
    # 默认值为1，仅检测图片中面积最大的那个人脸；
    # 最大值10，检测图片中面积最大的几张人脸。
    params = {"image": str(pic, 'utf-8'),
              "image_type": "BASE64", "max_face_num": 10}
    return params


def faceDetec(filepath):
    # 调用百度人脸检测API
    token = get_token()
    print("开始使用百度人脸识别API")
    # 人脸识别API
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token
    params = imgdata(filepath)
    data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    response = request.urlopen(req)
    content = response.read()
    content = bytes.decode(content)
    # 百度返回的检测内容,我们只是用来对比故只去人脸数,若需其他的参数,可以自行查看官方文档
    content = eval(content)
    # 百度返回的人脸数
    face_num = content['result']['face_num']
    # 人脸坐标集合
    face_euler_angle_arr = []
    if face_num != 0:
        for i in range(face_num):
            # face_list是百度返回的人脸数据集合,我们根据索引获取即可
            angle = content['result']['face_list'][i]['angle']
            baidu_euler_angle_str = 'roll:{}, pitch:{}, yaw:{}'.format(
                angle['roll'], angle['pitch'], angle['yaw'])
            face_euler_angle_arr.append(baidu_euler_angle_str)
    else:
        face_euler_angle_arr.append("百度人脸识别API没有检测到人脸")
    return face_num, face_euler_angle_arr


if __name__ == '__main__':
    print("本类只做函数调用使用,无需直接运行")
