#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
from tornado import web
from tornado import websocket
from . import _sql, wwwCleanName, BaseHandler, sendMail
import json
import datetime
import smtplib


import urllib
import urllib2
import requests

from requests_oauthlib import OAuth2Session

class O_logout(BaseHandler):
    def get(self):
        print "odhlasuji TE!!!!!!!!!!!!!!!"
        self.clear_cookie("login")
        self.clear_cookie("token")

        self.redirect("/")


class O_login(BaseHandler):
    def get(self):
        login = self.get_secure_cookie("login", None)
        #token = eval(self.get_secure_cookie("token", None))

        print "###########################"
        print login

        #else:
        github = OAuth2Session("575de67b6f7db300207f", scope = ["user:email"])
        authorization_url, state = github.authorization_url('https://github.com/login/oauth/authorize')

        print "redirect", state, authorization_url
        self.redirect(authorization_url)

        #print "redirect"
        #self.redirect('https://github.com/login/oauth/authorize?client_id=%s' %("34650903e94dd929f0b7"), permanent=True)

class O_github(BaseHandler):

    def get(self):
        github_code = self.get_argument('code', None)
        github = OAuth2Session("575de67b6f7db300207f", scope = ["user:email"])
        token = github.fetch_token('https://github.com/login/oauth/access_token', code = github_code, client_secret='74c374cb408d81b69fb748df7f2c5ab45995ce99')
        user_j = github.get('https://api.github.com/user').json()
        email_j = github.get('https://api.github.com/user/emails').json()
        user_db=_sql("SELECT count(*) FROM MLABvo.vo_user WHERE login = '%s';" %(user_j['login']))[0][0]

        print token
        print user_j
        print "------------"

        email = None
        for e in email_j:                   # najdi mail, ktery je primarni
            if e['primary'] == True:
                email = e['email']
            else:
                print "mail vedlejsi", e
        print email


        print user_db

        self.set_secure_cookie('login', user_j['login'])
        self.set_secure_cookie('token', repr(token))

        utcnow = datetime.datetime.utcnow().isoformat()

        if user_db == 1: # uzivatel je zpet :)
            _sql("UPDATE `vo_user` SET `name` = '%s', `email` = '%s', `service` = '%s', `last_login` = '%s' WHERE login = '%s';" 
                %(user_j['name'], email, "github", utcnow, user_j['login']))
            self.redirect("/")

        elif user_db == 0: # Novy uzivatel
            _sql("INSERT INTO `MLABvo`.`vo_user` (`login`, `name`, `email`, `service`, `date_joined`, `last_login`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
                %(user_j['login'], user_j['name'], email, "github", utcnow, utcnow))

            sendMail("%s<%s>"%(user_j['name'],email),"Welcome to MLABvo, RTbolidozor", open("/home/roman/repos/RTbolidozor/emails/new_reg","r").read()%(user_j['name']))
            self.redirect("/newuser")

        else:
            self.write("Chyba, prosím nahlašte do mailinglistu Bolidozoru č.0003")


        #_sql("REPLACE INTO `MLABvo`.`geozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))
                

        #self.redirect('https://github.com/login/oauth/authorize?client_id=%s' %("34650903e94dd929f0b7"), permanent=True)


class newuser(BaseHandler):
    def get(self):
        self.write("Ahoj novy uzivateli :), pokracuj na <a href='/'>MLABvo</a>")
