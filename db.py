#!/usr/bin/python
#coding: utf8
#########################################################################
# File Name: db.py
# Author: Justin Leo Ye
# Mail: justinleoye@gmail.com 
# Created Time: Thu Sep 17 19:37:52 2015
#########################################################################

import os
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

client = MongoClient(MONGO_URI)

db = client.sun_flower

