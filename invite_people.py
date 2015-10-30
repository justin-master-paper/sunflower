#!/usr/bin/python
#coding: utf8
#########################################################################
# File Name: invite_people.py
# Author: Justin Leo Ye
# Mail: justinleoye@gmail.com 
# Created Time: Thu Sep 17 21:03:18 2015
#########################################################################
import web
from bson.json_util import dumps

from db import db
from setting import render
from account import AccountHandler, valid_name, valid_user

SEED_USER = os.getenv('SEED_USER', 'justin')

def get_all_users():
    users = db.users.find()
    return users

def generate_seed_user():
    if not get_all_users():
        db.users.insert({'name': SEED_USER})

class InvitePeopleHandler(AccountHandler):
    def write_html(self, user=None, error=None, invite_url=None):
        return render.invite_people(user=user, error=error, invite_url=invite_url)

    def get_user(self, name):
        user = db.users.find_one({'name': name})
        return user

    def GET(self):
        user = self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")
        return self.write_html(user=user)

    def POST(self):
        user = self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")
        form = web.input()
        username = form['username']
        error = None
        if not isinstance(username, unicode):
            username = username.decode('utf-8')
        if not valid_name(username):
            error = u'只能输入汉字、字母、数字或者下划线'
        if self.get_user(username):
            error = u'已经有人邀请过他了'
        if error != None:
            return self.write_html(user=user, error=error)

        db.users.insert({'name': username})
        invite_url = '/user/' + username
        return self.write_html(user=user, invite_url=invite_url)

class UserHandler(AccountHandler):
    def write_html(self, user=None):
        return render.user(user=user)

    def GET(self,username):
        user = valid_user(username)
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")
        web.setcookie('user', user['name'])
        return self.write_html(user=user)

if __name__ == '__main__':
    generate_seed_user()
