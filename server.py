import sys
import os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor

import twresource

#import server_settings
PORT = 8092
DJANGO_PROJECT_PATH = "/home/django/lvnproject/Weblvn/"
TWISTED_LOG = "/home/django/lvnproject/Weblvn/log/twistd.log"

# Environment setup for your Django project files:
sys.path.append(DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Weblvn.settings'
from django.core.handlers.wsgi import WSGIHandler

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # Allow Ctrl-C to get you out cleanly:
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource


# Twisted Application Framework setup:
application = service.Application('twisted-django')

# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root 
wsgi_root = wsgi_resource()
root = twresource.Root(wsgi_root)

# Servce Django media files off of /media:
staticrsrc = static.File(os.path.join(DJANGO_PROJECT_PATH, "Weblvn/media"))
root.putChild("media", staticrsrc)


# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
#root.putChild("google", twresource.GoogleResource())

# my add (from buildbot runner.py):
rotateLength = 10000000
maxRotatedFiles = 5
try:
  from twisted.python.logfile import LogFile
  from twisted.python.log import ILogObserver, FileLogObserver
  logfile = LogFile.fromFullPath(TWISTED_LOG, rotateLength=rotateLength,
                                 maxRotatedFiles=maxRotatedFiles)
  application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
except ImportError:
  # probably not yet twisted 8.2.0 and beyond, can't set log yet
  pass

# Serve it up:
main_site = server.Site(root)


internet.TCPServer(PORT, main_site).setServiceParent(application)
