import cgi
import os
import logging
from data import make_watcher, get_watchers
from weather import *

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
        vals = { 'watchers' : get_watchers(), 'helena_weather' : zipcode_fetch('59601') }
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, vals))

class Sweep(webapp.RequestHandler):
    def get(self):
        ws = get_watchers()
        zips = {}
        for w in ws:
            zips[str(w.zip)] = ""
        for zip in zips:
            zips[zip] = zipcode_fetch(zip)
        for_template = []
        for zip in zips:
            forecast = zips[zip]
            for_template.append({ 'zip' : zip, 'forecast' : forecast, 
                                  'is_rain' : is_rain(forecast) })
        # now find all the emails we would send to
        email_outs = []
        for w in ws:
            if (is_rain(zips[str(w.zip)])):
                email_outs.append(w.email)
        vals = { 'zips' : for_template, 'email_outs' : email_outs }
        path = os.path.join(os.path.dirname(__file__), 'sweep.html')
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
                                       ('/sweep', Sweep),
                                       ('/signout', SignOut) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
