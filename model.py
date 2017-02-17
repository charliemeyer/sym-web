from google.appengine.ext import ndb

class Project(ndb.Model):
    """Models an individual project"""
    name = ndb.StringProperty()
    owner = ndb.StringProperty()
    shapes = ndb.JsonProperty()
