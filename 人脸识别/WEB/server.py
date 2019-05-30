# coding=utf-8
import funUtil                              # 人脸识别函数模块
import baiduApi                             # 百度API模块
import os
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template


app = Flask(__name__)
# 禁止ASCII以解决中文输出问题
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def server_error(error):
    # 拦截预期错误
    response = dict(status=0, message="错误代码:{}".format(error.code))
    return jsonify(response)


@app.errorhandler(Exception)
def exception(error):
    # 拦截意料之外的报错
    print(error)
    response = dict(status=0, message="意料之外的错误")
    return jsonify(response)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 返回主页
    return render_template('index.html'), 200, {'Content-Type': 'text/html'}


@app.route('/submits', methods=['POST'])
def submit():
    # 识别接口
    basedir = os.path.abspath(os.path.dirname(__file__))
    imgFile = request.files.get("file")
    # 缓存图片
    cachePath = basedir+"/static/cache/"+imgFile.filename
    imgFile.save(cachePath)
    # 本机人脸识别结果
    img, lenFaces, face_euler_angle_arr, face_euler_angle_obj_arr = funUtil.get_face(
        cachePath)
    # 检测结果缓存图片
    resultCachePath = basedir+"/static/cache/result_"+imgFile.filename
    img.save(resultCachePath)
    # 百度人脸识别结果
    baidu_lenFaces, baidu_face_euler_angle_arr, baidu_face_euler_angle_obj_arr = baiduApi.faceDetec(
        cachePath)

    result = {
        'img_url': "/static/cache/result_"+imgFile.filename,
        'baidu': {
            'face': baidu_lenFaces,
            'list': baidu_face_euler_angle_obj_arr,
        },
        'my': {
            'face': lenFaces,
            'list': face_euler_angle_obj_arr
        }
    }
    return jsonify(result)


if __name__ == '__main__':
    # 启动成功后通过浏览器访问127.0.0.1或localhost即可访问页面
    app.run(host='127.0.0.1', port='80')
