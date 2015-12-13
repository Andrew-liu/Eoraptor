#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import markdown
import tornado
from views import BaseHandler
from controllers import page


class IndexHandler(BaseHandler):

    def get(self):
        """ 数据库存储结构
        {u'title': u'Hello world',
        u'content': u'<p>Hello world</p>',
        u'tag': u'test', u'date': datetime.datetime(2015, 11, 10, 22, 45, 59, 428000), # noqa
        u'_id': ObjectId('56420327354ac95b0f7a0a01'),
        u'slug': u'hello-world'}
        """
        # select from db, and transfer to html
        collection = self.db.blog
        posts = list(collection.find())
        p = page.Page(posts, 1)
        if not posts:
            raise tornado.web.HTTPError(404)
        self.render(
            'index.html',
            posts=p.current(),
            page=p)


class ArticleListHandler(BaseHandler):

    def get(self, page_num):
        posts = list(self.db.blog.find())
        p = p.Page(posts, page_num)
        if not posts:
            raise tornado.web.HTTPError(404)
        self.render(
            'index.html',
            posts=p.current(),
            page=p)


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
        #  print "title = %s type= %s, tag = %s, content = %s" % (title, type(title), tag, content)  # noqa
        collection = self.db.blog  # get collection
        #  slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")  # noqa
        slug = "-".join(title.lower().strip().split())
        #  print "slug: ", slug
        content = markdown.markdown(
            content,
            extensions=['markdown.extensions.extra', 'markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],  # noqa
            safe_mode=True,
            enable_attributes=False)
        post = {
            "title": title,
            "tag": tag,
            "slug": slug,
            "date": datetime.datetime.now(),
            # 增加代码高亮
            "content": content}  # noqa
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


class RSSHandler(BaseHandler):
    def get(self):
        posts = list(self.db.blog.find())
        self.set_header("Content-Type", "application/atom+xml")
        print posts
        self.render("rss.xml", entries=posts)
