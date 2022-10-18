#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 文件下载接口
import io
from flask import Flask, url_for, request, render_template, redirect, flash, session, make_response,Blueprint, send_file, Response
from flask_wtf.file import FileField, FileRequired, FileAllowed  # 文件上传
from flask import send_from_directory  # 发送静态文件
from flask_cors import CORS  # 跨域访问
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter # 正则表达式
import os,sys
import uuid  # 生成随机字符串
import json
from flask import current_app as app # 让蓝图可以使用app对象

sys.path.append('../')
from app.db import user # 导入用户模型


# 创建蓝图对象
downloadFile=Blueprint('downloadFile',__name__)


def file_send(file_path):  # 发送大文件可以该方法
    with open(file_path, 'rb') as f:
        while 1:
            data = f.read(20 * 1024 * 1024)  # 每次读取20M
            if not data:
                break
            yield data
'''
    [文件下载接口]
'''
@downloadFile.route('/DownLoadApk', methods=['GET'])
def downLoadApk():
    return send_file('./download/4.1.1a Alpha2-armeabi-v7a-release.apk', as_attachment=True, attachment_filename='4.1.1a Alpha2-armeabi-v7a-release.apk')  # 或使用下行代码
    # return send_from_directory('./', 'test.xlsx', as_attachment=True)
    

@downloadFile.route("/download2")
def download2():
    with open('test.xlsx', 'rb') as f:
        stream = f.read()
    response = Response(stream, content_type='application/octet-stream')
    response.headers['Content-disposition'] = 'attachment; filename=test.xlsx'
    return response


@downloadFile.route("/download3")
def download3():
    file = io.BytesIO()  # 本地没有文件，将内容写入内存发送
    file.write("你好".encode('utf-8'))
    file.seek(0)
    return send_file(file, as_attachment=True, attachment_filename="hi.txt")  # 用下面3行代码也可

    # response = Response(file, content_type='application/octet-stream')
    # response.headers['Content-disposition'] = 'attachment; filename=test.xlsx'
    # return response


@downloadFile.route("/download4")
def download4():
    file_name = "MEM3.mp4"
    response = Response(file_send(file_name), content_type='application/octet-stream')
    response.headers["Content-disposition"] = f'attachment; filename={file_name}'
    return response

'''
    [版本更新接口]
    http://127.0.0.1:5876/downloadFile/CheckAppVersion
'''
@downloadFile.route('/CheckAppVersion', methods=['POST'])
def check_app_version():
    try:
        request_data = request.json
        print("request.json",request.json)
        # # TODO 查询数据库是否有新版
        # print(type(user.select_user_page(request_data["page_num"],request_data["page_size"])))
        # # TODO 如果有新版，则返回一个数据类型为字典的json数据，如果没有新版，则返回None
        # result=user.select_user_page(request_data["page_num"],request_data["page_size"])
        # print("register list ：",result)
        
        return dict(code=200, success="true", upgrade="true")
    except Exception as e:
        print(e)
        return {"msg": "fali", "code": 401, "data": e}
    

if __name__ == '__main__':
    print("downloadFile")