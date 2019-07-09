# -*- coding:utf-8 -*-
from bottle import template, Bottle, error
from threading import Timer
import datetime

root = Bottle()


def timerTask():
    print('TimeNow:%s' %
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(2, timerTask)
    t.start()
    return '定时任务已启动'


@root.error(404)
def error404(error):
    return '<h1>出现了一个不知名的错误!</h1>'


@root.route('/')
def index():
    return "优雅的主页"


@root.route('/<name>')
def hello(name):
    return template('<h1>Hello {{name}}!</h1>', name=name)


if __name__ == '__main__':
    root.run(host='localhost', port=8080, reloader=True)
