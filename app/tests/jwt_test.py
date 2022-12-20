import jwt
import datetime

dic = {
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 过期时间
    'iat': datetime.datetime.utcnow(),  #   开始时间
    'iss': 'ChaosMoor',  #   签名
    'data': { #   内容，一般存放该用户id和开始时间
    'a': 1,
    'b': 2,
            },
        }

# 加密生成字符串
token = jwt.encode(dic, 'secret', algorithm='HS256')
print(token)
# 解密，校验签名
payload = jwt.decode(token, 'secret', issuer='ChaosMoor', algorithms=['HS256'])
print("payload:",payload)
# print(type(payload))
