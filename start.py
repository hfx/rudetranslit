from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import urllib
import cgi
from translit import Translit

VERSION = os.environ.get('CURRENT_VERSION_ID','')

class OutputPage(webapp.RequestHandler):
    def get(self):
        template_dict = {
                         'post': False,
                         'version' : VERSION,
                         }
        self.response.out.write( template.render("output.html", template_dict, debug=True))
        
    def post(self):
        translit = Translit()
        type = cgi.escape( self.request.get('type') ) 
        input = cgi.escape( self.request.get('input') )     
          
        inLength = len(input)
        
        output = translit.translit(type, input)
                
        template_dict = {
                         'type': type,
                         'input': input,
                         'output' : output, 
                         'inLength' : inLength,
                         'post': True,
                         'version' : VERSION,
                         }
        self.response.out.write( template.render("output.html", template_dict, debug=True))


class PerUrl(webapp.RequestHandler):
    def get(self, type, input):
        translit = Translit()
        #type = type#self.request.get('type') 
        #input = #self.request.get('input')     
          
        input = urllib.unquote_plus(input)        
        input = input.decode("UTF-8", "replace")
        inLength = len(input)
        
        output = translit.translit(type, input)
                
        template_dict = {
                         'type': type,
                         'input': input,
                         'output' : output, 
                         'inLength' : inLength,
                         }
        
        self.response.out.write( template.render("ws.html", template_dict, debug=True))

application = webapp.WSGIApplication([
                                      ('/', OutputPage),
                                      ('/ws/(.*)/(.*)', PerUrl),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
