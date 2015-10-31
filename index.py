#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import copy
import web
from web.httpserver import StaticMiddleware

from setting import render
from account import AccountHandler
from issue_classify import RandomIssueToClassifyHandler, IssueClassifyHandler, count_issues
from invite_people import InvitePeopleHandler, UserHandler, get_all_users

# the urls of the web system
urls = (
    '/(.*)/', 'RedirectHandler',
    '/', 'HomeHandler',
    '/home','HomeHandler',
    '/classify', 'RandomIssueToClassifyHandler',
    '/classify/repo/(.*)/(.*)/issue/([0-9]*)', 'IssueClassifyHandler',
    '/invite-people', 'InvitePeopleHandler',
    '/user/(.*)', 'UserHandler',
)


#access the database
#db = web.database(dbn='mysql', db='alexbox', user='root', pw='alexzone')

class Handler:
    def redirect(self,path):
        web.seeother(path)

#when the url ended with '/',then redirect the url to the one without ending '/'
class RedirectHandler(Handler):
    def GET(self, path):
        self.redirect('/' + path)

class HomeHandler(AccountHandler):
    def write_html(self, user=None, contributors=None, issue_count=None):
        return render.home(user=user, contributors=contributors, issue_count=issue_count)

    def GET(self):
        user=self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")

        contributors = get_all_users()
        issue_count = count_issues()

        return self.write_html(user=user, contributors=contributors, issue_count=issue_count)

app = web.application(urls, globals())

application = app.wsgifunc(StaticMiddleware)

