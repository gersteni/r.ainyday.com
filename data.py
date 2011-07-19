from google.appengine.ext import db

class Watcher(db.Model):
    """Model for the users"""
    email = db.StringProperty()
    zip = db.IntegerProperty()
    
def group_key():
    return db.Key.from_path('watchers', 'main_watchers')

def make_watcher(email, zip):
    k = group_key()
    watcher = Watcher(parent=k)
    watcher.email = email
    watcher.zip = zip
    watcher.put()

def get_watchers():
    return db.GqlQuery("SELECT * "
                       "FROM Watcher "
                       "WHERE ANCESTOR IS :1",
                       group_key())
