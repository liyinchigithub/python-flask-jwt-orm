#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# 引入了Flask类
from crypt import methods
from encodings import utf_8
from importlib.resources import path
from flask import Flask, url_for, request, render_template, redirect, flash, session, make_response,Blueprint,jsonify
from flask_wtf.file import FileField, FileRequired, FileAllowed  # 文件上传
from flask import send_from_directory  # 发送静态文件
from flasgger import Swagger # flask swagger
from flasgger.utils import swag_from # flask swagger
from flask_cors import *  # 跨域访问
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter # 正则表达式
from flask_restplus import Api, Resource, fields, reqparse

import os
import uuid  # 生成随机字符串
import json
import config
from api.login import * # 定义路由-登录 [蓝图]模块化
from api.upload import * # 定义路由-上传文件
from api.logout import * # 定义路由-退出登录
from api.register import * # 定义路由-注册
from api.downloadFile import * # 定义路由-注册
from api.jwt_token import *  # 引入封装的jwt_token

# from common.token import * # token生成和校验
# 实例化Flask对象 app
app = Flask(__name__, template_folder='./templates/',static_folder="./static/") # 访问静态文件夹下的文件 http://127.0.0.1:5876/测试.jpg
#  [swagger]
swagger = Swagger(app)

# [允许跨域]
CORS(app, supports_credentials=True)
# CORS(app, resources=r'/*')

# [注册路由（蓝图）]
app.register_blueprint(login,url_prefix='/login')
app.register_blueprint(upload,url_prefix='/upload')
app.register_blueprint(logout,url_prefix='/logout')
app.register_blueprint(register,url_prefix='/register')
app.register_blueprint(downloadFile,url_prefix='/downloadFile')


# [文件上传]存放位置
print("上传文件存放路径为",os.path.dirname(os.path.abspath(__file__)))
app.config['UPLOAD_FOLDER'] = './upload/' # 注意 ：upload 前面不能加“/”
# [文件上传文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10M


# [动态路由参数]正则表达式
class RegexConver(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConver,self).__init__(url_map)
        self.regex = items[0]
        
app.url_map.converters['regex'] = RegexConver


# [静态路由]
@app.route('/')
#  每个路由对应一个函数（路由映射函数）
def root():
    return redirect(url_for('home'))# 重定向到home路由

# 后端渲染模板（前端页面）
@app.route('/home')
def home():
    return render_template('home.html', title="欢迎") # 模板内容进行渲染返回

# [动态路由]参数name在url中，数据类型默认为字符串
@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return  {"msg": "success", "status": 200, "data": name} 

# [动态路由]限制参数类型为整型
@app.route('/user_int/<int:id>', methods=['GET', 'POST'])
def user_int(id):
    print(id)
    return  {"msg": "success", "status": 200, "data": id}  #

# [动态路由]限制参数类型为浮点型
@app.route('/user_float/<float:score>', methods=['GET', 'POST'])
def user_float(score):
    return  {"msg": "success", "status": 200, "data": score} 

# [动态路由]限制参数类型为字符串
@app.route('/user_string/<string:name>', methods=['GET', 'POST'])
def user_string(name):
    return {"msg": "success", "status": 200, "data": name}

# [动态路由]限制参数类型为
@app.route('/user_any/<any(a,b,c):name>', methods=['GET', 'POST'])
def user_any(name):
    return {"msg": "success", "status": 200, "data": name}

# [动态路由]参数为接受用作目录分隔符的斜杠
@app.route('/templates/<path:filename>', methods=['GET', 'POST'])
def user_path(filename):
    return {"msg": "success", "status": 200, "data": filename}

# [动态理由]正则表达式
@app.route('/user_regex/<regex("[a-z]{3}"):name>',methods=['GET']) # 参数长度必须为3个字符，小写字母组成
def user_regex(name):
    request.cookies.get('username')
    return {"msg": "success", "status": 200, "data": name}


# [获取url ? 后面的&参数]    request.args.to_dict()
@app.route('/find', methods=['GET', 'POST'])
@swag_from('swagger_yaml/index.yaml')
def find():
    get_data = request.args.to_dict()# 获取传入的params参数
    username = get_data.get('username')
    password = get_data.get('password')
    # 返回
    return {"msg": "success", "code": 200, "data": {"username":username,"password":password}}

# 每个请求前执行
@app.before_request
def before_request():
    # print(request.url)
    # 判断是否为登录请求
    if ('login' in request.url or 'register' in request.url) and request.method == 'POST':
        print("当前是登录、注册接口，不会进行token验证，只进行token校验")
        return
    else:
        """
        1.获取请求头Authorization中的token
        2.判断是否以 Bearer开头
        3.使用jwt模块进行校验
        4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
        """
        # 获取请求头Authorization中的token
        auth = request.headers.get('Authorization')
        # 判断是否以 Bearer开头
        if auth and auth.startswith('Bearer '):
            # "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
            token = auth[7:]
            print("before_request token:",token)
            # "校验token"
            payload=jwt_token().verify_jwt(token,secret=config.JWT_SECRET_KEY)
            # payload = verify_jwt(token)
            print("before_request payload:",payload)
            # 判断payload是否为空
            if payload!=None:
                # "判断token的校验结果"
                # g.user_id = None
                # g.refresh = None
                # if payload:
                #     # "获取载荷中的信息，赋值给g对象"
                #     g.user_id = payload.get('user_id')
                #     g.refresh = payload.get('refresh')
                pass
            else:
                # 校验失败  例如：Signature has expired 签名过期
                return jsonify({"msg": "登录超时，请重新登录", "code": 403}) 
        # else:
        #     return jsonify({"msg": "登录超时，请重新登录", "code": 403}) 



# [后置处理]针对所有请求，对请求的Response header中加入header
@app.after_request
def after_request(resp):
    """
    请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    # 
    resp = make_response(resp)
    # 允许跨域访问
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = '*'#  允许跨域访问的请求头字段（星号表示全匹配）
    

    
    # 设置cookie，也可以把token放入cookie中
    # resp.set_cookie("token", token, max_age=3600)
    # resp.set_cookie("refresh_token", refresh_token, max_age=3600)
    return resp



# [错误处理]
@app.errorhandler(404)
def page_not_found(error):
    # return render_template('404.html'), 404
    return {"msg": "fial", "code": 201, "data": error}

# [启动服务器]
class InvalidUsage(Exception):  # 继承父类Exception
    # 定义异常类
    status_code = 400
    # 定义异常状态码
    def __init__(self, message, status_code=400):
        #  调用基类构造函数
        Exception.__init__(self)
        #  接收类实例化入参
        self.message = message
        self.status_code = status_code

# [错误处理]
@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    #  构造响应  返回错误异常内容给客户端
    response = make_response(error.message)
    #  响应状态码
    response.status_code = error.status_code
    return response

# [异常处理]
@app.route('/exception')
def exception():
    #  抛出异常
    raise InvalidUsage('No privilege to access the resource', status_code=403)




# [启动服务器]
if __name__ == "__main__":
    # 打印路由
    print(app.url_map)
    
    # debug=True        设置调试模式，生产模式的时候要关掉debug
    # host              主机地址
    # port              端口号，默认是5000
    # use_reloader=True 是否自动重启代码
    app.run(debug=True, host="127.0.0.1", port=5876, use_reloader=True)