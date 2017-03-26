#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web
import glob

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>Hi!</h1><h1>MLABvo - API server</h1>")