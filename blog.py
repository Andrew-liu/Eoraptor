# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os.path
import random
import unicodedata
import re, datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=9999,help="--port format: --port=<int>", type=int)

from pymongo import MongoClient
import markdown

class Application(tornado.web.Application):

    def __init__(self):
        hanlders = [
                (r"/", IndexHandler),
                (r"/login", LoginHandler),
                (r'/edit', EditHandler),
                (r'/article/([^/]+)', ArticleHandler), #只要不是反斜杠
                (r'/archive', ArchiveHandler),
                (r'/about', AboutHandler),
                ]
        settings = dict(
                    title=u"Andrew Liu | Snow Memory",
                    template_path=os.path.join(os.path.dirname(__file__), "templates"),
                    static_path=os.path.join(os.path.dirname(__file__), "static"),
                    cookie_secret="wnBzsGkRR2CMd0A0imH06CslRgSAQkrsus5kOq1/ZdI=",
                    xsrf_cookies=True,
                    login_url="/login",
                    debug=True,
                )
        tornado.web.Application.__init__(self, hanlders, **settings)  # call super init
        # create db object, use `self.application.db` to get it.
        conn = MongoClient('localhost', 27017)  # use passwd and user to start it
        self.db = conn.test_database
        # create new collection if itn't exist

class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        print "%s: %s" % (__name__, self.get_secure_cookie("user"))
        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    def get(self):
        # select from db, and transfer to html
        collection = self.db.blog
        posts = collection.find()
        """
        if not posts.count():  # not item, to edit new one
            self.redirect("/edit")
            return
        """
        if not posts:
            raise tornado.web.HTTPError(404)
        self.render('index.html', posts=posts)

class LoginHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.render("login.html")
            return
        # 已经成功登陆
        self.redirect("/")

    def post(self):
        username =  self.get_argument("email") # 获得用户名
        passwd = self.get_argument("password")
        # 此处应该有一个账户密码的验证
        self.set_secure_cookie("user", username)  # 给新登录的用户创建一个cookie, 并将这个cookie在response set_cookie返回给客户端,
        # 以后客户端的每次请求header中都有一个cookie域
        self.redirect("/")  # login success

class EditHandler(BaseHandler):

    def get(self):
        print "self.current_user: %s" % self.current_user
        if not self.current_user:  # 表示用户cookie过时, 或者签名不匹配
            self.redirect("/login")  #  重新登录, 此时客户端会得到cookie值
            return
        # 有cookie
        self.render("edit.html")

    def post(self):  # 创建文章
        title = self.get_argument("title")
        tag = self.get_argument("tag")
        content = self.get_argument("content")
        #  print "title = %s type= %s, tag = %s, content = %s" % (title, type(title), tag, content)
        collection = self.db.blog # get collection
        #  slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
        slug = "-".join(title.lower().strip().split())
        #  print "slug: ", slug
        post = {
                "title": title,
                "tag": tag,
                "slug": slug,
                "date": datetime.datetime.now(),
                "content": markdown.markdown(content)  # 增加代码高亮
                }
        print post
        collection.insert_one(post)
        self.redirect("/article/" + slug)

class ArticleHandler(BaseHandler):

    def get(self, slug):
        # 查询文章实体
        post = self.db.blog.find_one({"slug": slug})
        print post
        if not post: 
            raise tornado.web.HTTPError(404)
        self.render('post.html', post=post)

class ArchiveHandler(BaseHandler):

    def get(self):
        posts = self.db.blog.find()  # 生成一个可迭代的对象
        self.render("archive.html", posts=posts)

class AboutHandler(BaseHandler):

    def get(self):
        self.render("about.html")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
