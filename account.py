#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import cgi
import web
import urllib
import random
import string
import hashlib

from setting import render
from db import db

#valid useful functions
def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{1,20}$")
USER_RE_UNICODE = re.compile(u"^[\u4e00-\u9fa5]{1,20}$")

def valid_name(name):
    if name:
        if USER_RE.match(name):
            return USER_RE.match(name)
        if USER_RE_UNICODE.match(name):
            return USER_RE_UNICODE.match(name)
    return False


def valid_user(username):
    if not username:
        return False
    user = db.users.find_one({'name': username})
    return user

class AccountHandler(object):
    def redirect(self,path):
        web.seeother(path)
        
    def valid(self):
        cookie_user = web.cookies().get('user')
        user = valid_user(cookie_user)
        if user:
            return user
        else:
            #delete the cookie
            web.setcookie('user','')
            return None
