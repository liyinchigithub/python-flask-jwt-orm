import jwt
from flask import current_app


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
            secret = current_app.config['JWT_SECRET']
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
            secret = current_app.config['JWT_SECRET']

        try:
            payload = jwt.decode(token, secret, algorithm=['HS256'])
        except jwt.PyJWTError:
            payload = None

        return payload
