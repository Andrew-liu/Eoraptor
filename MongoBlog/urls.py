#!/usr/bin/env python
# -*- coding: utf-8 -*-
from views.home import *
from views.login import *
from views.about import *

hanlders = [
    (r"/", IndexHandler),
    (r'/page/(\d+)', ArticleListHandler),
    (r'/edit', EditHandler),
    (r'/article/([^/]+)', ArticleHandler),
    (r'/search', SearchHandler),
    (r'/archive', ArchiveHandler),
    (r'/about', AboutHandler),
    # about login
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    # RSS
    (r'/rss', RSSHandler),
    ]


def get_handlers():
    return hanlders
