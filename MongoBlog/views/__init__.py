#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tornado
from tornado.web import RequestHandler
from utils import json_decode


# 基类Handler, 用于被其他Handler集成
class BaseHandler(RequestHandler):

    @property
    def db(self):
        # 每个Handler中都包含一个application对象
        return self.application.db

    # 以json写入的response.body中
    def render_json(self, data, status_code=200):
        if not isinstance(data, basestring):
            data = json.dumps(data)
        self.set_status(status_code)
        self.set_header('Content-Type', 'application/json')
        return self.write(data)  # 写入到body

    # self.current_user会调用此函数
    def get_current_user(self):
        # print "%s: %s" % (__name__, self.get_secure_cookie("user"))
        print "get_current_user: %s" % self.get_secure_cookie("user")
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

    def get_int_argument(self, name, *arg, **kwargs):
        try:
            obj = self.get_argument(name, *arg, **kwargs)
            if not obj:
                return None
            return int(self.get_argument(name, *arg, **kwargs))
        except ValueError:
            raise tornado.web.HTTPError(400, 'Bad int value')

    @property
    def body(self):
        try:
            return json_decode(self.request.body)
        except ValueError:
            raise tornado.web.HTTPError(400, 'Bad json body')
