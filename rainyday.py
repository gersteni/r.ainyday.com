import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
             <body>
               <form action="/register" method="post">                                             
                <div><label>Email:</label><input type="text" name="email" /></div> 
                <div><label>Zip code:</label><input type="text" name="zip"></div>
                <div><input type="submit" value="Let me know"></div>                             
              </form>
             </body>
          </html>""")

class Registration(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('email')))
        self.response.out.write(cgi.escape(self.request.get('zip')))
        self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/register', Registration)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
