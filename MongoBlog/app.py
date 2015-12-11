#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from pymongo import MongoClient
from tornado.options import define, options
from urls import get_handlers


define("port", default=9999, help="--port format: --port=<int>", type=int)


settings = dict(
    title=u'Andrew Liu | Snow Memory',
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    cookie_secret="wnBzsGkRR2CMd0A0imH06CslRgSAQkrsus5kOq1/ZdI=",
    xsrf_cookies=True,
    login_url="/login",
    debug=True
)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = get_handlers()  # 获取所有的url及handler
        # 初始化app
        tornado.web.Application.__init__(
            self,
            handlers,
            **settings)
        # create db object, use `self.application.db` to get it.
        conn = MongoClient('localhost', 27017)
        self.db = conn.test_database
        # create new collection if itn't exist


application = Application()  # 生成app对象


def main():
    # 解析命令行参数
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print "Server is running 127.0.0.1: %s" % options.port
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
