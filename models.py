import cgi
import os
import datetime


from google.appengine.ext import db
from google.appengine.api import users


class User(db.Model):
    google_user = db.UserProperty()
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    friends = db.ListProperty(users.User, indexed=True)

    @staticmethod
    def get_by_google_user(g_user):
        return User.all().filter('google_user = ', g_user).get()
        
    
class SomeEntity(db.Model):
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User)
    tags = db.ListProperty(db.Category)
    text = db.StringProperty(required=True)
    
    @staticmethod
    def get_by_name(name):
       return SomeEntity.all().filter('name = ', name).get()

