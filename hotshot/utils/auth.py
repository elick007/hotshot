from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from hotshot import models


# 实现自定义的认证类
class Authtication(BaseAuthentication):
    def authenticate(self, request):
        # 这儿的 request 对象不是 django 原生的 request 而是 rest_framework 内部进行封装过的 request
        # 使用 request._request 调用 django 原生的 request 对象
        token = request._request.GET.get('token')
        # 检查用户的 token 是否合法
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            # rest_framework 会在内部捕捉这个异常并返回给用户认证失败的信息
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在 rest_framework 内部会将这两个字段赋值给request以供后续调用
        return (token_obj.user, token_obj)
