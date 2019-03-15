#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont  # 中文处理模块 Pillow
import dlib                                  # 人脸识别模块 Dlib
import numpy as np                           # 数据处理模块 numpy
import cv2                                   # 图像处理模块 OpenCv
import time                                  # 时间模块
import math                                  # 数学模块


def get_image_points_from_landmark_shape(landmark_shape):
    # 从dlib的检测结果抽取姿态估计需要的点坐标
    if landmark_shape.num_parts != 68:
        print("ERROR:landmark_shape.num_parts-{}".format(landmark_shape.num_parts))
        return None
    # 从68点特征点中取出我们需要的部分
    image_points = np.matrix([
        (landmark_shape.part(30).x, landmark_shape.part(30).y),     # 鼻尖
        (landmark_shape.part(8).x,
         landmark_shape.part(8).y),       # 下巴
        (landmark_shape.part(36).x,
         landmark_shape.part(36).y),     # 左眼角
        (landmark_shape.part(45).x,
         landmark_shape.part(45).y),     # 右眼角
        (landmark_shape.part(48).x,
         landmark_shape.part(48).y),     # 左嘴角
        (landmark_shape.part(54).x,
         landmark_shape.part(54).y)      # 右嘴角
    ], dtype="double")
    return image_points


def get_pose_estimation(img_size, image_points):
    # 获取旋转向量和平移向量
    # 3D模型坐标.
    model_points = np.array([
        (0.0, 0.0, 0.0),             # 鼻尖
        (0.0, -330.0, -65.0),        # 下巴
        (-225.0, 170.0, -135.0),     # 左眼角
        (225.0, 170.0, -135.0),      # 右眼角
        (-150.0, -150.0, -125.0),    # 左嘴角
        (150.0, -150.0, -125.0)      # 右嘴角
    ])

    # 图片矩阵
    focal_length = img_size[1]
    center = (img_size[1]/2, img_size[0]/2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    print("图片矩阵:{}".format(camera_matrix))

    dist_coeffs = np.zeros((4, 1))  # 创建一个空坐标组
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
                                                                  image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    print("旋转向量:\n {}".format(rotation_vector))
    print("平移向量:\n {}".format(translation_vector))
    return success, rotation_vector, translation_vector, camera_matrix, dist_coeffs


def get_euler_angle(rotation_vector):
    # 从旋转向量转换为欧拉角
    # 计算旋转角度
    theta = cv2.norm(rotation_vector, cv2.NORM_L2)

    # 转换为四元数
    w = math.cos(theta / 2)
    x = math.sin(theta / 2)*rotation_vector[0][0] / theta
    y = math.sin(theta / 2)*rotation_vector[1][0] / theta
    z = math.sin(theta / 2)*rotation_vector[2][0] / theta
    ysqr = y * y

    # X轴
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + ysqr)
    pitch = math.atan2(t0, t1)

    # Y轴
    t2 = 2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1.0
    if t2 < -1.0:
        t2 = -1.0
    yaw = math.asin(t2)

    # Z轴
    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (ysqr + z * z)
    roll = math.atan2(t3, t4)

    # 转化出的欧拉角单位是弧度，需要除以Pi乘以180得到度的单位值
    # 单位转换：将弧度转换为度
    Y = int((pitch/math.pi)*180)
    if Y > 0:
        Y = Y - 180
    else:
        Y = Y + 180
    X = int((yaw/math.pi)*180)
    Z = int((roll/math.pi)*180)
    return 0, Y, X, Z


def putText_chinese(img, text, point, font_size, color):
    # 向图片输出中文
    # 由于由于putText不支持输出中文,故借助PTL实现中文输出
    # cv2图片转换为PTL图片
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)

    # PIL图片上打印汉字
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    # 字体文件可任意设置系统中已有字体,但请注意字体文件是否支持中文
    font = ImageFont.truetype("msyh.ttc", font_size, encoding="utf-8")
    draw.text(point, text, color, font=font)

    # PIL图片转cv2图片
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return cv2charimg


