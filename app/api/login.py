#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 登录接口
from crypt import methods
from importlib.resources import path
from typing import Type
from flask import Flask, url_for, request, render_template, redirect, flash, session, make_response, Blueprint, g
from flask_wtf.file import FileField, FileRequired, FileAllowed  # 文件上传
from flask import send_from_directory  # 发送静态文件
from flask_cors import CORS  # 跨域访问
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter  # 正则表达式
import functools
import os
import datetime
import uuid  # 生成随机字符串
import json
from db import user  # 导入用户模型
import jwt
from api.jwt_token import *  # 引入封装的jwt_token
from flask import current_app as app  # 让蓝图可以使用app对象
from config import *  # JWT参数配置文件
from flasgger import Swagger  # flask swagger
from flasgger.utils import swag_from  # flask swagger
# 创建蓝图对象
login = Blueprint('login', __name__)

# [request body json]  多方式：request.json.get('key')、request.get_data()、


@login.route('/', methods=['POST'])
@swag_from('swagger_yaml/login.yaml')
def login_api():
    try:
        # 获取请求参数
        # 对于前端POST请求发送过来的json数据，Flask后台可使用 request.get_data() 来接收数据，数据的格式为 bytes；再使用 json.loads() 方法就可以转换字典。
        request_data = request.get_data()
        # 将bytes类型转换为json数据
        request_json_data = json.loads(request_data)  # 将json字符串数据转换为字典
        username = request_json_data.get('username')  # 获取num1
        password = request_json_data.get('password')
        # return json.dumps({"username":username,"password":password})# 将字典转换为json字符串
        # 查询数据库表，判断账号密码是否正确
        result = user.select_user_first_one(username)
        print("result:", result)
        # 如果账号密码正确
        if result != None or (result['password'] == password and result['username'] == username):
            print("result['password']:", result['password'])
            print("result['username']:", result['username'])
            # 生成时间信息
            current_time = datetime.datetime.utcnow()
            # 指定有效期  业务token -- 2小时,我们这里测试所以设置的秒数

            expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=config.JWT_EXPIRY_HOURS)  # days=1、seconds=3600
            print("expire_time:",expire_time)
            #
            print("config.JWT_EXPIRY_HOURS:", config.JWT_EXPIRY_HOURS)
            #
            _payload = {"data": {"user_id": "6666"}, "exp": expire_time,'iat': datetime.datetime.utcnow()}  # iat 开始时间  # exp 过期时间
          
            # 查询数据库,检查账号密码是否正确
            token = jwt_token().generate_jwt(payload=_payload,
                                             expiry=expire_time, secret=config.JWT_SECRET_KEY)
            print("login token:", token)
            # response body
            return {"msg": "success", "status": 200, "token": token}  # 返回json数据
        else:
            return {"msg": "fail", "status": 201, "data": "账号或密码错误"}  # 返回json数据
    except Exception as e:
        # 捕获异常，判断异常是否查询不到账号爆抛出的异常
        if str(e) == "'NoneType' object is not subscriptable":
            return {"msg": "fail", "status": 201, "data": "账号或密码错误"}  # 返回json数据
        else:
            return {"msg": "error", "status": 500, "data":  str(e)}


# @login.route('/getToken', methods=['GET', 'POST'])
# def get_token():
#     try:
#         _payload={"some": {"jwt": "jwt"}, "exp": datetime.utcnow(
#         )}
#         token = jwt.encode(_payload, JWT_SECRET_KEY, algorithm='HS256')
#         print("token",token)
#         return json.dumps({"token":token})
#     except Exception as e:
#         print(e)
#         return {"msg": "error", "status": 500, "data": e}  # 重定向到指定路由
