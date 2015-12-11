#!/usr/bin/env python
# -*- coding: utf-8 -*-
from views.home import *
from views.login import *
from views.about import *

hanlders = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r'/edit', EditHandler),
    (r'/article/([^/]+)', ArticleHandler),
    (r'/archive', ArchiveHandler),
    (r'/about', AboutHandler),
    ]


def get_handlers():
    return hanlders
