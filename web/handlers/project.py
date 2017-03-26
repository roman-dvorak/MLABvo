#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import _sql
from . import BaseHandler

import tornado.escape
from tornado import web


class project_page(BaseHandler):
    @tornado.web.asynchronous
    def get(self, project):
        project_id = _sql("select id from vo_projects WHERE project_name = '%s'" %(project))[0][0]
        self.render("project_page.hbs", title="MLABvo | %s" %(project), project = project, project_id = project_id)

class project_table(BaseHandler):
    @tornado.web.asynchronous
    def get(self, project, table, page = 0):
        columns = _sql("SELECT column_name, datatype, description FROM vo_columns WHERE `table_name` = '%s' ORDER BY column_index" %table)
        count = _sql("select count(id) from %s" %(table))[0][0]
        sql_limit = self.get_argument('limit', 100)
        sql_page = self.get_argument('page', 0)
        sql_orderby = self.get_argument('orderby', 'id')
        sql_orderdesc = self.get_argument('desc', 'DESC')
        sql_where = self.get_argument('where', None)
        sql_whereoperator = self.get_argument('whereoperator', '=')
        sql_whereparam = self.get_argument('whereparam', '')

        sql_parameters = (sql_limit, sql_page, sql_orderby, sql_orderdesc, sql_where, sql_whereoperator, sql_whereparam)

        limit = "LIMIT 0,100"
        if sql_limit:
            limit_range = (int(sql_limit)*int(sql_page), int(sql_limit))
            limit = "LIMIT %d, %d" %limit_range

        where = ""
        if sql_where and sql_whereparam != "":
            where = "WHERE `%s` %s '%s'" %(sql_where, sql_whereoperator, sql_whereparam)

        orderby = ""
        if sql_orderby:
            orderby = "ORDER BY `%s` " %sql_orderby
            orderby += sql_orderdesc


        sql_dotaz = "SELECT * FROM `%s` %s %s %s" %(table, where, orderby, limit)
        print sql_dotaz
        data = _sql(sql_dotaz)

        print count
        print columns
        print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh"
        print sql_parameters
        self.render("project_table.hbs", title="MLABvo | %s/%s" %(project, table), project = project, count = count, table = table, page = int(sql_page), limit = int(limit_range[1]), data = data, columns = columns, sql_parameters = sql_parameters)

        