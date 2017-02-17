#!/usr/bin/env python

import webapp2
import jinja2
import os
from model import Project
import json
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

title = "sym LOCAL " if os.environ['SERVER_SOFTWARE'].startswith('Development') else "sym LIVE DEV "

def proj_key(proj_name=None):
    """Constructs a Datastore key for a proj entity with name proj_name."""
    return ndb.Key('cal', 'TODO_wtf_is_an_ndb_key')

# the main sym app
class SYM_app(webapp2.RequestHandler):
    def get(self):
        template_values = {"title": title + "HOME"}

        template = JINJA_ENVIRONMENT.get_template('templates/app.html')
        self.response.write(template.render(template_values))


# the page that lists all the projects on sym
class SYM_list(webapp2.RequestHandler):
    def get(self):
        projects = Project.query().fetch(420)

        template_values = {"title": title + "proj_list",
                           "projects": projects}

        template = JINJA_ENVIRONMENT.get_template('templates/list.html')
        self.response.write(template.render(template_values))


# loads a project with name given as proj_name in get request
class SYM_load(webapp2.RequestHandler):
    def get(self):
        proj_name = self.request.get('proj_name')
        projs = Project.query(Project.name == proj_name).fetch(1)

        if len(projs) == 0:
            # todo: uh oh
            self.response.http_status_message(404)
        else:
            proj = projs[0]
            self.response.headers['Content-Type'] = 'text/json'
            self.response.write(json.dumps(proj.shapes))


# writes a project to the db, makes a new one if none exists
class SYM_store(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        proj_name = self.request.get('proj_name')
        proj_data = self.request.get('proj_data')

        projs = Project.query(Project.name == proj_name).fetch(1)

        if len(projs) == 0:
            new_proj = Project(parent=proj_key(proj_name))
            new_proj.name = proj_name
            new_proj.owner = "charlie"
            new_proj.shapes = json.loads(proj_data)
            new_proj.put()
        else:
            proj = projs[0]
            proj.shaps = json.loads(proj_data)
            proj.owner = "charlie2"
            proj.put()

        self.response.write("you should really posting to /store")


app = webapp2.WSGIApplication([
    ('/', SYM_app),
    ('/list', SYM_list),
    ('/getproject', SYM_load),
    ('/storeproject', SYM_store),    
], debug=True)
