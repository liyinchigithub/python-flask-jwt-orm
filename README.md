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
* |---static      # 静态文件（图片）
* |---templates   # 模板文件
* |---tests       # 测试文件
* |---upload      # 上传文件存放位置
* |---config.py   # 配置文件
* |---run.py      # 启动文件
* |---postman     # postman脚本
* |---sql         # sql数据库脚本


# 安装依赖

## 创建虚拟目录

```shell
# python -m venv 虚拟环境名称，名称是随意起的
python -m venv tutorial-env
```
## 激活虚拟环境
当激活虚拟环境时命令行上会有个虚拟环境名前缀。

### Unix或MacOS上激活虚拟环境
```shell
source tutorial-env/bin/activate
```
### windows上激活虚拟环境
```shell
tutorial-env\Scripts\activate.bat

#### 冻结第三方库，就是将所有第三方库及版本号保存到requirements.txt文本文件中
```shell
pip freeze > requirements.txt
```

###  安装requirement.txt
```shell
pip install -r requirements.txt
```

## 启动服务
```shell
cd app
python run.py
```

## 启动docker-mysql5.7

## 接口列表

<!-- run.py中加入app.url_map 可查看当前项目所有可用接口 -->
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
### 7.访问静态文件

```python
app = Flask(__name__, template_folder='./templates/',static_folder="./static/") 

# 访问静态文件夹下的文件 http://127.0.0.1:5876/测试.jpg
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
## 文件下载




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


```python
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date, Time, DECIMAL, Text, create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid,sys

# 创建对象的基类:
Base = declarative_base()

# 创建表对象:


class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(Integer, autoincrement=True,
                primary_key=True, nullable=False)  # 自增、主键、不为空
    username = Column(String(100), nullable=False)  # 字符串、不为空
    password = Column(String(500), nullable=False)  # 字符串、不为空
    role = Column(String(500), nullable=False)  # 字符串、不为空
    type = Column(Integer, nullable=False)  # 整型、不为空
    mark = Column(String(500), nullable=False)  # 字符串、不为空
    uuid = Column(String(500), nullable=False)  # 字符串、不为空
    is_delete = Column(Boolean, nullable=False)  # 布尔值、不为空
    create_date = Column(DateTime, nullable=False)  # 日期时间、不为空，  数据库自动生成时间戳
    update_date = Column(DateTime, nullable=False)  # 日期时间、不为空，  数据库自动生成时间戳
    # datetime.datetime.now() 获取当前时间

    # sqlalchemy转json，方式一
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'type': self.type,
            'mark': self.mark,
            'uuid': self.uuid,
            'is_delete': self.is_delete,
            'create_date': self.create_date,
            'update_date': self.update_date
        }
    # sqlalchemy转dict，方式二

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'type': self.type,
            'mark': self.mark,
            'uuid': self.uuid,
            'is_delete': self.is_delete,
            'create_date': self.create_date,
            'update_date': self.update_date
        }


'''
    CREATE TABLE IF NOT EXISTS `user`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `username` VARCHAR(100) NOT NULL COMMENT '账号',
    `password` VARCHAR(500) NOT NULL COMMENT '密码',
    `role` VARCHAR(500) NOT NULL COMMENT '角色',
    `type` INT(255) NOT NULL COMMENT '类型ID',
    `mark` VARCHAR(500) NOT NULL COMMENT '备注',
    `uuid` VARCHAR(500) NOT NULL COMMENT '唯一uuid',
    `is_delete` TINYINT NOT NULL COMMENT '是否使用',
    `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '日期',
    `update_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新日期',
    PRIMARY KEY (`id`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
```

### 增加一行记录
```python
# 初始化数据库连接: TODO 参数化
engine = create_engine(
    f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
'''
    # [用户表插入数据-创建用户]
    @param: username string
    @pparam: password string
    @pparam: role string
    @pparam: type int
    @pparam: mark string
    @return: user object
'''

def insert_user(username, password, role, type, mark):
    try:
        # 创建新User对象:
        user = User(username=username, password=password, role=role, type=type, mark=mark,
                    uuid=str(uuid.uuid4()), is_delete=False)  # 插入数据表成功后，返回的是一个对象，具有id属性
        # 添加到session
        session.add(user)
        print("user:", user)
        # 提交即保存到数据库
        session.commit()
        # 判断是否插入成功
        if user.id:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session
# 初始化数据库连接: TODO 参数化
engine = create_engine(
    f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

'''
    [用户表插入数据-创建用户]
    @param: username string
    @pparam: password string
    @pparam: role string
    @pparam: type int
    @pparam: mark string
    @return: user object
'''


def insert_user(username, password, role, type, mark):
    try:
        # 创建新User对象:
        user = User(username=username, password=password, role=role, type=type, mark=mark,
                    uuid=str(uuid.uuid4()), is_delete=False)  # 插入数据表成功后，返回的是一个对象，具有id属性
        # 添加到session
        session.add(user)
        print("user:", user)
        # 提交即保存到数据库
        session.commit()
        # 判断是否插入成功
        if user.id:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session

```

