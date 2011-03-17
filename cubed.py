#!/usr/bin/env python

import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util
from google.appengine.api import users


from models import User
from constants import *


#What the Template App Still Needs

#- Basic Security Features
#- Data validation decorator
#- Sign in 
#- Must sign in decorator


# Decorators
def MustLogIn(inFunction):
    """Must Log in Decorator - Ensures that user is logged in"""
    def outFunction(*args,**kwargs):
        
        user = users.get_current_user()
        
        if user:
			return inFunction(*args,**kwargs)
        else :
            self.redirect(users.create_login_url("/save"))
            

    return outFunction


# Home Page Handler
class MainHandler(webapp.RequestHandler):
    def get(self):
        
        content_template_values = {
           
        }
       
        self.response.out.write(RenderFullPage('page1.html', content_template_values))



# Page Handlers
class PageHandler1(webapp.RequestHandler):
    def get(self):
        template_values = {

        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/page1.html')
        self.response.out.write(template.render(path, template_values))

       
        
class PageHandler2(webapp.RequestHandler):
    
    @MustLogIn
    def get(self):
        
        saved_users = User.all().fetch(100)
        template_values = {
            'saved_users': saved_users 
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/page2.html')
        self.response.out.write(template.render(path, template_values))


# Gets
class GetMethod(webapp.RequestHandler):
    def get(self):
        return 0



# Posts
class PostMethod(webapp.RequestHandler):
    def post(self):
        return 0

class SaveUser(webapp.RequestHandler):
    
    @MustLogIn
    def get(self):
        google_user = users.get_current_user()
        db_user = User.get_by_google_user(google_user)
        
        if db_user:
            self.redirect('/')
            
        else:
            db_user = User()
            db_user.google_user = google_user
            db_user.put()
            self.redirect('/')
        
        

# Helpers
def RenderFullPage(template_file_name, content_template_values):
    """This re-renders the full page with the specified template."""
    
    main_path = os.path.join('templates/index.html')
    content_path = os.path.join('templates/' + template_file_name )
    
    content = template.render(content_path, content_template_values)
    
    user = users.get_current_user()
    if user:
        login = ("Welcome, %s! (<a href=\"%s\">Sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
    else:
        login = ("<a href=\"%s\">Sign in With Google</a>." % users.create_login_url("/save"))
    
    template_values = {
        'CONTENT': content,
        'LOGIN': login
    }
    
    return template.render(main_path, template_values)






appRoute = webapp.WSGIApplication( [('/page1', PageHandler1),
										('/page2', PageHandler2),
										('/save', SaveUser),
										('/', MainHandler)
										], debug=True)
										
def main():
    run_wsgi_app(appRoute)

if __name__ == '__main__':
    main()
