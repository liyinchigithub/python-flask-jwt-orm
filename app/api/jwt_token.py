import jwt
from flask import current_app
import config

# jwt 官方文档 https://pyjwt.readthedocs.io/en/latest/usage.html
class jwt_token():
    # 构造函数（类实例化对象时传入参数） 类(形参)
    def __init__(self):
        pass
   
    def generate_jwt(self, payload, expiry, secret=None):
        """
        生成jwt
        :param payload: dict 载荷
        :param expiry: datetime 有效期
        :param secret: 密钥
        :return: jwt
        """
        _payload = {'exp': expiry}
        _payload.update(payload)

        if not secret:
            secret = config.JWT_SECRET_KEY
        # bytes.decode('utf-8', 'ignore')
        token = jwt.encode(_payload, secret, algorithm='HS256')
        return token

    def verify_jwt(self, token, secret=None):
        """
        检验jwt
        :param token: jwt
        :param secret: 密钥
        :return: dict: payload
        """
        if not secret:
            secret = secret = config.JWT_SECRET_KEY

        try:
            print("verify_jwt token:",token)
            print("verify_jwt secret:",secret) # liyinchi1234567890
            payload = jwt.decode(token, secret, algorithms= ['HS256'] )
            print("verify_jwt payload:",payload) # {'exp': 1671632633, 'some': {'jwt': 'jwt'}}
            
        except jwt.PyJWTError as e:
            print("verify_jwt PyJWTError",str(e))
            payload = None

        return payload
