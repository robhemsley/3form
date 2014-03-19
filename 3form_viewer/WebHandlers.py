import json

from twisted.web import static
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import File

webdir = File(".")
webdir.contentTypes['.webm'] = 'video/webm'
webdir.contentTypes['.mp4'] = 'video/mp4'
webdir.contentTypes['.mp2'] = 'video/mp2'
webdir.contentTypes['.json'] = 'application/json'
webdir.contentTypes['.m4v'] = 'video/x-m4v'

class StaticHandler(Resource):
    base_path  = None
    
    isLeaf = False
    
    def __init__(self, base_path):
        self.base_path = base_path
        Resource.__init__(self)

    def getChild(self, path, request):
        return static.File(self.base_path)

class JsonHandler(Resource):
    json     = None
    
    isLeaf = True
    def __init__(self, json_in):
        Resource.__init__(self)
        if isinstance(json_in, str):
            self.json = json_in
        else:
            self.json = json.dumps(json_in)
            
    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        return str(self.json)
    
    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        return str(self.json)

    def getChild(self, path, request):
        return self
    
class AppHandler(Resource):
    app     = None
    usr_id  =   None
    
    isLeaf = True
    def __init__(self, app, usr_id):
        self.app    = app
        self.usr_id = usr_id
        Resource.__init__(self)
        
    def render_GET(self, request):
        return self.app.render_request(self.usr_id, request)
    
    def render_POST(self, request):
        return self.app.render_request(self.usr_id, request)

    def getChild(self, path, request):
        return self

class HtmlHandler(Resource):
    html     = None
    
    isLeaf = True
    def __init__(self, html):
        Resource.__init__(self)
        self.html    = html
        
    def render_GET(self, request):
        return self.html
    
    def render_POST(self, request):
        return self.html

    def getChild(self, path, request):
        return self
    
class NotDoneHandler(Resource):
    html     = None
    
    isLeaf = True
    def __init__(self):
        Resource.__init__(self)
        
    def render_GET(self, request):
        return NOT_DONE_YET
    
    def render_POST(self, request):
        return NOT_DONE_YET

    def getChild(self, path, request):
        return self
    
class DataHandler(Resource):
    data     = None
    mimetype = None
    
    isLeaf = True
    def __init__(self, data, mimetype):
        Resource.__init__(self)
        self.data       = data
        self.mimetype   = mimetype
        
    def render_GET(self, request):
        request.setHeader('Content-Type', self.mimetype)
        return self.data
    
    def render_POST(self, request):
        request.setHeader('Content-Type', self.mimetype)
        return self.data

    def getChild(self, path, request):
        return self
