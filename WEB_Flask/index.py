# coding=utf-8
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 禁止ASCII以解决中文输出问题
app.config['JSON_AS_ASCII'] = False
# 为app指定数据库的配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dmblog_f:darkmario@hzg25euu.2316.dnstoo.com:5507/dmblog?charset=utf8'
# 指定当视图执行完毕后,自动提交数据库操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
# 创建 SQLAlchemy的数据库实例
db = SQLAlchemy(app)


class User(db.Model):  # User类
    __tablename__ = "User"
    USERNAME = db.Column(db.String(32), primary_key=True)
    PASSWORD = db.Column(db.String(32))
    CREATED_TIME = db.Column(db.DateTime(64))
    LAST_LOGIN_TIME = db.Column(db.DateTime(64))

    def __repr__(self):
        return "{{'用户名':'{}','密码':'{}','创建时间':'{}','最后登录时间':'{}'}}".format(self.USERNAME, self.PASSWORD, self.CREATED_TIME, self.LAST_LOGIN_TIME)


class UserDao():  # Dao层
    def create_note(user):
        db.session.add(user)
        db.session.commit()
        return new_note

    def update_note(user):
        user = User.query.get(user.USERNAME)
        db.session.commit()
        return user

    def delete_note(user):
        user = User.query.get(user.USERNAME)
        db.session.delete(user)
        db.session.commit()
        return True

    def list_all():
        return User.query.all()

    def get_note(username):
        return User.query.get(username)


# 拦截预期错误
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def server_error(error):
    response = dict(status=0, message="错误代码:{}".format(error.code))
    return jsonify(response)


# 拦截意料之外的报错
@app.errorhandler(Exception)
def exception(error):
    response = dict(status=0, message="意料之外的错误")
    return jsonify(response)


# 拦截器,在所有路由前执行
@app.before_request
def before_request():
    print("请求地址：" + str(request.path))
    print("请求方法：" + str(request.method))
    print("---请求headers--start--")
    print(str(request.headers).rstrip())
    print("---请求headers--end----")
    print("GET参数：" + str(request.args))
    print("POST参数：" + str(request.form))


# 在所有路由后执行,此时response已形成但还未返回，如果请求没有异常。
@app.after_request
def after_request(response):
    print("请求执行完成")
    # # 请不要在此处进行如下操作,否则你会发现所有response都被识别为JSON这显然不是我们要的,
    # # 仅以此展示response操作
    # response.headers["Content-Type"] = "application/json"
    return response


# 主页
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='优雅的主页'), 200, {'Content-Type': 'text/html'}


# 测试查询数据库
@app.route('/user', methods=['GET', 'POST'])
def user():
    # User.query.filter(User.USERNAME == 'DarkMario').all()
    # 过滤器函数
    # 作用:专门对数据进行筛选,返回部分行数据
    # 1.filter(id>1,name=='abc')    按指定条件进行过滤(单表,多表,定值,不定值)
    # 2.filter_by(id==1)            按等值条件进行过滤
    # 3.limit(x).offset(y)          按限制行数量获取结果
    # 4.order_by("age desc,id asc") 按指定列进行排序
    # 5.group_by()                  按指定条件进行分组
    # 查询执行函数
    # 1.all()                       以列表形式返回查询的所有结果
    # 2.first()                     返回查询的第一个结果,如果没有结果,则返回 None
    # 3.first_or_404()              返回查询的第一个结果,如果没有结果,则终止请求,返回 404 错误响应
    # 4.get()                       返回指定主键对应的行,如果没有对应的行,则返回 None
    # 5.get_or_404()                返回指定主键对应的行,如果没找到指定的主键,则终止请求,返回 404 错误响应
    # 6.count()                     返回查询结果的数量
    # 7.paginate()返回一个 Paginate  对象,它包含指定范围内的结果
    # 以下为测试,可随意删除
    # user = User()
    # user.USERNAME = '用户名1'
    # user.PASSWORD = '密码123'
    # db.session.add(user)
    # db.session.delete(user)
    return str(UserDao.list_all())


# 登录接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = ""
    if request.method == 'GET':
        username = request.args.get("username")
        print("GET请求参数:", request.args.get("username"))
    else:
        username = request.form.get("username")
        print("POST请求参数:", request.form.get("username"))
    return render_template('index.html', title='你输出的参数为:{}'.format(username))


# 可以根据参数类型进行重载
@app.route('/login/<int:arg>', methods=['GET', 'POST'])
def login_int(arg):
    return "你发送的int参数为:{}".format(arg)


@app.route('/login/<path:arg>', methods=['GET', 'POST'])
def login_path(arg):
    return "你发送的path参数为:{}".format(arg)


@app.route('/login/<float:arg>', methods=['GET', 'POST'])
def login_float(arg):
    return "你发送的float参数为:{}".format(arg)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')
