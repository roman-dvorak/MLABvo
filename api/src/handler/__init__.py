#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import datetime
import json
import os
import sys

def _sql(query, read=False, db = 'MLABvo'):
        print "#>", query
        connection = mdb.connect(host="localhost", user="root", passwd="root", db=db, use_unicode=True, charset="utf8")
        cursorobj = connection.cursor()
        result = None
        try:
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                if not read:
                    connection.commit()
        except Exception, e:
                print "Err", e
        connection.close()
        return result