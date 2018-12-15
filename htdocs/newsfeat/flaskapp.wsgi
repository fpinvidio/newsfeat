#!/usr/bin/python
import sys
import logging
import site
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/")
sys.path.insert(0,"/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/")
site.addsitedir('/var/venvs/cs410/local/lib/python2.7/site-packages')

from newsfeat import app as application
application.secret_key = '\x03U+\xb5\x15\t\xd9\x97\x82\x1d\xa7\x96\x90\xed\xf6\xc5\x14:B\x8f\xdcQ5a'
