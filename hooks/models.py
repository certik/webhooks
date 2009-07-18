from appengine_django.models import BaseModel
from google.appengine.ext import db

class User(BaseModel):
    name = db.StringProperty()
    email = db.StringProperty()

class Repository(BaseModel):
    name = db.StringProperty()
    owner = db.ReferenceProperty(User)

class RepoUpdate(BaseModel):
    update = db.TextProperty()
    repo = db.ReferenceProperty(Repository)
