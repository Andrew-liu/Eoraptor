#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado
from views import BaseHandler


class AboutHandler(BaseHandler):

    def get(self):
        self.render("about.html")
