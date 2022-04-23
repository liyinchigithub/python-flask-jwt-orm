# python-flask

[![python](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-374/) [![flask](https://img.shields.io/badge/flask-1.1.1-yellow.svg)](https://flask.palletsprojects.com/en/2.1.x/)[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v8.12.0-blue.svg)](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)[![Flask-jwt](https://img.shields.io/badge/jwt-v1.1.1-blue.svg)](https://pythonhosted.org/Flask-JWT/)



基于python RESTful api flask + jwt + orm 后端项目

* ORM 即Object-Relational Mapping，把关系数据库的表结构映射到对象上。

* JWT 即json web token，是一种认证机制，它是一种用于授权的标准协议。


# 目录说明

* |--app          # 应用目录
* |---api         # flask api
* |---common      # 公共模块
* |---db          # 数据库模块
* |---static      # 静态文件
* |---templates   # 模板文件
* |---tests       # 测试文件
* |---upload      # 上传文件存放位置
* |---config.py   # 配置文件
* |---run.py      # 启动文件


## 启动服务
```shell
cd /app
python run.py
```

## 接口列表

run.py中加入app.url_map 可查看当前项目所有可用接口
```shell
if __name__ == "__main__":
    print(app.url_map)# 打印路由
    app.run(debug=True, host="127.0.0.1", port=5876, use_reloader=True)
```
<img width="678" alt="image" src="https://user-images.githubusercontent.com/19643260/164743311-90f127f0-3369-408b-9cce-097e9502bbd5.png">


## 允许跨域配置

* 安装flask-cors
```shell
pip install flask-cors
```

* run.py
```python
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app, supports_credentials=True)
 
if __name__ == "__main__":
    app.run()
```

## Response headers 配置
```python
# 在每个请求后面加入header
@app.after_request
def after_request(resp):     
    """
     #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp
```
## Response headers cookie 配置

```python
# 在每个请求后面加入cookie
@app.after_request
def after_request(resp):     
    """
     请求钩子，在所有的请求发生后执行，设置cookie。
    :param resp:
    :return:
    """
    # 设置cookie，也可以把token放入cookie中
    resp.set_cookie("token", token, max_age=3600)
    resp.set_cookie("refresh_token", refresh_token, max_age=3600)
    return resp
```



## 获取请求参数

### 1.request.form['key']

* 针对 request body form-data

```python
    data = request.form['data']  # 获取值
    return json.dumps(data, ensure_ascii=False)
```

```python
    data =request.values
    username=data["username"]
    password=data["password"]
```

### 2.request.get_data    

>针对 POST request body json
```python
    # 获取请求参数
    request_data = request.get_data() 
    # 对于前端POST请求发送过来的json数据，Flask后台可使用 request.get_data() 来接收数据，数据的格式为 bytes；再使用 json.loads() 方法就可以转换字典。
    # 将bytes类型转换为json数据
    request_json_data = json.loads(request_data)# 将json字符串数据转换为字典
    username = request_json_data.get('username')# 获取num1
    password = request_json_data.get('password')# 
    # return json.dumps({"username":username,"password":password})# 将字典转换为json字符串
    return {"username":username,"password":password }# 返回json数据
```

### 3.request.args.get('key') 

>针对 GET url ?之后的参数

```python
request.args.get('key') # request url param
```

### 4.request.form['key']

* 针对GET 但有from-data

```python
get_data=request.form['username']# request form-data

```

### 5.request.args.to_dict()

* 针对 POST request url params
```python
    get_data = request.args.to_dict()# 获取传入的params参数
    username = get_data.get('username')
    password = get_data.get('password')
    return {"msg": "success", "status": 200, "data": {"username":username,"password":password}}
```

### 6.request.json.get('key')

* 针对 POST request body json
```python
    username = request.json.get('username')
    password = request.json.get('password')
    return {"msg": "success", "status": 200, "data": {"username":username,"password":password}}
```

```python
    request_data = request.json
    print("request.json",request.json)
    return {"msg": "success", "status": 200, "data": request_data}
```


## 重定向到指定路由函数

```python
return redirect(url_for('函数名'))  # 重定向
```


## Content-Type

### application/json

### application/x-www-form-urlencode

### application/xml

### mulitipart/form-data

## 文件上传

在 Flask 中处理文件上传非常简单。它需要一个 HTML 表单，其 ​enctype​ 属性设置为“​multipart/form-data”​，将文件发布到 URL。

URL 处理程序从 ​request.files[]​ 对象中提取文件，并将其保存到所需的位置。

每个上传的文件首先会保存在服务器上的临时位置，然后将其实际保存到它的最终位置。

目标文件的名称可以是硬编码的，也可以从 ​request.files[file] ​对象的​ filename ​属性中获取。

使用 ​secure_filename()​ 函数获取它的安全版本。

* 单元测试 上传文件
```shell
cd /app/tests/test_.py
pytest
```



## Flask JWT

### 生成token
```python
token = jwt.encode(_payload, secret, algorithm='HS256')
```
### 校验token
```python
payload = jwt.decode(token, secret, algorithms=['HS256'])
```

## Flask ORM SQLAlchemy

### 增加一行记录
```python

```

### 修改一行记录
```python

```

### 查询一行记录
```python

```

### 删除一行记录
```python

```


# 常见问题

* 1.
原因：

解决办法：

* 2.
原因：

解决办法：

* 3.
原因：

解决办法：



# 参考

[Flask 蓝图](https://www.cnblogs.com/jackadam/p/8684148.html)

[w3school Flask](https://www.w3school.com.cn/python/python_flask.asp)

[flask jwt](https://pythonhosted.org/Flask-JWT/)

[python orm SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)