### 修改一行记录
```python
'''
    [修改]
    param: id int
    param: data dict
'''
def update_user(id, data):
    try:
        # 根据 id 字段修改数据
        res = session.query(User).filter(User.id == id).update(data)
        print("res:", res)  # 1
        print("修改一条数据======================")
        session.commit()
        return res
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session
```

### 查询一行记录
```python

'''
    [查询(多条件or)]
'''
def select_user_multiple_condition_and(searchText):
    try:
        # res = session.query(UserMonitor).filter(
        #     UserMonitor.username.like('%liyinchi%'), UserMonitor.id > 5).all()  # 方法一
        # res = session.query(UserMonitor).filter(
        #     and_(UserMonitor.username.like('%liyinchi%'), UserMonitor.id > 5)).all()  # 方法二
        # res = session.query(JiraJql).filter(
        #         JiraJql.title.like(f'%{title}%')).all()
        res = session.query(User).filter(or_(User.username.like(f'%{searchText}%'), User.role.like(f'%{searchText}%'), User.mark.like(f'%{searchText}%'))).all()  # 方法二
        print("res:",res)
        # for r in res7:
        #     print("r.title", r.title)
        #     print("r.id:", r.id)
        print("多条件  且 and======================")
        if isinstance(res, list):
            return [{column.name:getattr(value,column.name) for column in value.__table__.columns} for value in res]
        else:
            if hasattr(res, '__table__'):
                return {column.name:getattr(res,column.name) for column in res.__table__.columns}
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session

'''
     [ 查询(检查账号密码是否正确)]
'''
def select_check_username_password(username, password):
    try:
        # 获取多条，只返回第一条
        res = session.query(User).filter(User.username == username).filter(
            User.password == password).first()
        print(type(res))
        if isinstance(res, list):
            return [{column.name: getattr(value, column.name) for column in value.__table__.columns} for value in res]
        else:
            if hasattr(res, '__table__'):
                return {column.name: getattr(res, column.name) for column in res.__table__.columns}
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session

'''
    [精确查询(用户姓名)仅返回匹配多条中的第一条]
    param: condition 列表 例如：['liyinchi1','liyinchi2']
    return json
'''
def select_user_first_one(username):
    try:
        # 获取多条，只返回第一条
        res = session.query(User).filter(User.username == username).first()
        print(type(res))
        if isinstance(res, list):
            return [{column.name: getattr(value, column.name) for column in value.__table__.columns} for value in res]
        else:
            if hasattr(res, '__table__'):
                return {column.name: getattr(res, column.name) for column in res.__table__.columns}
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session

'''
    [精确查询(用户ID)仅返回匹配多条中的第一条]
    param: condition 列表 例如：['liyinchi1','liyinchi2']
    return json
'''
def select_user_id_first_one(id):
    try:
        # 获取多条，只返回第一条
        res = session.query(User).filter(User.id == id).first()
        print(type(res))
        if isinstance(res, list):
            return [{column.name: getattr(value, column.name) for column in value.__table__.columns} for value in res]
        else:
            if hasattr(res, '__table__'):
                return {column.name: getattr(res, column.name) for column in res.__table__.columns}
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session


'''
    [模糊查询（用户姓名）]
    param: username string
'''
def select_user_fuzzy(username):
    try:
        res = session.query(User).filter(
            User.username.like(f'%{username}%')).all()
        for r in res:
            print("r.username", r.username)
            print("r.id:", r.id)
        res = session.query(func.count(User.id), func.count(
            User.username)).group_by(User.id).all()
        print("func.count(User.id):", res)
        print("模糊查询======================")
        return res
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session


'''
    [查询(全量数据)]
'''
def select_user_all():
    try:
        res = session.query(User).all()
        if isinstance(res, list):
            return [{column.name:getattr(value,column.name) for column in value.__table__.columns} for value in res]
        else:
            if hasattr(res, '__table__'):
                return {column.name:getattr(res,column.name) for column in res.__table__.columns}
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session

'''
    [分页查询]
    @param: page_size int  每页显示的记录数量
    @param: page_num int 当前页码
'''
def select_user_page(page_num=1, page_size=10):
    try:
        # 偏移量
        offset_data = page_size * (page_num-1)
        # 查询数据
        res = session.query(User).offset(offset_data).limit(page_size)
        # to_dict方法是在 创建数据模型 时就定义好了的
        res = [item.to_dict() for item in res]
        print("select_user_page res:", type(res))  # list
        return res
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session


```