def get_face(imgpath):
    # 主要函数,只需要调用本函数即可

    # 记录识别时间
    start_time = time.time()

    # Dlib 检测器和预测器
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        './model/shape_predictor_68_face_landmarks.dat')
    # 读取图像文件
    # img_rd = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), -1)
    # 读取图片文件,
    # 如果报错提示:RuntimeError: Unsupported image type,must be 8bit gray or RGB image.
    # 可以注释本函数,启用上方的cv2.imdecode函数
    img_rd = cv2.imread(imgpath)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数
    faces = detector(img_gray, 0)

    # 设置cv2字体
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 人脸坐标集合
    face_euler_angle_arr = []

    # 标记特征点
    if len(faces) != 0:
        # 检测到人脸
        for i in range(len(faces)):
            print("\n\n正在检测第", i+1, "张人脸")
            # 取特征点坐标
            # 获取全部68个特征点,后面的计算主要依赖于6点坐标,故这个获取68点坐标只做吉祥物使用,以便在需要修改重构时有个较完善的起点
            # landmarks = np.matrix([[p.x, p.y] for p in predictor(img_rd, faces[i]).parts()])
            # 只获取必要的坐标点
            landmarks = get_image_points_from_landmark_shape(
                predictor(img_rd, faces[i]))

            # 获取旋转向量和平移向量
            ret, rotation_vector, translation_vector, camera_matrix, dist_coeffs = get_pose_estimation(
                img_rd.shape, landmarks)
            if ret != True:
                print('get_pose_estimation failed')
                continue

            # 从旋转向量转换为欧拉角
            ret, pitch, yaw, roll = get_euler_angle(rotation_vector)
            euler_angle_str = 'roll:{}, pitch:{}, yaw:{}'.format(
                roll, pitch, yaw)
            ## euler_angle_str = '上下翻转角:{},平面内旋转角::{}, 左右翻转角:{}'.format(pitch, yaw, roll)
            face_euler_angle_arr.append(euler_angle_str)
            # cv2.putText()参数:cv2图片,文本内容,打印坐标,字体,字体大小,字体颜色,线宽,线型
            # cv2.putText(img_rd, euler_angle_str, (20, 80),
            #             font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            print("欧拉角:\n {}".format(euler_angle_str))

            # 在图片中构建3维坐标系
            # 以人脸鼻尖为原点画一条面部朝向的线
            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array(
                [(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

            p1 = (int(landmarks[0][0, 0]), int(landmarks[0][0, 1]))
            p2 = (int(nose_end_point2D[0][0][0]),
                  int(nose_end_point2D[0][0][1]))
            cv2.line(img_rd, p1, p2, (255, 0, 0), 2)
            # 标记每张脸的序号
            # img_rd = putText_chinese(img_rd, "第"+str(i+1)+"张脸", (int(landmarks[0][0,0]),int(landmarks[0][0,1])), 20, (255, 0, 0))
            # 遍历所有特征点,并标记出来
            for idx, point in enumerate(landmarks):

                # 点的坐标
                pos = (int(point[0, 0]), int(point[0, 1]))

                # 利用 cv2.circle 给每个特征点画一个圈
                cv2.circle(img_rd, pos, 10, color=(255, 0, 0))

                # 利用 cv2.putText 写数字
                cv2.putText(img_rd, str(idx + 1), pos, font,
                            0.5, (0, 0, 255), 2, cv2.LINE_AA)
        # img_rd = putText_chinese(img_rd, "人脸数: " + str(len(faces)), (20, 40), 20, (255, 0, 0))
    else:
        # 没有检测到人脸
        # img_rd = putText_chinese(img_rd, "没有检测到人脸或人脸显示不完整", (20, 40), 20, (255, 0, 0))
        face_euler_angle_arr.append("没有检测到人脸或人脸显示不完整")
    print("\n检测用时:{} 秒".format(round(time.time() - start_time, 3)))
    # cv2图片通道顺序为BGR,故需要翻转为RGB
    return Image.fromarray(img_rd[..., ::-1]), len(faces), face_euler_angle_arr


if __name__ == '__main__':
    print("本类只做函数调用使用,无需直接运行")
