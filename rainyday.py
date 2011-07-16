import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

class Registration(webapp.RequestHandler):
    def post(self):
        vals = { 
            'email': cgi.escape(self.request.get('email')),
            'zip': cgi.escape(self.request.get('zip'))
            }
        path = os.path.join(os.path.dirname(__file__), 'done.html')
        self.response.out.write(template.render(path, vals))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/register', Registration)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
