#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import markdown
import tornado
from views import BaseHandler


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


class EditHandler(BaseHandler):

    def get(self):
        print "self.current_user: %s" % self.current_user
        # 表示用户cookie过时, 或者签名不匹配
        if not self.current_user:
            # 重新登录, 此时客户端会得到cookie值
            self.redirect("/login")
            return
        # 有cookie
        self.render("edit.html")

    def post(self):  # 创建文章
        title = self.get_argument("title")
        tag = self.get_argument("tag")
        content = self.get_argument("content")
        #  print "title = %s type= %s, tag = %s, content = %s" % (title, type(title), tag, content)
        collection = self.db.blog  # get collection
        #  slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
        slug = "-".join(title.lower().strip().split())
        #  print "slug: ", slug
        post = {
            "title": title,
            "tag": tag,
            "slug": slug,
            "date": datetime.datetime.now(),
            # 增加代码高亮
            "content": markdown.markdown(content)}
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
