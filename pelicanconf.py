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

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
            ('Archives', 'archives.html'),
            ('Github', 'https://github.com/robertfoss'),
        )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['videos', 'images', 'favicon.png', 'logo.png']
EXTRA_PATH_METADATA = {
    'favicon.png': {'path': 'favicon.png'},
    'logo.png': {'path': 'logo.png'}
}
