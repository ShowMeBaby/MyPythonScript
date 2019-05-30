# -*- coding:utf-8 -*-
from bottle import template, Bottle
root = Bottle()


@root.route('/')
def index():
    return "优雅的主页"


@root.route('/hello/<name>')
def hello(name):
    # return "你好世界"
    return template('<b>Hello {{name}}</b>!', name="Alex")


root.run(host='localhost', port=8080)
