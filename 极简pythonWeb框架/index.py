# -*- coding:utf-8 -*-
from bottle import template, Bottle, error
root = Bottle()


@root.error(404)
def error404(error):
    return '<h1>出现了一个不知名的错误!</h1>'


@root.route('/')
def index():
    return "优雅的主页"


@root.route('/<name>')
def hello(name):
    return template('<h1>Hello {{name}}!</h1>', name=name)


root.run(host='localhost', port=8080)
