# 自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        print("ShopMiddleware initialized")

    def __call__(self, request):
        # 获取当前请求路径
        path = request.path
        print(f"Processing request for {path}")

        # 定义不用登录也可访问的路由url
        urllist = ['/login','/dologin','/logout','/register']
        # 判断当前请求的path是否不在urllist中
        if path not in urllist:
            # 判断当前用户是否没有登录
            if 'adminuser' not in request.session:
                print("User not logged in, redirecting to login page")
                # 执行登录界面跳转
                return redirect(reverse('myweb_login'))

            print(f"User logged in as {request.session['adminuser']}, processing request")

        # 对于其他情况，获取下一个中间件或视图的响应
        response = self.get_response(request)
        return response