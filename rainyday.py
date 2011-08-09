import cgi
import os
from data import make_watcher, get_watchers

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
            'zip': int(cgi.escape(self.request.get('zip')))
            }
        make_watcher(vals['email'], vals['zip'])
        path = os.path.join(os.path.dirname(__file__), 'done.html')
        self.response.out.write(template.render(path, vals))

class Admin(webapp.RequestHandler):
    def get(self):
        vals = { 'watchers' : get_watchers() }
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, vals))

# really just for testing convenience
class SignOut(webapp.RequestHandler):
    def get(self):
        vals = { 'sign_out_link' : users.create_logout_url('/') }
        path = os.path.join(os.path.dirname(__file__), 'sign_out.html')
        self.response.out.write(template.render(path, vals))

application = webapp.WSGIApplication(
                                     [ ('/', MainPage),
                                       ('/register', Registration),
                                       ('/admin', Admin),
                                       ('/signout', SignOut) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