### 删除一行记录
```python
def delete_user(id):
    try:
        # 根据 id 字段删除数据
        res = session.query(User).filter(
            User.id == id).delete()  # 根据id字段，删除指定数据
        print("res11:", res)  # 1表示删除成功，0表示删除失败
        print("删除一条数据======================")
        session.commit()
        return res
    except Exception as e:
        print(e)
        session.rollback()# 回滚
    finally:
        session.close()# 关闭session
```

### 其他

```Python
# [is null]
res5 = session.query(User).filter(User.username.is_(None)).all()
for r in res5:
    print("r.username", r.username)
    print("r.id:", r.id)
print("为空======================")

# [is not null]
res6 = session.query(User).filter(User.username.isnot(None)).all()
for r in res6:
    print("r.username", r.username)
    print("r.id:", r.id)
print("不为空======================")

# [and]
res7 = session.query(User).filter(
    User.username.like('%liyinchi%'), User.id > 5).all()  # 方法一
res7 = session.query(User).filter(
    and_(User.username.like('%liyinchi%'), User.id > 5)).all()  # 方法二
res7 = session.query(User).filter(User.username.like(
    '%liyinchi%')).filter(User.id > 5).all()  # 方法三

for r in res7:
    print("r.username", r.username)
    print("r.id:", r.id)
print("多条件  且 and======================")

# [or]
res8 = session.query(User).filter(
    or_(User.username.like('%liyinchi%'), User.id > 5)).all()  # 方法二
for r in res8:
    print("r.username", r.username)
    print("r.id:", r.id)
print("或 or======================")

# [限制返回条数]
res = session.query(User).limit(2).all()
# [限制，类似mysql的limit]
res = session.query(User).filter(
    User.id > 1, User.username.like('%liyinchi%'))[1:3]
print("res", res)
print("限制返回条数======================")

# [指定范围之间 between]
res = session.query(User).filter(User.id.between(1, 3))
print("res", res)
print("指定范围之间 between======================")

# [通配符]
res = session.query(User).filter(User.username.like('liyinchi_'))
res = session.query(User).filter(User.username.like('%liyinchi'))
print("res", res)
print("通配符======================")

# [排序] 默认升序，desc降序
res = session.query(User).order_by(User.id.desc()).all()
print("res", res)  # 返回的是一个列表
print("排序======================")


# [分组]
res = session.query(func.count(User.id), func.max(
    User.id), func.min(User.id)).group_by(User.type).all()
print("res", res)  # [(1, 1, 1), (1, 1, 1)]
print("分组======================")

[连表]
res = session.query(User).join(UserType, isouter=True) # 内连接取外表的交集   isouter=True表示可以不存在关联的数据
print("res",res)# [(1, 'liyinchi1', '1', '1'), (2, 'liyinchi2', '1', '1'), (3, 'liyinchi3', '1', '1')]
print("连表======================")
res = session.query(User).outerjoin(UserType)# 外连接取外表的并集
print("res",res)# [(1, 'liyinchi1', '1', '1'), (2, 'liyinchi2', '1', '1'), (3, 'liyinchi3', '1', '1')]
print("连表======================")
```


# 接口文档（swagger）

本项目使用flasgger

>http://127.0.0.1:5876/apidocs/#/

<img width="1439" alt="image" src="https://user-images.githubusercontent.com/19643260/208307968-03625cea-976d-47c7-a100-b5d7403d14ac.png">

[flask flasgger 官方文档](https://github.com/flasgger/flasgger)

[Flask 引入swagger](https://blog.csdn.net/u013302168/article/details/128337182)



# 常见问题

* 1.jwt 报错“'str' object has no attribute 'decode'”
![image](https://user-images.githubusercontent.com/19643260/208307781-4959a8a6-c80d-40ac-bb6d-dea61d21ea40.png)

解决办法：
修改成 return token
![image](https://user-images.githubusercontent.com/19643260/208307764-45aed83c-e2c3-417f-81c2-30d7fde09c3b.png)

* 2.
原因：

解决办法：

* 3.
原因：

解决办法：

* 4.
原因：

解决办法：

# 参考

[Flask 蓝图](https://www.cnblogs.com/jackadam/p/8684148.html)

[w3school Flask](https://www.w3school.com.cn/python/python_flask.asp)

[flask jwt](https://pythonhosted.org/Flask-JWT/)

[python orm SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)

[flask flasgger](https://github.com/flasgger/flasgger)

[flask swagger flask-restplus](https://flask-restplus.readthedocs.io/en/stable/swagger.html)

[flask swagger](https://www.cnblogs.com/lifei01/p/13797889.html)
