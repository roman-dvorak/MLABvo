#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.speedups


from handler import base
from handler import api

tornado.options.define("port", default=10000, help="port", type=int)
tornado.options.define("debug", default=True, help="debug mode")


class WebApp(tornado.web.Application):

    def __init__(self, config={}):

        name = 'MLABvo-APIserver'
        server = 'meteor1.astrozor.cz'

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        handlers = [
            (r"/api", base.MainHandler),
            (r"/(.*)", api.api),
            (r"/api/(.*)", api.api),
        ]
        settings = dict(
            cookie_secret="brauoaykikeuaoeikaoeiakku",
            #template_path=os.path.join(self._base_dir, "template"),
            #template_path= "/home/odroid/repos/arom-web_ui/src/aromweb/template/",
            #static_path=os.path.join(self._base_dir, "static"),
            #static_path= "/home/odroid/repos/arom-web_ui/src/aromweb/static/",
            xsrf_cookies=True,
            name=name,
            server_url=server_url,
            site_title=name+" | MLABvo API",
            #ui_modules=modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebApp())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()