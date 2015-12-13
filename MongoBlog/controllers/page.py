#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import ceil
from pymongo import MongoClient


class Page(object):

    def __init__(self, posts, page_num, page_count=5):
        self.posts = posts
        self.count = len(posts)  # 总文章数
        # 总页数
        self.pages = int(ceil(float(self.count) / page_count))
        print "pages: ", self.pages
        # 当前页
        self.page_num = page_num if 1 <= page_num <= self.pages else 1  # noqa
        self.page_count = page_count  # 每页显示Post数

    def has_next(self):
        return (self.page_num + 1 <= self.pages)

    def has_previous(self):
        return (self.page_num - 1 >= 1)

    def current(self):
        if self.page_count > self.count:
            return self.posts
        else:
            return self.posts[(self.page_num - 1) * self.page_count: self.page_num * self.page_count]  # noqa


if __name__ == '__main__':
    p = Page([1, 2, 3, 4, 5, 6, 7], 2)
    print p.has_next()  # False
    print p.has_previous()  # True
    print p.current()
    """
    {u'title': u'Hello world',
    u'content': u'<p>Hello world</p>',
    u'tag': u'test', u'date': datetime.datetime(2015, 11, 10, 22, 45, 59, 428000), # noqa
    u'_id': ObjectId('56420327354ac95b0f7a0a01'),
    u'slug': u'hello-world'}
    """
    # client = MongoClient('localhost', 27017)
    # db = client.test_database
    # coll = db.blog
    # print list(coll.find())
