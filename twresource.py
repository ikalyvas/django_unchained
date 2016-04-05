from twisted.web import server, resource, client
from twisted.internet import defer


class Root(resource.Resource):

    """Root resource that combines the two sites/entry points"""
    WSGI = None

    def __init__(self, wsgi):
       resource.Resource.__init__(self)
       self.WSGI = wsgi

    def getChild(self, child, request):
        request.prepath.pop()
        request.postpath.insert(0, child)
        print 'getChild: %s' % self.WSGI
        return self.WSGI

    def render_GET(self, request):
        """Delegate to the WSGI resource"""
        print 'rendering: %s' % request
        print 'WSGI: %s' % self.WSGI
        #return self.WSGI.render(request)
        return GoogleResource().render_GET(request)

class GoogleResource(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)

    def getChild(self, name, request):
        return self

    @defer.inlineCallbacks
    def get_page(self, request, q):
        page = yield client.getPage("http://google.com/search?q=%s" % q)
        request.write(page)
        request.finish()

    def render_GET(self, request):
        q = request.args.get('q', [""])[0]
        self.get_page(request, q)
        return server.NOT_DONE_YET
