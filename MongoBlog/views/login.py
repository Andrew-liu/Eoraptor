#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado
from views import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        """
        if not self.current_user:
            self.render("login.html")
            return
        # 已经成功登陆
        self.redirect("/")
        """
        self.render("login.html")

    def post(self):
        username = self.get_argument("email")  # 获得用户名
        passwd = self.get_argument("password")
        # 此处应该有一个账户密码的验证
        # 给新登录的用户创建一个cookie, 并将这个cookie在response set_cookie返回给客户端,
        self.set_secure_cookie("user", username)
        # 以后客户端的每次请求header中都有一个cookie域
        self.redirect("/")  # login success
