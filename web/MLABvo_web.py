#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado
#from tornado import web
from tornado import ioloop
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web
import os
import json
#import sqlite3
import MySQLdb as mdb
import time
import datetime
import calendar
import svgwrite
import crypt


from handlers import auth, project
from handlers import _sql, BaseHandler

tornado.options.define("port", default=10005, help="port", type=int)
tornado.options.define("debug", default=True, help="debug mode")



class WebHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        self.render("home.hbs", title="voMLAB", user=self.get_secure_cookie("login"))



class WebApp(tornado.web.Application):
    def __init__(self, config={}):

        name = 'MLABvo'
        server = 'vo.mlab.cz'

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        self._sql = _sql

        handlers =[
            
            (r'/project/(.*)', project.project_page),
            (r'/table/(?P<project>.*)/(?P<table>.*)', project.project_table),

            (r'/login/oauth/github', auth.O_github),
            (r'/login/', auth.O_login),
            (r'/login', auth.O_login),
            (r'/logout/', auth.O_logout),
            (r'/logout', auth.O_logout),
            (r'/newuser', auth.newuser),
            
            (r'/(favicon.ico)', web.StaticFileHandler, {'path': '.'}),
            (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
            (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": './static/media/' }),
            (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": './static/media/' }),
            (r"/(.*\.css)", tornado.web.StaticFileHandler,{"path": './static/css/' }),

            (r'/', WebHandler),
            (r"/(.*)", WebHandler),
        ]
        settings = dict(
            cookie_secret="ROT13IrehaxnWrArwyrcfvQvixnAnFirgr",
            template_path= os.path.join(os.path.dirname(__file__), "template"),
            static_path= os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            name=name,
            server_url=server,
            site_title=name,
            login_url="/login",
            #ui_modules=modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
            autoreload=True
        )

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebApp())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
