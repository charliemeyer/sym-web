#!/usr/bin/env python

import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

class HomePage(webapp2.RequestHandler):
    def get(self):
        page = '<h1 class="pagetitle">Welcome to Sched</h1>'
        page += "<h3 style='margin-bottom: 40px'>Let's get started</h3>"
        page += '<a href ="survey/" class="button bigbutton">Users</a>'
        page += '<a href ="admin/" class="button bigbutton">Admins</a>'

        title = "sym LOCAL" if os.environ['SERVER_SOFTWARE'].startswith('Development') else "sym LIVE DEV"

        template_values = {"title": title}

        template = JINJA_ENVIRONMENT.get_template('templates/app.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', HomePage)
], debug=True)
