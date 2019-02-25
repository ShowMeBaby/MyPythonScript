#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *                       # 导入 tkinter 库
from PIL import Image, ImageTk              # 图片处理模块
import tkinter.filedialog                   # 用以获取图片路径
import tkinter.messagebox as msg            # 用来进行'关于'弹窗
import funUtil                              # 人脸识别函数模块
import math                                 # 数学模块
import urllib.request                       # 安全验证相关正式交付后应删除
import json                                 # 安全验证相关正式交付后应删除
import os                                   # 安全验证相关正式交付后应删除

try:
    isRun = json.loads(urllib.request.urlopen("http://21120903.xyz/pyhondlib_is_start.php").read().decode('utf-8')).get("javaNo.1")
    if isRun != True:
        print("验证失败,请联系作者")
        os._exit(0)
except :
    print("验证失败,请联系作者")
    os._exit(0)

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # 设置窗口大小及居中居中
        self.center_window(800, 600)
        self.init_window()

    def init_window(self):
        # 设置窗口标题
        self.master.title("人脸姿态测试")
        # 设置窗口图标
        try:
            self.master.iconbitmap('img/favicon.ico')
        except:
            pass
        # 禁止改变窗口大小
        # self.master.resizable(0, 0)
        self.pack(fill=BOTH, expand=1)
        # 显示图片控件
        self.master.imgLabel = Label(self.master, text="暂未选择图片", font=(
            "", 16), width=800, height=23, bg="#eeeeee")
        self.master.imgLabel.pack(fill=X, side='top')
        # 选择图片按钮
        self.master.button = Button(
            self.master, text="选择图片", command=self.inputFile, height=2, bg="#e3f2fd")
        self.master.button.pack(fill=X, side='bottom')
        # 提示框控件
        self.master.tipsLabel = Label(self.master, text="请点击下方按钮以开始检测", font=(
            "", 16), width=800, height=2, wraplength=800, bg="#fafafa")
        self.master.tipsLabel.pack(fill=X, side='bottom')
        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # 创建设置'关于'菜单，下面有'关于'和'退出'两个子菜单
        file = Menu(menu, tearoff=0)
        file.add_command(label='关于', command=self.about)
        file.add_separator()
        file.add_command(label='退出', command=self.client_exit)
        menu.add_cascade(label='关于', menu=file)

    def about(self):
        msg.showinfo(
            title="提示", message="1.点击'选择图片'开始计算\n2.基本可检测出图中所有人脸并标定\n3.但不建议单张图片中出现多张人脸,否则在图上进行标记会将图片画乱")

    def showImg(self, image):
        # 根据窗口大小自适应
        width = self.winfo_width()
        height = self.winfo_height()
        # 兼容性调整,在软件启动后直接执行第一次showImg时,图片大小不会跟随最大化,目前原因未知,暂时手动调整回正确数值,以进行修正
        if height == 1:
            height = 485
        elif height == 423:
            height = 912
        # 展示图片
        image = self.resize(width, height, image)
        render = ImageTk.PhotoImage(image)
        self.master.imgLabel.config(image=render, width=width, height=height)
        self.master.imgLabel.image = render
        self.master.imgLabel.place(x=0, y=0)

    def showTxt(self, txt):
        width = self.master.winfo_width()
        # 在提示框中显示提示文字
        if len(txt) > (width/27):
            self.master.tipsLabel.config(
                text=txt, wraplength=width, height=math.floor(len(txt)/(width/27)))
        else:
            self.master.tipsLabel.config(text=txt, wraplength=width, height=2)

    def resize(self, w_box, h_box, pil_image):
        # 参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size  # 获取图像的原始大小
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def inputFile(self):
        # 选择图片文件,选择多个文件的函数为askopenfilenames(),如有需要可直接更改
        self.showTxt("正在检测")
        filenames = tkinter.filedialog.askopenfilename()
        if len(filenames) != 0:
            img, lenFaces, face_euler_angle_arr = funUtil.get_face(filenames)
            print("\n结果集为:\n {}".format(face_euler_angle_arr))
            self.showTxt("人脸数:"+str(lenFaces)+"     " +
                         str(face_euler_angle_arr))
            self.showImg(img)
        else:
            self.showTxt("没有选中图片,请重新选择")

    def center_window(self, w, h):
        # 设置窗口屏幕居中
        # 获取屏幕 宽、高
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def client_exit(self):
        # 退出
        exit()


if __name__ == '__main__':
    print("启动成功")
    root = Tk()
    app = Window(root)
    root.mainloop()
    # GUI启动成功,后面的代码会在GUI结束运行后执行
    print("退出成功")
