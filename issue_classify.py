#!/usr/bin/python
#coding: utf8
#########################################################################
# File Name: issue_classify.py
# Author: Justin Leo Ye
# Mail: justinleoye@gmail.com 
# Created Time: Thu Sep 17 21:02:23 2015
#########################################################################

import web
import json
import random
from bson.json_util import dumps

from db import db
from setting import render
from account import AccountHandler

from consts import DEFECT_CLAS_LIST, DEFECT_CLASSIFICATIONS

not_to_be_classified_now = ['https://api.github.com/repos/moment/moment', 'https://api.github.com/repos/jadejs/jade']

repos_dict = {
    'echart': 'https://api.github.com/repos/ecomfe/echarts'
}

not_to_classify_all_issues = True

def count_issues(repo=None):
    if repo:
        filters = {'classified': {'$ne': True}, 'repo': repo}
    elif not_to_classify_all_issues:
        filters = {'classified': {'$ne': True}, 'repo': {'$nin': not_to_be_classified_now}}
    else:
        filters = {'classified': {'$ne': True}}
    cnt = db.issues.find(filters).count()
    return cnt

def get_issue_not_classified_by_random(repo=None):
    cnt = count_issues(repo)
    skip = random.randint(0,cnt-1)
    if repo:
        filters = {'classified': {'$ne': True}, 'repo': repo}
    elif not_to_classify_all_issues:
        filters = {'classified': {'$ne': True}, 'repo': {'$nin': not_to_be_classified_now}}
    else:
        filters = {'classified': {'$ne': True}}
    issue = db.issues.find(filters).skip(skip).limit(1)
    if issue:
        return issue[0]
    return None

def get_issue(filters):
    issue = db.issues.find_one(filters)
    return issue

def set_issue_classified(filters):
    db.issues.update(filters, {'$set': {'classified': True}}, multi = True)

def increase_user_classifying_count(filters):
    if not db.user_classifying_account.find(filters).count():
        db.user_classifying_account.insert({'user': filters['user'], 'count': 1})
    else:
        db.user_classifying_account.update(filters, {'$inc': {'count': 1}}, multi = True)

def get_user_classifying_cnt(filters):
    account = db.user_classifying_account.find_one(filters)
    if account:
        return account['count']
    return 0

def gen_repo(repo_user, repo):
    return 'https://api.github.com/repos/'+repo_user+'/'+repo

def repo_to_repo_user_and_short_repo(repo):
    return tuple(repo.split('/')[-2::])

# some validations
def valid_defect_data(data, defect_clas):
    print 'data:',data
    print 'defect_clas:',defect_clas
    if data in [clas for clas,clas_title in DEFECT_CLASSIFICATIONS[defect_clas]['classification']]:
        return True
    return False

class RandomIssueToClassifyHandler(AccountHandler):
    def GET(self):
        user = self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")

        repo = None
        if user['name'] == u'平兄':
            repo = 'echart'
            try:
                repo = repos_dict[repo]
            except KeyError,e:
                print e
                repo = None
        print 'repo:',repo
        issue = get_issue_not_classified_by_random(repo)
        if issue:
            repo_user,repo = repo_to_repo_user_and_short_repo(issue['repo'])
            self.redirect('/classify/repo/%s/%s/issue/%s' % (repo_user, repo, issue['number']))
        return '没有issue需要分类了'

class IssueClassifyHandler(AccountHandler):
    def write_html(self, user=None, issue=None, defect_classified=None, user_classifying_cnt=None):
        return render.issue_classify(user=user, DCSL=DEFECT_CLAS_LIST, DCS=DEFECT_CLASSIFICATIONS, issue=issue, defect_classified=defect_classified, user_classifying_cnt=user_classifying_cnt)

    def get_issue(self, repo_user, repo, number):
        repo = gen_repo(repo_user, repo)
        repo = repo.encode('utf-8')
        return get_issue({'repo': repo, 'number': int(number)})

    def set_issue_classified(self, repo, number):
        set_issue_classified({'repo': repo, 'number': int(number)})

    def increase_user_classifying_count(self, user):
        increase_user_classifying_count({'user': user['name']})

    def get_user_classifying_cnt(self, user):
        return get_user_classifying_cnt({'user': user['name']})

    def GET(self, repo_user, repo, number):
        user = self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")

        issue = self.get_issue(repo_user, repo, number)
        user_classifying_cnt = self.get_user_classifying_cnt(user)
        return self.write_html(user=user, issue=issue, user_classifying_cnt=user_classifying_cnt)

    def POST(self, repo_user, repo, number):
        user = self.valid()
        if not user:
            return web.notfound("Sorry, the page you were looking for was not found.")

        form = web.input()
        defect_classify_result = {}
        any_error = False
        issue = self.get_issue(repo_user, repo, number)
        if not issue:
            return '404'

        defect_classified = {
            "repo": issue['repo'],
            "number": issue['number']
        }

        for defect_clas in DEFECT_CLAS_LIST:
            defect_classify_result[defect_clas] = {} 
            name = DEFECT_CLASSIFICATIONS[defect_clas]['name'][0]
            if not form.has_key(name):
                form[name] = None
            data = form[name]
            defect_classify_result[defect_clas]['data'] = data
            defect_classify_result[defect_clas]['error'] = None # init
            if not valid_defect_data(data, defect_clas):
                any_error = True
                defect_classify_result[defect_clas]['error'] = u'请选择正确的' + DEFECT_CLASSIFICATIONS[defect_clas]['name'][1]
            else:
                defect_classified[defect_clas] = data

        if any_error:
            user_classifying_cnt = self.get_user_classifying_cnt(user)
            return self.write_html(user=user, issue=issue, defect_classified=defect_classify_result, user_classifying_cnt=user_classifying_cnt)

        db.defects_classified.update({'repo': issue['repo'], 'number': issue['number']}, defect_classified, upsert=True)
        self.set_issue_classified(issue['repo'], issue['number'])
        self.increase_user_classifying_count(user)

        self.redirect('/classify')
