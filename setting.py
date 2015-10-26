#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import web

from web.contrib.template import render_jinja

# define the template directory '/templates'
# using the jinja2
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates').replace('\\', '/')

render = render_jinja(
        templates_root,#set the template directory
        encoding = 'utf-8',#set the unicode
    )

