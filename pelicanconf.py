#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Robert Foss'
SITENAME = u'memcpy.io'
TAGLINE = u'Projects, hacks and engineering'
SITEURL = ''

PATH = 'content'

THEME = 'themes/pelican-svbtle'

TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = u'en'

SUMMARY_MAX_LENGTH=125

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

MENUITEMS = (
    ('About', 'about-me.html'),
    ('Contracting', 'contracting.html'),
    ('GitHub', 'https://github.com/robertfoss'),
    ('Previous posts', 'archives.html')
)
LINKS = ()

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

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
    "pelican-open_graph",
    "minification"
    ]
