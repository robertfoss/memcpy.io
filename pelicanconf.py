#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date

AUTHOR = u'Robert Foss'
SITENAME = u'memcpy.io'
SITEURL = ''
KEYWORDS = "Robert Foss, Open Source, Software, Linux, Embedded, Engineer"

PATH = 'content'

THEME = 'themes/ruuda'

TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = u'en'

SUMMARY_MAX_LENGTH=125
CURRENTYEAR = str(date.today().year)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Make pages appear in the top dir
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_LINKS_ON_MENU = False

DIRECT_TEMPLATES = ['index', 'contact', 'about']

MENUITEMS = (
    ('Blog', '/index.html'),
    ('About', '/about.html'),
    ('Contact', '/contact.html'),
    ('GitHub', 'https://github.com/robertfoss'),
)
LINKS = ()


CURRENTYEAR = str(date.today().year)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 999

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['videos', 'images', 'files', 'favicon.png', 'logo.png', 'me.jpg', 'keybase.txt']
EXTRA_PATH_METADATA = {
    'favicon.png': {'path': 'favicon.png'},
    'logo.png': {'path': 'logo.png'},
    'me.jpg': {'path': 'me.jpg'},
    'keybase.txt': {'path': 'keybase.txt'},
}


PLUGIN_PATHS = ["plugins", "plugins"]
PLUGINS = [
    "pelican-open_graph"
#    "minification"
    ]
