"""
*    Author: Rob Hemsley
*    Contact: hemsley@media.mit.edu
"""

import settings, APIV1

from twisted.web.static import File

# Import Twisted 
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.enterprise import adbapi 
from twisted.python import log

class API(File):
    
    def __init__(self):
        Resource.__init__(self)
        self.putChild('v1', APIV1.API1())         
        self.putChild('ahh', File('html')) 

    def getChild(self, path, request):
        #if path == '':
            return File('html')
        
        #return Resource.getChild(self, path, request)

if __name__ == '__main__':

    web = Site(API())
    reactor.listenTCP(settings._PORT_NUM, web)
    reactor.run()
            
